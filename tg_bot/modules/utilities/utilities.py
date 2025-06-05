import requests
import subprocess
from subprocess import Popen, PIPE
from speedtest import Speedtest
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from telegram.constants import ParseMode
from tg_bot.core.permissions import owner, authorized
from tg_bot.core.logging import LOGI
from tg_bot.core.bot import get_bot_context


@owner
async def sh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        return await update.message.reply_text("Usage: /sh <command>")

    command = " ".join(context.args)
    msg = await update.message.reply_text(f"~$ {command}")

    out = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = out.communicate()
    output = (stderr + stdout).decode()

    await context.bot.edit_message_text(
        f"<b>~$ {command}</b>\n<code>{output}</code>",
        chat_id=update.message.chat_id,
        message_id=msg.message_id,
        parse_mode="HTML",
    )


@owner
async def shell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        return await update.message.reply_text("Usage: /shell <command>")

    command = " ".join(context.args)
    try:
        process = subprocess.check_output(
            command,
            shell=True,
            executable="/bin/bash",
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        returncode = 0
        output = process
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        output = e.output

    await update.message.reply_text(f"Command: {command}\n"
                                    f"Return code: {returncode}\n\n"
                                    f"Output:\n{output}")


@authorized
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    if message.reply_to_message:
        await message.reply_to_message.reply_text(args[1])
    else:
        await message.reply_text(args[1])
    try:
        await message.delete()
    except BadRequest:
        pass


@authorized
async def speedtest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sent_message = await update.message.reply_text("Running speedtest...")
    message_id = sent_message.message_id
    LOGI("Started")
    
    speedtest = Speedtest()
    speedtest.get_best_server()
    speedtest.download()
    speedtest.upload()
    speedtest.results.share()
    results_dict = speedtest.results.dict()
    
    download = str(results_dict["download"] // 10**6)
    upload = str(results_dict["upload"] // 10**6)
    
    await context.bot.edit_message_text(
        chat_id=update.message.chat_id,
        message_id=message_id,
        text=f"Download: {download} mbps\n"
             f"Upload: {upload} mbps",
    )
    
    LOGI(f"Finished, download: {download} mbps, upload: {upload} mbps")


@authorized
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    before = datetime.now()
    message = await update.message.reply_text("Appraising..")
    now = datetime.now()
    res = (now - before).microseconds / 1000
    await message.edit_text(f"ping = {res}ms")


async def paste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        await message.reply_text("What am I supposed to do with this?")
        return

    try:
        response = requests.post("https://nekobin.com/api/documents",
                                 json={"content": data})
        json_data = response.json()
        print("Nekobin raw response:",
              json_data)
        key = json_data.get("result", {}).get("key")
        if not key:
            raise ValueError("Nekobin response missing key")
    except Exception as e:
        await message.reply_text(f"Failed to paste: {e}")
        return

    url = f"https://nekobin.com/{key}"
    reply_text = f"Nekofied to *Nekobin* : {url}"

    await message.reply_text(reply_text,
                             parse_mode=ParseMode.MARKDOWN,
                             disable_web_page_preview=True)


@owner
async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gracefully shut down the bot."""
    LOGI("Exit command received, shutting down bot")
    await update.effective_message.reply_text("Exiting now...")

    # Get the Bot instance and stop it gracefully
    bot = get_bot_context()
    if bot:
        await bot.stop()
    else:
        LOGI("Bot context not available, cannot stop gracefully")


sh.handler = {"type": "command", "commands": ["sh"]}
shell.handler = {"type": "command", "commands": ["shell"]}
echo.handler = {"type": "command", "commands": ["echo"]}
speedtest.handler = {"type": "command", "commands": ["speedtest"]}
ping.handler = {"type": "command", "commands": ["ping"]}
paste.handler = {"type": "command", "commands": ["paste"]}
exit.handler = {"type": "command", "commands": ["exit"]}

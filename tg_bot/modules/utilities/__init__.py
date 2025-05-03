from subprocess import Popen, PIPE
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from telegram.error import BadRequest
from tg_bot.core.permissions import owner, authorized
import subprocess


@owner
async def sh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 1:
        return await update.message.reply_text("Usage: /sh <command>")

    command = " ".join(context.args)
    msg = await update.message.reply_text(f"~$ {command}")

    out = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = out.communicate()
    output = (stderr + stdout).decode()

    await update.message.bot.edit_message_text(
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


# Define commands as CommandHandler instances
commands = [
    CommandHandler("sh", sh),
    CommandHandler("shell", shell),
    CommandHandler("echo", echo),
]

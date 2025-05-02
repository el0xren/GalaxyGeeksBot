import subprocess
from subprocess import Popen, PIPE
from telegram import Update
from telegram.ext import CallbackContext
from tg_bot.core.permissions import owner
from tg_bot.core.modules_manager import Command

@owner
def sh(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        return update.message.reply_text("Usage: /sh <command>")

    command = " ".join(context.args)
    msg = update.message.reply_text(f"~$ {command}")

    out = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = out.communicate()
    output = (stderr + stdout).decode()

    update.message.bot.edit_message_text(
        f"<b>~$ {command}</b>\n<code>{output}</code>",
        chat_id=update.message.chat_id,
        message_id=msg.message_id,
        parse_mode="HTML"
    )

@owner
def shell(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        return update.message.reply_text("Usage: /shell <command>")

    command = " ".join(context.args)
    try:
        process = subprocess.check_output(
            command,
            shell=True,
            executable="/bin/bash",
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        returncode = 0
        output = process
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        output = e.output

    update.message.reply_text(
        f"Command: {command}\n"
        f"Return code: {returncode}\n\n"
        f"Output:\n{output}"
    )

commands = {
    sh: ['sh'],
    shell: ['shell']
}

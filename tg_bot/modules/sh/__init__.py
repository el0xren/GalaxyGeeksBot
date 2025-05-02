from subprocess import Popen,PIPE
from telegram import Update

allowed = [] # Seperate ID's with [ , ], like this allowed = "[6969696969,6969696969]"

def sh(update:Update,context):
    if update.message.from_user.id not in allowed:
        update.message.reply_text("Error: You are not authorized to execute sh")
        return
    command = update.message.text.replace("/sh","").split(" ", 1)[1]
    msg = update.message.reply_text(f"~$ {command}")
    out = Popen(command,shell=True,stdout=PIPE,stderr=PIPE)
    stdout,stderr = out.communicate()
    output = str(stderr.decode() + stdout.decode())
    update.message.bot.edit_message_text(
        f"<b>~$ {command}</b>\n<code>{output}</code>",
        chat_id=update.message.chat_id,
        message_id=msg.message_id,
        parse_mode="HTML"
    )

commands = {
	sh: ['sh']
}

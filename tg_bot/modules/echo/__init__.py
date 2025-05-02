from telegram.ext import CallbackContext
from telegram.update import Update

allowed = [] # Seperate ID's with [ , ], like this "allowed = [6969696969,6969696969]"

def echo(update, context):
    if update.message.from_user.id not in allowed:
        update.message.reply_text("Error: You are not authorized to execute echo")
        return
    update.message.reply_text(update.message.text.replace("/echo",""))
    
commands = {
    echo : ['echo']
}

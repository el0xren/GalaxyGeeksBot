import time
from datetime import datetime

def ping(update,context):
    before = datetime.now()
    message = update.message.reply_text("Appraising..")
    now =  datetime.now()
    res = (now-before).microseconds / 1000
    update.message.bot.edit_message_text(f"ping = {res}ms",update.message.chat_id,message.message_id)

commands = {
	ping: ['ping']
}

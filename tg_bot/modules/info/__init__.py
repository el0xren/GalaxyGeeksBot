from telegram import Update,ParseMode
from telegram.ext import CallbackContext
from os import remove

def info(update:Update,context:CallbackContext):
    chat_id = update.message.chat_id
    message = update.message
    bot = message.bot
    user = bot.get_chat_member(chat_id,message.from_user.id)
    if message.reply_to_message:
        user = bot.get_chat_member(chat_id,message.reply_to_message.from_user.id)
    try:
        text = "\n<b>User Info:</b>\n\n"
        text += f"ID: {user.user.id}\n"
        text += f"First Name: {user.user.first_name}\n"
        if user.user.username:
            text += f"Username: @{user.user.username}\n"
        text += f"{user.user.last_name if user.user.last_name != None else 'Last Name: null'}\n"
        if user.user.language_code:
            text += f"Language Code: {user.user.language_code}\n"
        text += f"Bot: {user.user.is_bot}\n\n"
        text += "<b>Admin Status:</b>\n"
        if user.ADMINISTRATOR:
            text += f"Status: {user.status if user.status != None else 'null'}\n"
            text += f"Title: {user.custom_title}\n"
        photo = context.bot.get_user_profile_photos(user.user.id).photos[0][-1]
        file = update.message.bot.get_file(photo["file_id"])
        file.download(f"{user.user.id}.png")
        update.message.bot.send_document(
                chat_id=update.message.chat_id,
                caption=text,
                document=open(f"{user.user.id}.png","rb"),
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id
            )
        remove(f"{user.user.id}.png")
    except Exception as e:
        update.message.reply_text(f"Couldn't parse user info!\nError:{e}")
        remove(f"{user.user.id}.png")

def id(update:Update, context:CallbackContext):
    message = update.effective_message
    user = update.effective_user
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    message.reply_text(f"{user.name}'s id is <code>{user.id}</code>",parse_mode="html")

def chat_id(update:Update, context:CallbackContext):
    message = update.effective_message
    message.reply_text(f"this chat's id <code>{message.chat_id}</code>",parse_mode="html")

commands = {
	info: ['info'],
    id: ["id","get_id"],
    chat_id: ["get_chat","chat_id","chat"]
}

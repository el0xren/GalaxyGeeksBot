from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from os import remove


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Retrieve and display user information, including profile photo if available."""
    chat_id = update.message.chat_id
    message = update.message
    bot = context.bot
    # Get user info (from sender or replied-to user)
    user = await bot.get_chat_member(chat_id, message.from_user.id)
    if message.reply_to_message:
        user = await bot.get_chat_member(chat_id,
                                         message.reply_to_message.from_user.id)

    try:
        text = "<b>User Info:</b>\n\n"
        text += f"ID: {user.user.id}\n"
        text += f"First Name: {user.user.first_name}\n"
        if user.user.username:
            text += f"Username: @{user.user.username}\n"
        text += f"Last Name: {user.user.last_name or 'null'}\n"
        if user.user.language_code:
            text += f"Language Code: {user.user.language_code}\n"
        text += f"Bot: {user.user.is_bot}\n\n"
        text += "<b>Admin Status:</b>\n"
        if user.status == "administrator":
            text += f"Status: {user.status}\n"
            text += f"Title: {user.custom_title or 'None'}\n"

        # Try to get and send profile photo
        photo = (await
                 context.bot.get_user_profile_photos(user.user.id)).photos
        if photo:
            file = await bot.get_file(photo[0][-1]["file_id"])
            file_path = f"{user.user.id}.png"
            await file.download_to_drive(file_path)
            try:
                await bot.send_document(
                    chat_id=chat_id,
                    caption=text,
                    document=open(file_path, "rb"),
                    parse_mode=ParseMode.HTML,
                    reply_to_message_id=message.message_id,
                )
            finally:
                remove(file_path)
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=text + "\nNo profile photo available.",
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message.message_id,
            )
    except Exception as e:
        await update.message.reply_text(
            f"Couldn't parse user info!\nError: {e}")
        try:
            remove(f"{user.user.id}.png")
        except FileNotFoundError:
            pass


async def id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the ID of the user or replied-to user."""
    message = update.effective_message
    user = update.effective_user
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    await message.reply_text(f"{user.name}'s id is <code>{user.id}</code>",
                             parse_mode=ParseMode.HTML)


async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the chat ID."""
    message = update.effective_message
    await message.reply_text(
        f"This chat's id is <code>{message.chat_id}</code>",
        parse_mode=ParseMode.HTML)



info.handler = {"type": "command", "commands": ["info"]}
id.handler = {"type": "command", "commands": ["id"]}
chat_id.handler = {"type": "command", "commands": ["chat_id"]}

from tg_bot import get_config
from tg_bot.core.logging import LOGI
from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
import json
from pathlib import Path

OWNER_ID = int(get_config("OWNER_ID"))
authorized_file = Path("tg_bot/authorized_users.json")


def user_is_admin(user_id):
    """
    Check if the given user ID is in the list
    of the approved user IDs.
    """
    if str(user_id) not in get_config("CI_APPROVED_USER_IDS").split():
        LOGI(f"Access denied to user {user_id}")
        return False
    LOGI(f"Access granted to user {user_id}")
    return True


def owner(func):

    @wraps(func)
    async def is_owner(update: Update, context: ContextTypes.DEFAULT_TYPE,
                       *args, **kwargs):
        user = update.effective_user
        message = update.effective_message
        if user and user.id == OWNER_ID:
            return await func(update, context, *args, **kwargs)
        else:
            if message:
                await message.reply_text(
                    "This is a restricted command. You do not have permission to run this."
                )

    return is_owner


def is_authorized(user_id):
    if authorized_file.exists():
        with authorized_file.open("r") as f:
            authorized_users = json.load(f)
    else:
        authorized_users = []

    return str(user_id) in map(str, authorized_users)


def authorized(func):

    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE,
                      *args, **kwargs):
        user = update.effective_user
        message = update.effective_message
        if user and (user.id == OWNER_ID or is_authorized(user.id)):
            return await func(update, context, *args, **kwargs)
        if message:
            await message.reply_text(
                "You're not authorized to run this command.")

    return wrapper

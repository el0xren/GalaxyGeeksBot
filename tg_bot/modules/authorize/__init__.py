import json
from pathlib import Path
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from tg_bot.core.permissions import owner

authorized_file = Path("tg_bot/authorized_users.json")


def read_authorized_users():
    """Read authorized users from file."""
    if authorized_file.exists():
        try:
            with authorized_file.open("r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


def write_authorized_users(users):
    """Write authorized users to file."""
    authorized_file.write_text(json.dumps(users))


@owner
async def authorize(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    """Authorize a user by replying to their message or providing a user ID."""
    authorized_users = read_authorized_users()
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        if user_id in authorized_users:
            return await update.message.reply_text(
                f"User {user_id} is already authorized.")
        authorized_users.append(user_id)
        write_authorized_users(authorized_users)
        await update.message.reply_text(f"Authorized user {user_id}")
    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("Invalid user ID.")
        if user_id in authorized_users:
            return await update.message.reply_text(
                "User is already authorized.")
        authorized_users.append(user_id)
        write_authorized_users(authorized_users)
        await update.message.reply_text(f"Authorized user {user_id}.")
    else:
        await update.message.reply_text(
            "Usage: /authorize <user_id> or reply to a message to authorize a user."
        )


@owner
async def unauthorize(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unauthorize a user by replying to their message or providing a user ID."""
    authorized_users = read_authorized_users()
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        if user_id not in authorized_users:
            return await update.message.reply_text(
                f"User {user_id} is not authorized.")
        authorized_users.remove(user_id)
        write_authorized_users(authorized_users)
        await update.message.reply_text(f"Unauthorized user {user_id}")
    elif context.args:
        try:
            user_id = int(context.args[0])
        except ValueError:
            return await update.message.reply_text("Invalid user ID.")
        if user_id not in authorized_users:
            return await update.message.reply_text(
                f"User {user_id} is not authorized.")
        authorized_users.remove(user_id)
        write_authorized_users(authorized_users)
        await update.message.reply_text(f"Unauthorized user {user_id}.")
    else:
        await update.message.reply_text(
            "Usage: /unauthorize <user_id> or reply to a message to unauthorize a user."
        )


@owner
async def list_authorized(update: Update,
                          context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all authorized users."""
    authorized_users = read_authorized_users()
    if not authorized_users:
        return await update.message.reply_text("No users are authorized yet.")
    users = "\n".join(str(uid) for uid in authorized_users)
    await update.message.reply_text(f"Authorized users:\n{users}")


# Define commands as CommandHandler instances for Module integration
commands = [
    CommandHandler("authorize", authorize),
    CommandHandler("unauthorize", unauthorize),
    CommandHandler("authorized", list_authorized),
]

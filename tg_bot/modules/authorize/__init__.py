import json
from pathlib import Path
from telegram import Update
from telegram.ext import CallbackContext
from tg_bot.core.permissions import owner
from tg_bot.core.modules_manager import Command

authorized_file = Path("authorized_users.json")

if authorized_file.exists():
    with authorized_file.open("r") as f:
        authorized_users = json.load(f)
else:
    authorized_users = []
    authorized_file.write_text(json.dumps(authorized_users))

@owner
def authorize(update: Update, context: CallbackContext):
    if not context.args:
        return update.message.reply_text("Usage: /authorize <user_id>")

    try:
        user_id = int(context.args[0])
    except ValueError:
        return update.message.reply_text("Invalid user ID.")

    if user_id in authorized_users:
        return update.message.reply_text("User is already authorized.")

    authorized_users.append(user_id)
    authorized_file.write_text(json.dumps(authorized_users))
    update.message.reply_text(f"Authorized user {user_id}.")

@owner
def unauthorize(update: Update, context: CallbackContext):
    if not context.args:
        return update.message.reply_text("Usage: /unauthorize <user_id>")

    try:
        user_id = int(context.args[0])
    except ValueError:
        return update.message.reply_text("Invalid user ID.")

    if user_id not in authorized_users:
        return update.message.reply_text("User is not authorized.")

    authorized_users.remove(user_id)
    authorized_file.write_text(json.dumps(authorized_users))
    update.message.reply_text(f"Unauthorized user {user_id}.")

@owner
def list_authorized(update: Update, context: CallbackContext):
    if not authorized_users:
        return update.message.reply_text("No users are authorized yet.")

    users = "\n".join(str(uid) for uid in authorized_users)
    update.message.reply_text(f"Authorized users:\n{users}")

commands = {
    authorize: ["authorize"],
    unauthorize: ["unauthorize"],
    list_authorized: ["authorized"]
}

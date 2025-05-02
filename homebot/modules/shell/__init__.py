from tg_bot.core.admin import user_is_admin
import subprocess
from telegram.ext import CallbackContext
from telegram.update import Update

def shell(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to load modules")
		return

	if len(update.message.text.split(' ', 1)) < 2:
		update.message.reply_text("No command provided")
		return

	command = update.message.text.split(' ', 1)[1]
	try:
		process = subprocess.check_output(command, shell=True, executable="/bin/bash",
										  stderr=subprocess.STDOUT, universal_newlines=True)
	except subprocess.CalledProcessError as e:
		returncode = e.returncode
		output = e.output
	else:
		returncode = 0
		output = process

	update.message.reply_text(f"Command: {command}\n"
							  f"Return code: {returncode}\n\n"
							  f"Output:\n"
							  f"{output}\n")

commands = {
	shell: ['shell']
}

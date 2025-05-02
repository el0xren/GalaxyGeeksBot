from contextlib import redirect_stdout
from cowsay import cow
import io
from telegram.ext import CallbackContext
from telegram.update import Update

def cowsay(update: Update, context: CallbackContext):
	with io.StringIO() as buf, redirect_stdout(buf):
		try:
			cow(update.message.text.split(' ', 1)[1])
		except IndexError:
			update.message.reply_text("Error: Write something after the command!")
		else:
			update.message.reply_text(f"`{buf.getvalue()}`", parse_mode="Markdown")

commands = {
	cowsay: ['cowsay']
}

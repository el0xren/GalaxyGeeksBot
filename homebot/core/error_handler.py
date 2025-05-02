from tg_bot.core.logging import LOGE
from telegram.ext import CallbackContext
from telegram.update import Update
import traceback

def error_handler(update: Update, context: CallbackContext):
	formatted_error =   "GalaxyGeeksBot: Error encountered!\n"
	formatted_error += f"Command sent: {update.message.text}\n\n"
	formatted_error +=  ''.join(traceback.format_exception(type(context.error), context.error,
														   context.error.__traceback__,
														   limit=None, chain=True))
	update.message.reply_text(formatted_error)
	LOGE(formatted_error)
	LOGE("End error handling")

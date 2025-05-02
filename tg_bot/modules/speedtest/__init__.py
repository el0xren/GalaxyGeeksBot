from tg_bot.core.logging import LOGI
from speedtest import Speedtest
from telegram.ext import CallbackContext
from telegram.update import Update

def speedtest(update: Update, context: CallbackContext):
	message_id = update.message.reply_text("Running speedtest...").message_id
	LOGI("Started")
	speedtest = Speedtest()
	speedtest.get_best_server()
	speedtest.download()
	speedtest.upload()
	speedtest.results.share()
	results_dict = speedtest.results.dict()
	download = str(results_dict["download"] // 10 ** 6)
	upload = str(results_dict["upload"] // 10 ** 6)
	context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=message_id,
								  text=f"Download: {download} mbps\n"
									   f"Upload: {upload} mbps")
	LOGI(f"Finished, download: {download} mbps, upload: {upload} mbps")

commands = {
	speedtest: ['speedtest']
}

from tg_bot.core.logging import LOGI
from speedtest import Speedtest
from telegram.ext import CommandHandler, ContextTypes
from telegram import Update


async def speedtest(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = await update.message.reply_text("Running speedtest..."
                                                 ).message_id
    LOGI("Started")
    speedtest = Speedtest()
    speedtest.get_best_server()
    speedtest.download()
    speedtest.upload()
    speedtest.results.share()
    results_dict = speedtest.results.dict()
    download = str(results_dict["download"] // 10**6)
    upload = str(results_dict["upload"] // 10**6)
    await context.bot.edit_message_text(
        chat_id=update.message.chat_id,
        message_id=message_id,
        text=f"Download: {download} mbps\n"
        f"Upload: {upload} mbps",
    )
    LOGI(f"Finished, download: {download} mbps, upload: {upload} mbps")


# Define commands as CommandHandler instances
commands = [
    CommandHandler("speedtest", speedtest),
]

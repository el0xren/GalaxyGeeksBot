from tg_bot import __version__, get_config
from tg_bot.core.bot import Bot
from tg_bot.core.logging import LOGI

def main():
    bot = Bot(get_config("BOT_API_TOKEN"))
    support_chat_id = int(get_config("SUPPORT_CHAT_ID"))
    LOGI(f"GalaxyGeeksBot started, version {__version__}")
    LOGI(f"Bot username: @{bot.updater.bot.get_me().username}")
    bot.updater.bot.send_message(
        chat_id=support_chat_id,
        text=f"🤖 GalaxyGeeksBot v{__version__} has started successfully!",
        disable_web_page_preview=True,
    )
    bot.updater.start_polling()


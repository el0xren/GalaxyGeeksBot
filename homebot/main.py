from tg_bot import __version__, get_config
from tg_bot.core.bot import Bot
from tg_bot.core.logging import LOGI

def main():
	bot = Bot(get_config("BOT_API_TOKEN"))
	LOGI(f"GalaxyGeeksBot started, version {__version__}")
	LOGI(f"Bot username: @{bot.updater.bot.get_me().username}")
	bot.updater.start_polling()

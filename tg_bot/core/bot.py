from tg_bot import modules_path
from tg_bot.core.error_handler import error_handler
from tg_bot.core.modules_manager import Module
from tg_bot.core.logging import LOGE, LOGI
from pkgutil import iter_modules
from telegram.ext import Updater

# TODO: Find a better way to provide
# modules status to modules itself
bot = None

def get_bot_context():
	return bot

class Bot:
	"""
	This class represent a bot instance.
	"""
	def __init__(self, token):
		"""
		Initialize the bot and its modules.
		"""
		LOGI("Initializing bot")
		self.updater = Updater(token=token, use_context=True)
		self.dispatcher = self.updater.dispatcher
		self.dispatcher.add_error_handler(error_handler, True)
		self.modules = {}
		LOGI("Bot initialized")

		LOGI("Parsing modules")
		for module in [name for _, name, _ in iter_modules([modules_path])]:
			try:
				module = Module(module)
			except Exception as e:
				LOGE(f"Error loading module {module}, will be skipped\n"
					 f"Error: {e}")
			else:
				self.modules[module] = "Disabled"
		LOGI("Modules parsed")

		LOGI("Loading modules")
		for module in self.modules:
			self.load_module(module)
		LOGI("Modules loaded")

		# TODO: Find a better way to provide
		# modules status to modules itself
		global bot
		bot = self

	def load_module(self, module: Module):
		"""
		Load a provided module and add its command handler
		to the bot's dispatcher.
		"""
		LOGI(f"Loading module {module.name}")
		self.modules[module] = "Starting up"

		for command in module.commands:
			self.dispatcher.add_handler(command.handler)

		self.modules[module] = "Running"
		LOGI(f"Module {module.name} loaded")

	def unload_module(self, module: Module):
		"""
		Unload a provided module and remove its command handler
		from the bot's dispatcher.
		"""
		LOGI(f"Unloading module {module.name}")
		self.modules[module] = "Stopping"

		for command in module.commands:
			self.dispatcher.remove_handler(command.handler)

		LOGI(f"Module {module.name} unloaded")
		self.modules[module] = "Disabled"

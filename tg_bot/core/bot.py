from tg_bot import modules_path
from tg_bot.core.error_handler import error_handler
from tg_bot.core.modules_manager import Module
from tg_bot.core.logging import LOGE, LOGI
from pkgutil import iter_modules
from telegram.ext import Application

# Global bot instance reference
bot = None


def get_bot_context():
    return bot


class Bot:
    """
    This class represents a bot instance.
    """

    def __init__(self, application: Application):
        """
        Initialize the bot and its modules.
        """
        LOGI("Initializing bot")
        self.application = application
        # Add error handler
        self.application.add_error_handler(error_handler)
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
        # Set global bot reference
        global bot
        bot = self

    def load_module(self, module: Module):
        """
        Load a provided module and add its command handler
        to the bot's application.
        """
        LOGI(f"Loading module {module.name}")
        self.modules[module] = "Starting up"
        for command in module.commands:
            # Add handlers to application
            self.application.add_handler(
                command.handler)  # Use command.handler
        self.modules[module] = "Running"
        LOGI(f"Module {module.name} loaded")

    def unload_module(self, module: Module):
        """
        Unload a provided module and remove its command handler
        from the bot's application.
        """
        LOGI(f"Unloading module {module.name}")
        self.modules[module] = "Stopping"
        for command in module.commands:
            # Remove handlers from application
            for handler in self.application.handlers.get(None, []):
                if handler.callback == command.handler.callback:
                    self.application.handlers[None].remove(handler)
                    break
        LOGI(f"Module {module.name} unloaded")
        self.modules[module] = "Disabled"

    async def start(self):
        """
        Start the bot by initializing and running polling.
        """
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        """
        Stop the bot gracefully.
        """
        if self.application.updater.running:
            await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
        LOGI("Bot stopped")

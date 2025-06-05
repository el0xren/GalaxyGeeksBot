from tg_bot import modules_path
from tg_bot.core.error_handler import error_handler
from tg_bot.core.modules_manager import Module
from tg_bot.core.logging import LOGE, LOGI, LOGW
from telegram.ext import Application
import os

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
        self.application.add_error_handler(error_handler)
        self.modules = {}
        LOGI("Bot initialized")
        LOGI("Parsing modules")
        for root, dirs, files in os.walk(modules_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__")
            rel_path = os.path.relpath(root, modules_path)
            if rel_path == ".":
                continue
            for file in files:
                if not file.endswith(".py") or file == "__init__.py":
                    continue
                module_name = f"{rel_path.replace(os.sep, '.')}.{file[:-3]}"
                try:
                    module = Module(module_name)
                    LOGI(f"Loaded module {module_name} with commands: {[str(cmd) for cmd in module.commands]}")
                    self.modules[module] = "Disabled"
                except Exception as e:
                    LOGE(f"Error loading module {module_name}, will be skipped\nError: {e}")
        LOGI("Modules parsed")
        LOGI("Loading modules")
        for module in self.modules:
            self.load_module(module)
        LOGI("Modules loaded")
        global bot
        bot = self

    def load_module(self, module: Module):
        LOGI(f"Loading module {module.name}")
        self.modules[module] = "Starting up"
        for command in module.commands:
            self.application.add_handler(command.handler)
        self.modules[module] = "Running"
        LOGI(f"Module {module.name} loaded")

    def unload_module(self, module: Module):
        LOGI(f"Unloading module {module.name}")
        self.modules[module] = "Stopping"
        for command in module.commands:
            for handler in self.application.handlers.get(None, []):
                if handler.callback == command.handler.callback:
                    self.application.handlers[None].remove(handler)
                    break
        LOGI(f"Module {module.name} unloaded")
        self.modules[module] = "Disabled"

    async def start(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

    async def stop(self):
        if self.application.updater.running:
            await self.application.updater.stop()
        await self.application.stop()
        await self.application.shutdown()
        LOGI("Bot stopped")
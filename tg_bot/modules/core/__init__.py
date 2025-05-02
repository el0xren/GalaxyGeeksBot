from tg_bot import __version__, get_config
from tg_bot.core.bot import get_bot_context
from tg_bot.core.logging import LOGI
from tg_bot.core.permissions import authorized  # Importing the authorized decorator
from telegram.ext import CallbackContext
from telegram.update import Update

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm GalaxyGeeksBot, and I'm alive\n"
                              f"Version {__version__}\n"
                              "To see all the available modules, type /modules")

def modules(update: Update, context: CallbackContext):
    message = "Loaded modules:\n\n"
    modules = get_bot_context().modules
    for module in modules:
        message += f"{module.name}\n"
        message += f"Status: {modules[module]}\n"
        message += f"Commands: {', '.join([command.name for command in module.commands])}\n\n"
    update.message.reply_text(message)

@authorized  # Check if the user is authorized using the `authorized` decorator
def load(update: Update, context: CallbackContext):
    try:
        module_name = update.message.text.split(' ', 1)[1]
    except IndexError:
        update.message.reply_text("Error: Module name not provided")
        return

    if module_name == "core":
        update.message.reply_text("Error: You can't load module used for loading/unloading modules")
        return

    bot_context = get_bot_context()
    modules = bot_context.modules
    for module in modules:
        if module_name == module.name:
            bot_context.load_module(module)
            update.message.reply_text(f"Module {module_name} loaded")
            return

    update.message.reply_text("Error: Module not found")

@authorized  # Check if the user is authorized using the `authorized` decorator
def unload(update: Update, context: CallbackContext):
    try:
        module_name = update.message.text.split(' ', 1)[1]
    except IndexError:
        update.message.reply_text("Error: Module name not provided")
        return

    if module_name == "core":
        update.message.reply_text("Error: You can't unload module used for loading/unloading modules")
        return

    bot_context = get_bot_context()
    modules = bot_context.modules
    for module in modules:
        if module_name == module.name:
            bot_context.unload_module(module)
            update.message.reply_text(f"Module {module_name} unloaded")
            return

    update.message.reply_text("Error: Module not found")

commands = {
    start: ['start', 'help'],
    modules: ['modules'],
    load: ['load'],
    unload: ['unload']
}

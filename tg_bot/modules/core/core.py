from tg_bot import __version__
from tg_bot.core.bot import get_bot_context
from tg_bot.core.permissions import authorized
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start and /help commands."""
    await update.message.reply_text(
        "Hi! I'm GalaxyGeeksBot, and I'm alive\n"
        f"Version {__version__}\n"
        "To see all the available modules, type /modules")


async def modules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """List all loaded modules and their statuses."""
    message = "Loaded modules:\n\n"
    bot = get_bot_context()
    if not bot or not bot.modules:
        message = "No modules loaded."
    else:
        for module in bot.modules:
            message += f"{module.name}\n"
            message += f"Status: {bot.modules[module]}\n"
            message += f"Commands: {', '.join([command.name for command in module.commands])}\n\n"
    await update.message.reply_text(message)


@authorized
async def load(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Load a specified module."""
    try:
        module_name = update.message.text.split(" ", 1)[1].strip()
    except IndexError:
        await update.message.reply_text("Error: Module name not provided")
        return

    if module_name.lower() == "core":
        await update.message.reply_text("Error: You can't load the core module"
                                        )
        return

    bot = get_bot_context()
    if not bot:
        await update.message.reply_text("Error: Bot context not available")
        return

    for module in bot.modules:
        if module_name == module.name:
            if bot.modules[module] == "Running":
                await update.message.reply_text(
                    f"Error: Module {module_name} is already loaded")
                return
            bot.load_module(module)
            await update.message.reply_text(f"Module {module_name} loaded")
            return

    await update.message.reply_text(f"Error: Module {module_name} not found")


@authorized
async def unload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unload a specified module."""
    try:
        module_name = update.message.text.split(" ", 1)[1].strip()
    except IndexError:
        await update.message.reply_text("Error: Module name not provided")
        return

    if module_name.lower() == "core":
        await update.message.reply_text(
            "Error: You can't unload the core module")
        return

    bot = get_bot_context()
    if not bot:
        await update.message.reply_text("Error: Bot context not available")
        return

    for module in bot.modules:
        if module_name == module.name:
            if bot.modules[module] == "Disabled":
                await update.message.reply_text(
                    f"Error: Module {module_name} is already unloaded")
                return
            bot.unload_module(module)
            await update.message.reply_text(f"Module {module_name} unloaded")
            return

    await update.message.reply_text(f"Error: Module {module_name} not found")


start.handler = {"type": "command", "commands": ["start", "help"]}
modules.handler = {"type": "command", "commands": ["modules"]}
load.handler = {"type": "command", "commands": ["load"]}
unload.handler = {"type": "command", "commands": ["unload"]}

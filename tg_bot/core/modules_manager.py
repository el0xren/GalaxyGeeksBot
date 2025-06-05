from importlib import import_module
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.ext.filters import Text  # Updated import
from types import FunctionType
import inspect
from tg_bot.core.logging import LOGW, LOGE

class Command:
    """
    A class representing a tg_bot command or handler.
    """
    def __init__(self, handler, handler_type="command"):
        self.handler = handler
        self.handler_type = handler_type
        self.name = getattr(handler.callback, "__name__", str(handler))
        if not inspect.iscoroutinefunction(handler.callback):
            LOGW(
                f"Handler '{self.name}' in module is not async. All handlers must be async in python-telegram-bot v22.0.0."
            )

    def __str__(self):
        return f"{self.handler_type}:{self.name}"

class Module:
    """
    A class representing a tg_bot module.
    """
    def __init__(self, name: str, base_path: str = "tg_bot.modules"):
        self.name = name
        self.commands = []
        try:
            self.module = import_module(f"{base_path}.{self.name}", package="tg_bot")
        except ImportError as e:
            LOGE(f"Failed to import module {self.name}: {e}")
            raise

        # Check for a 'commands' list (backward compatibility)
        commands_attr = getattr(self.module, "commands", [])
        if commands_attr:
            if not isinstance(commands_attr, list):
                LOGE(f"Invalid commands format in module {self.name}: expected list, got {type(commands_attr)}")
                raise ValueError(f"Invalid commands format in module {self.name}")
            for handler in commands_attr:
                if not isinstance(handler, (CommandHandler, MessageHandler, CallbackQueryHandler)):
                    LOGE(f"Invalid handler in module {self.name}: {handler} is not a supported handler")
                    continue
                handler_type = (
                    "command" if isinstance(handler, CommandHandler) else
                    "message" if isinstance(handler, MessageHandler) else
                    "callback_query"
                )
                self.commands.append(Command(handler, handler_type))

        # Dynamically discover handlers
        for name, obj in inspect.getmembers(self.module, inspect.isfunction):
            handler_info = getattr(obj, "handler", None)
            if handler_info:
                handler_type = handler_info.get("type")
                if handler_type == "command":
                    commands = handler_info.get("commands", [])
                    if not commands:
                        LOGW(f"No commands specified for command handler {name} in module {self.name}")
                        continue
                    self.commands.append(Command(CommandHandler(commands, obj), "command"))
                elif handler_type == "message":
                    filters = handler_info.get("filters", Text())  # Updated to Text()
                    self.commands.append(Command(MessageHandler(filters, obj), "message"))
                elif handler_type == "callback_query":
                    pattern = handler_info.get("pattern", None)
                    self.commands.append(Command(CallbackQueryHandler(obj, pattern=pattern), "callback_query"))
                else:
                    LOGW(f"Unknown handler type {handler_type} for {name} in module {self.name}")
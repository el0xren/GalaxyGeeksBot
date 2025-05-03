from importlib import import_module
from telegram.ext import CommandHandler
from types import FunctionType
import inspect
from tg_bot.core.logging import LOGW, LOGE


class Command:
    """
    A class representing a tg_bot command
    """

    def __init__(self, function: FunctionType, commands: list) -> None:
        """
        Initialize the command class.
        """
        self.function = function
        self.name = self.function.__name__
        self.commands = commands

        # Check if the function is async
        if not inspect.iscoroutinefunction(function):
            LOGW(
                f"Command '{self.name}' in module is not async. All handlers must be async in python-telegram-bot v22.0.0."
            )

        # Create CommandHandler
        self.handler = CommandHandler(self.commands, self.function)


class Module:
    """
    A class representing a tg_bot module
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the module class and import its commands.
        """
        self.name = name
        try:
            self.module = import_module(f"tg_bot.modules.{self.name}",
                                        package="tg_bot")
        except ImportError as e:
            LOGE(f"Failed to import module {self.name}: {e}")
            raise

        commands_attr = getattr(self.module, "commands", [])

        if not isinstance(commands_attr, list):
            LOGE(
                f"Invalid commands format in module {self.name}: expected list, got {type(commands_attr)}"
            )
            raise ValueError(f"Invalid commands format in module {self.name}")

        self.commands = []
        for handler in commands_attr:
            if not isinstance(handler, CommandHandler):
                LOGE(
                    f"Invalid command in module {self.name}: {handler} is not a CommandHandler"
                )
                raise ValueError(
                    f"Invalid command format in module {self.name}")
            self.commands.append(Command(handler.callback, handler.commands))

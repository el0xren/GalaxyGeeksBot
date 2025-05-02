from importlib import import_module
from telegram.ext import CommandHandler
from types import FunctionType

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
		self.handler = CommandHandler(self.commands, self.function, run_async=True)

class Module:
	"""
	A class representing a tg_bot module
	"""
	def __init__(self, name: str) -> None:
		"""
		Initialize the module class and import its commands.
		"""
		self.name = name
		self.module = import_module('tg_bot.modules.' + self.name, package="*")
		self.commands = [Command(command, self.module.commands[command]) for command in self.module.commands]

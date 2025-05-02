from argparse import ArgumentParser
from telegram import Message

class CIParser(ArgumentParser):
	def set_output(self, reply_text: Message.reply_text):
		self.reply_text = reply_text

	def _print_message(self, message, file=None):
		if message:
			self.reply_text(message)

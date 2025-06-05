from telegram import Dice
from telegram import Update
from telegram.ext import ContextTypes
from contextlib import redirect_stdout
from cowsay import cow
import io

async def basket(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.BASKETBALL)


async def bowling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.BOWLING)


async def dart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.DARTS)


async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.DICE)


async def football(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.FOOTBALL)


async def slotmachine(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_dice(emoji=Dice.SLOT_MACHINE)


async def cowsay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Format text using cowsay."""
    with io.StringIO() as buf, redirect_stdout(buf):
        try:
            cow(update.effective_message.text.split(" ", 1)[1])
        except IndexError:
            await update.effective_message.reply_text(
                "Error: Write something after the command!")
        else:
            await update.effective_message.reply_text(
                f"`{buf.getvalue()}`", parse_mode=ParseMode.MARKDOWN)


basket.handler = {"type": "command", "commands": ["basket"]}
bowling.handler = {"type": "command", "commands": ["bowling"]}
dart.handler = {"type": "command", "commands": ["dart"]}
dice.handler = {"type": "command", "commands": ["dice"]}
football.handler = {"type": "command", "commands": ["football"]}
slotmachine.handler = {"type": "command", "commands": ["slotmachine"]}
cowsay.handler = {"type": "command", "commands": ["cowsay"]}

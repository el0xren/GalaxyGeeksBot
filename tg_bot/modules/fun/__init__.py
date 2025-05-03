from telegram import Dice
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


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


# Define commands as CommandHandler instances
commands = [
    CommandHandler("basket", basket),
    CommandHandler("bowling", bowling),
    CommandHandler("dart", dart),
    CommandHandler("dice", dice),
    CommandHandler("football", football),
    CommandHandler("slotmachine", slotmachine),
]

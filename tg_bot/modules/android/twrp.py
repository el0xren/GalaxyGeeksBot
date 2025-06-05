from requests import get
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bs4 import BeautifulSoup

async def twrp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the latest TWRP for a device codename."""
    device = " ".join(context.args)
    if not device:
        await update.effective_message.reply_text("Error: use /twrp codename")
        return
    link = get(f"https://eu.dl.twrp.me/{device}")
    if link.status_code == 404:
        message = f"TWRP currently is not available for {device}"
    else:
        page = BeautifulSoup(link.content, "lxml")
        download = page.find("table").find("tr").find("a")
        dl_link = f"https://eu.dl.twrp.me{download['href']}"
        dl_file = download.text
        size = page.find("span", {"class": "filesize"}).text
        date = page.find("em").text.strip()
        message = f"<b>Latest TWRP for the {device}</b>\n\n"
        message += f"• Release type: official\n"
        message += f"• Size: {size}\n"
        message += f"• Date: {date}\n"
        message += f"• File: {dl_file}\n\n"
        message += f"• <b>Download:</b> {dl_link}\n"
    await update.effective_message.reply_text(
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

twrp.handler = {"type": "command", "commands": ["twrp"]}
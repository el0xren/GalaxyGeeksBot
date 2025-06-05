# tg_bot/modules/android/orangefox.py
from requests import get
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from ujson import loads


async def orangefox(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the latest OrangeFox Recovery for a device codename."""
    device = " ".join(context.args)
    if not device:
        await update.effective_message.reply_text("Error: use /ofox codename")
        return
    link = get(
        f"https://api.orangefox.download/v3/releases/?codename={device}&sort=date_desc&limit=1"
    )
    if link.status_code == 404:
        message = f"OrangeFox currently is not available for {device}"
    else:
        page = loads(link.content)
        file_id = page["data"][0]["_id"]
        link = get(
            f"https://api.orangefox.download/v3/devices/get?codename={device}")
        page = loads(link.content)
        oem = page["oem_name"]
        model = page["model_name"]
        full_name = page["full_name"]
        link = get(
            f"https://api.orangefox.download/v3/releases/get?_id={file_id}")
        page = loads(link.content)
        dl_file = page["filename"]
        build_type = page["type"]
        version = page["version"]
        changelog = page["changelog"][0]
        size = page["size"]
        dl_link = page["mirrors"]["DL"]
        date = page["date"]
        md5 = page["md5"]
        message = f"<b>Latest OrangeFox Recovery for the {full_name}</b>\n\n"
        message += f"• Manufacturer: {oem}\n"
        message += f"• Model: {model}\n"
        message += f"• Codename: {device}\n"
        message += f"• Release type: official\n"
        message += f"• Build type: {build_type}\n"
        message += f"• Version: {version}\n"
        message += f"• Changelog: {changelog}\n"
        message += f"• Size: {size}\n"
        message += f"• Date: {date}\n"
        message += f"• File: {dl_file}\n"
        message += f"• MD5: {md5}\n\n"
        message += f"• <b>Download:</b> {dl_link}\n"
    await update.effective_message.reply_text(
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


orangefox.handler = {"type": "command", "commands": ["ofox"]}
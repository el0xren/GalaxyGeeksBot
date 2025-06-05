# tg_bot/modules/android/magisk.py
from requests import get
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def magisk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the latest Magisk releases."""
    link = "https://raw.githubusercontent.com/topjohnwu/magisk_files/"
    magisk_dict = {
        "*Stable*": "master/stable.json",
        "\n*Canary*": "canary/canary.json",
    }
    releases = "*Latest Magisk Releases:*\n\n"
    for magisk_type, release_url in magisk_dict.items():
        canary = ("https://github.com/topjohnwu/magisk_files/raw/canary/"
                  if "Canary" in magisk_type else "")
        data = get(link + release_url).json()
        releases += (
            f"{magisk_type}:\n"
            f'• Manager - [{data["app"]["version"]} ({data["app"]["versionCode"]})]({canary + data["app"]["link"]}) \n'
            f'• Uninstaller - [Uninstaller {data["magisk"]["version"]} ({data["magisk"]["versionCode"]})]({canary + data["uninstaller"]["link"]}) \n'
        )
    await update.effective_message.reply_text(
        text=releases,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


# Mark the function as a command handler
magisk.handler = {"type": "command", "commands": ["magisk", "root", "su"]}
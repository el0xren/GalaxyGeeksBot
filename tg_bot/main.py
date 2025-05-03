import asyncio
from telegram.ext import Application
from tg_bot import __version__, get_config
from tg_bot.core.bot import Bot
from tg_bot.core.logging import LOGI


async def main():
    # Get configuration
    bot_token = get_config("BOT_API_TOKEN")
    support_chat_id = int(get_config("SUPPORT_CHAT_ID"))

    # Initialize the Application
    application = Application.builder().token(bot_token).build()

    # Initialize the Bot with the Application
    bot = Bot(application)

    # Log startup information
    bot_info = await application.bot.get_me()
    LOGI(f"GalaxyGeeksBot started, version {__version__}")
    LOGI(f"Bot username: @{bot_info.username}")

    # Send startup message to support chat
    await application.bot.send_message(
        chat_id=support_chat_id,
        text=f"🤖 GalaxyGeeksBot v{__version__} has started successfully!",
        disable_web_page_preview=True,
    )

    # Start the bot and keep it running
    try:
        await bot.start()
        # Keep the bot running until interrupted
        await asyncio.Event().wait()  # Wait indefinitely
    except KeyboardInterrupt:
        # Handle graceful shutdown
        await bot.stop()
        LOGI("GalaxyGeeksBot stopped gracefully")


if __name__ == "__main__":
    asyncio.run(main())

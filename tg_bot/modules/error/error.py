from telegram.ext import ContextTypes
from telegram import Update
from telegram.error import TelegramError
from tg_bot.core.logging import LOGI, LOGE, LOGD
import asyncio

async def trigger_generic_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trigger a generic exception."""
    LOGI(f"Triggering generic error for user {update.effective_user.id}")
    raise ValueError("Test: Generic exception triggered by /test_generic")

async def trigger_telegram_error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trigger a Telegram API error by sending an invalid request."""
    LOGI(f"Triggering Telegram API error for user {update.effective_user.id}")
    LOGD(f"Sending message to invalid chat_id=999999999999")
    await context.bot.send_message(chat_id=999999999999, text="This should fail")

async def trigger_rate_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simulate rate-limit error by sending messages quickly."""
    LOGI(f"Triggering rate-limit simulation for user {update.effective_user.id}")
    for i in range(5):
        try:
            LOGD(f"Sending rate-limit test message {i+1} to chat {update.effective_chat.id}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Rate-limit test message {i+1}"
            )
            await asyncio.sleep(0.2)
        except TelegramError as e:
            LOGE(f"Rate-limit test error: {e}")
            break

async def trigger_none_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trigger an error with a None update."""
    LOGI(f"Triggering None update error for user {update.effective_user.id}")
    LOGD(f"Attempting get_chat_member with invalid chat")
    try:
        await context.bot.get_chat_member(
            chat_id=None,  # Force None to trigger error
            user_id=update.effective_user.id
        )
    except AttributeError as e:
        LOGE(f"AttributeError in get_chat_member: {e}")
        raise


trigger_generic_error.handler = {"type": "command", "commands": ["test_generic"]}
trigger_telegram_error.handler = {"type": "command", "commands": ["test_telegram"]}
trigger_rate_limit.handler = {"type": "command", "commands": ["test_ratelimit"]}
trigger_none_update.handler = {"type": "command", "commands": ["test_none"]}

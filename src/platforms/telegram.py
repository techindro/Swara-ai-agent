"""Telegram platform integration."""

from telegram import Bot
from telegram.error import TelegramError
from loguru import logger
from src.config import config


class TelegramPlatform:
    """Handles Telegram channel posting."""

    def __init__(self):
        if config.telegram.bot_token:
            self.bot = Bot(token=config.telegram.bot_token)
            self.channel_id = config.telegram.channel_id
            self.enabled = True
        else:
            self.bot = None
            self.enabled = False
            logger.warning("⚠️  Telegram not configured, skipping.")

    async def post(self, text: str) -> dict:
        """Post a message to Telegram channel."""
        if not self.enabled:
            return {"skipped": True, "reason": "not configured"}

        try:
            message = await self.bot.send_message(
                chat_id=self.channel_id,
                text=text,
                parse_mode="Markdown",
            )
            logger.success(f"✈️  Telegram message posted: {message.message_id}")
            return {"id": message.message_id, "text": text}

        except TelegramError as e:
            logger.error(f"Telegram post error: {e}")
            raise

    async def send_report(self, report_text: str) -> None:
        """Send daily report to Telegram."""
        if not self.enabled:
            return

        chunks = [report_text[i:i+4096] for i in range(0, len(report_text), 4096)]
        for chunk in chunks:
            await self.post(chunk)

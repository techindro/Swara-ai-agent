# Swara Social Media AI Agent - Main Orchestrator
# Using standard library modules + some lightweight dependencies
import asyncio
from loguru import logger
from src.config import config
from src.models.content_generator import ContentGenerator
from src.platforms.twitter import TwitterPlatform
from src.platforms.telegram import TelegramPlatform
from src.platforms.linkedin import LinkedInPlatform
from src.analytics.reporter import Reporter
from src.utils.scheduler import Scheduler
from src.utils.logger import setup_logger


class SocialMediaAgent:
    """Main agent that orchestrates all social media activities."""

    def __init__(self):
        setup_logger(config.app.log_level)
        self.content_gen = ContentGenerator()
        
        # Initializing platform handlers.
        # Note: If credentials are missing, they just log a warning and mark as disabled.
        self.twitter = TwitterPlatform()
        self.telegram = TelegramPlatform()
        self.linkedin = LinkedInPlatform()
        
        self.reporter = Reporter()
        self.scheduler = Scheduler()
        self.reply_count = 0

    async def post_daily_question(self):
        """Pick a topic and post an engaging question across the board."""
        logger.info("🚀 Preparing today's engagement question...")
        try:
            question = await self.content_gen.generate_question()
            logger.info(f"📝 Drafted: {question}")

            results = await asyncio.gather(
                self.twitter.post(question),
                self.telegram.post(question),
                self.linkedin.post(question),
                return_exceptions=True
            )

            for platform, result in zip(["Twitter", "Telegram", "LinkedIn"], results):
                if isinstance(result, Exception):
                    logger.error(f"❌ {platform} post failed: {result}")
                else:
                    logger.success(f"✅ Posted to {platform}")

        except Exception as e:
            logger.error(f"❌ Daily question failed: {e}")

    async def engage_with_audience(self):
        """Reply to mentions and comments."""
        if self.reply_count >= config.app.max_replies_per_day:
            logger.warning("⚠️  Max replies reached for today.")
            return

        logger.info("💬 Checking mentions...")
        try:
            mentions = await self.twitter.get_mentions()
            for mention in mentions:
                reply = await self.content_gen.generate_reply(mention.text)
                await self.twitter.reply(mention.id, reply)
                self.reply_count += 1
                logger.success(f"✅ Replied to @{mention.author}")
                if self.reply_count >= config.app.max_replies_per_day:
                    break
        except Exception as e:
            logger.error(f"❌ Engagement failed: {e}")

    async def generate_daily_report(self):
        """Generate and save daily analytics report."""
        logger.info("📊 Generating daily report...")
        try:
            report = await self.reporter.generate_daily_report()
            logger.success(f"✅ Report saved: {report}")
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")

    def run(self):
        """Start the agent with scheduled tasks."""
        logger.info("🤖 Social Media AI Agent starting...")

        # Schedule daily question
        self.scheduler.every_day_at(
            config.app.post_time,
            self.post_daily_question
        )

        # Schedule engagement checks
        self.scheduler.every_n_minutes(
            config.app.engagement_interval,
            self.engage_with_audience
        )

        # Schedule daily report at midnight
        self.scheduler.every_day_at("23:55", self.generate_daily_report)

        logger.info(f"⏰ Daily post scheduled at {config.app.post_time}")
        logger.info(f"💬 Engagement every {config.app.engagement_interval} min")

        self.scheduler.run_forever()


if __name__ == "__main__":
    agent = SocialMediaAgent()
    agent.run()

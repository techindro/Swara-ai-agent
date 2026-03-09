"""Configuration management for Social Media AI Agent."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class TwitterConfig:
    api_key: str = os.getenv("TWITTER_API_KEY", "")
    api_secret: str = os.getenv("TWITTER_API_SECRET", "")
    access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    access_secret: str = os.getenv("TWITTER_ACCESS_SECRET", "")
    bearer_token: str = os.getenv("TWITTER_BEARER_TOKEN", "")


@dataclass
class TelegramConfig:
    bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    channel_id: str = os.getenv("TELEGRAM_CHANNEL_ID", "")


@dataclass
class LinkedInConfig:
    client_id: str = os.getenv("LINKEDIN_CLIENT_ID", "")
    client_secret: str = os.getenv("LINKEDIN_CLIENT_SECRET", "")
    access_token: str = os.getenv("LINKEDIN_ACCESS_TOKEN", "")


@dataclass
class AIConfig:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = "gpt-4-turbo-preview"
    max_tokens: int = 280


@dataclass
class AppConfig:
    post_time: str = os.getenv("POST_TIME", "09:00")
    timezone: str = os.getenv("TIMEZONE", "Asia/Kolkata")
    engagement_interval: int = int(os.getenv("ENGAGEMENT_INTERVAL_MINUTES", "30"))
    max_replies_per_day: int = int(os.getenv("MAX_REPLIES_PER_DAY", "50"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    news_api_key: str = os.getenv("NEWS_API_KEY", "")


@dataclass
class Config:
    twitter: TwitterConfig = None
    telegram: TelegramConfig = None
    linkedin: LinkedInConfig = None
    ai: AIConfig = None
    app: AppConfig = None

    def __post_init__(self):
        self.twitter = TwitterConfig()
        self.telegram = TelegramConfig()
        self.linkedin = LinkedInConfig()
        self.ai = AIConfig()
        self.app = AppConfig()


# Global config instance
config = Config()

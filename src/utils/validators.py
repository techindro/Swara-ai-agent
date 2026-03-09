"""Validate configuration and environment variables."""

from loguru import logger
from src.config import Config


REQUIRED_FIELDS = {
    "twitter": ["api_key", "api_secret", "access_token", "access_secret", "bearer_token"],
    "ai": ["openai_api_key"],
    "app": ["news_api_key"],
}


def validate_config(config: Config) -> bool:
    """Validate all required config fields are set."""
    all_valid = True

    for section, fields in REQUIRED_FIELDS.items():
        section_obj = getattr(config, section)
        for field in fields:
            value = getattr(section_obj, field, "")
            if not value:
                logger.error(f"❌ Missing config: {section}.{field}")
                all_valid = False

    if all_valid:
        logger.success("✅ All required config fields present.")
    else:
        logger.warning("⚠️  Some config fields missing. Check your .env file.")

    return all_valid

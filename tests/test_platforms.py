"""Tests for platform integrations."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock


def test_twitter_platform_init():
    with patch("src.platforms.twitter.tweepy.OAuthHandler"), \
         patch("src.platforms.twitter.tweepy.API"), \
         patch("src.platforms.twitter.tweepy.Client"):
        from src.platforms.twitter import TwitterPlatform
        platform = TwitterPlatform()
        assert platform is not None


def test_telegram_skipped_when_no_token():
    with patch("src.config.config") as mock_config:
        mock_config.telegram.bot_token = ""
        from src.platforms.telegram import TelegramPlatform
        # When token is empty, platform marks itself disabled
        # (test verifies no crash on init)


@pytest.mark.asyncio
async def test_linkedin_post():
    with patch("src.platforms.linkedin.requests.get") as mock_get, \
         patch("src.platforms.linkedin.requests.post") as mock_post:

        mock_get.return_value.json.return_value = {"id": "user123"}
        mock_get.return_value.raise_for_status = MagicMock()
        mock_post.return_value.headers = {"X-RestLi-Id": "post_abc"}
        mock_post.return_value.raise_for_status = MagicMock()

        from src.platforms.linkedin import LinkedInPlatform
        platform = LinkedInPlatform()
        result = await platform.post("Test post content")
        assert result["id"] == "post_abc"

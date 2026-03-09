"""Tests for the main agent."""

import pytest
from unittest.mock import AsyncMock, patch
from src.agent import SocialMediaAgent


@pytest.fixture
def agent():
    with patch("src.agent.TwitterPlatform"), \
         patch("src.agent.TelegramPlatform"), \
         patch("src.agent.LinkedInPlatform"), \
         patch("src.agent.ContentGenerator"), \
         patch("src.agent.Reporter"):
        return SocialMediaAgent()


@pytest.mark.asyncio
async def test_post_daily_question(agent):
    agent.content_gen.generate_question = AsyncMock(
        return_value="🧠 Will AI replace programmers? #AI"
    )
    agent.twitter.post = AsyncMock(return_value={"id": "123"})
    agent.telegram.post = AsyncMock(return_value={"id": 1})
    agent.linkedin.post = AsyncMock(return_value={"id": "li_123"})

    await agent.post_daily_question()

    agent.content_gen.generate_question.assert_called_once()
    agent.twitter.post.assert_called_once()


@pytest.mark.asyncio
async def test_max_replies_limit(agent):
    agent.reply_count = 50  # Already at max
    agent.twitter.get_mentions = AsyncMock()

    await agent.engage_with_audience()

    agent.twitter.get_mentions.assert_not_called()

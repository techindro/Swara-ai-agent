"""Tests for content generator."""

import pytest
from unittest.mock import AsyncMock, patch
from src.models.content_generator import ContentGenerator


@pytest.fixture
def generator():
    with patch("src.models.content_generator.AIModel"), \
         patch("src.models.content_generator.NewsApiClient"):
        return ContentGenerator()


@pytest.mark.asyncio
async def test_generate_question(generator):
    generator.ai.generate = AsyncMock(
        return_value="🧠 What's your take on AGI? #AI #ArtificialIntelligence"
    )
    generator._get_news_context = AsyncMock(return_value="")

    result = await generator.generate_question()

    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_generate_reply(generator):
    generator.ai.generate = AsyncMock(
        return_value="Great point! What do you think about safety measures?"
    )

    result = await generator.generate_reply("AI is going to take over!")

    assert isinstance(result, str)
    generator.ai.generate.assert_called_once()


def test_topic_rotation(generator):
    topics_seen = set()
    for _ in range(4):
        topics_seen.add(generator._get_next_topic())
    assert len(topics_seen) == 4

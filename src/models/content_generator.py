# Content generation engine. 
# Pulls news context from NewsAPI to make the AI questions relevant.
import json
import random
from pathlib import Path
from loguru import logger
from newsapi import NewsApiClient
from src.models.ai_models import AIModel
from src.config import config

TOPICS = ["Artificial Intelligence", "Robotics", "Space Exploration", "Climate Change"]

TOPIC_EMOJIS = {
    "Artificial Intelligence": "🧠",
    "Robotics": "🦾",
    "Space Exploration": "🚀",
    "Climate Change": "🌍",
}


class ContentGenerator:
    """Core logic for generating posts, threads, and replies."""

    def __init__(self):
        self.ai = AIModel()
        self.news_client = NewsApiClient(api_key=config.app.news_api_key)
        self.topic_index = 0
        self._load_question_templates()

    def _load_question_templates(self):
        templates_path = Path("src/data/questions.json")
        if templates_path.exists():
            with open(templates_path, encoding='utf-8') as f:
                self.templates = json.load(f)
        else:
            self.templates = {}

    def _get_next_topic(self) -> str:
        topic = TOPICS[self.topic_index % len(TOPICS)]
        self.topic_index += 1
        return topic

    async def _get_news_context(self, topic: str) -> str:
        try:
            news = self.news_client.get_top_headlines(
                q=topic, language="en", page_size=3
            )
            headlines = [
                a["title"]
                for a in news.get("articles", [])
                if a.get("title")
            ]
            return " | ".join(headlines[:2]) if headlines else ""
        except Exception as e:
            logger.warning(f"News fetch skipped or failed: {e}")
            return ""

    async def generate_question(self) -> str:
        """Generate a thought-provoking daily question."""
        topic = self._get_next_topic()
        emoji = TOPIC_EMOJIS.get(topic, "💡")
        news_context = await self._get_news_context(topic)

        prompt = f"""Create an engaging Twitter question about {topic}.
{f'Recent news context: {news_context}' if news_context else ''}

Requirements:
- Start with {emoji}
- Under 240 characters
- End with relevant hashtags like #{topic.replace(' ', '')}
- Thought-provoking, invites discussion
- Do NOT use quotes around the question"""

        return await self.ai.generate(prompt, max_tokens=100)

    async def generate_reply(self, mention_text: str) -> str:
        """Generate a context-aware reply to a mention."""
        prompt = f"""Someone replied to our social media post:
"{mention_text}"

Write a friendly, engaging reply (under 240 chars) that:
- Acknowledges their point
- Adds value or asks a follow-up
- Stays on topic (AI/Robotics/Space/Climate)
- Is conversational and warm"""

        return await self.ai.generate(prompt, max_tokens=100)

    async def generate_thread(self, topic: str, num_tweets: int = 5) -> list[str]:
        """Generate a Twitter thread on a topic."""
        prompt = f"""Create a {num_tweets}-tweet Twitter thread about {topic}.
Format: Return each tweet on a new line starting with the tweet number.
Example:
1/ Introduction tweet here...
2/ Second point here...
Each tweet must be under 270 chars."""

        content = await self.ai.generate(prompt, max_tokens=800)
        tweets = [
            line.split("/", 1)[1].strip()
            for line in content.split("\n")
            if "/" in line and line[0].isdigit()
        ]
        return tweets[:num_tweets]

"""Twitter/X platform integration using Tweepy."""

import tweepy
from dataclasses import dataclass
from loguru import logger
from src.config import config


@dataclass
class Mention:
    id: str
    text: str
    author: str


class TwitterPlatform:
    """Handles all Twitter/X API interactions."""

    def __init__(self):
        auth = tweepy.OAuthHandler(
            config.twitter.api_key,
            config.twitter.api_secret
        )
        auth.set_access_token(
            config.twitter.access_token,
            config.twitter.access_secret
        )
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.client = tweepy.Client(
            bearer_token=config.twitter.bearer_token,
            consumer_key=config.twitter.api_key,
            consumer_secret=config.twitter.api_secret,
            access_token=config.twitter.access_token,
            access_token_secret=config.twitter.access_secret,
            wait_on_rate_limit=True,
        )
        self._last_mention_id = None

    async def post(self, text: str) -> dict:
        """Post a tweet."""
        try:
            response = self.client.create_tweet(text=text)
            tweet_id = response.data["id"]
            logger.success(f"🐦 Tweet posted: {tweet_id}")
            return {"id": tweet_id, "text": text}
        except tweepy.TweepyException as e:
            logger.error(f"Twitter post error: {e}")
            raise

    async def get_mentions(self) -> list[Mention]:
        """Fetch recent mentions."""
        try:
            me = self.client.get_me()
            user_id = me.data.id

            kwargs = {"expansions": ["author_id"]}
            if self._last_mention_id:
                kwargs["since_id"] = self._last_mention_id

            response = self.client.get_users_mentions(user_id, **kwargs)

            if not response.data:
                return []

            mentions = []
            users = {u.id: u.username for u in (response.includes.get("users") or [])}

            for tweet in response.data:
                mentions.append(
                    Mention(
                        id=tweet.id,
                        text=tweet.text,
                        author=users.get(tweet.author_id, "unknown"),
                    )
                )

            self._last_mention_id = response.data[0].id
            logger.info(f"📬 Found {len(mentions)} new mentions")
            return mentions

        except tweepy.TweepyException as e:
            logger.error(f"Mentions fetch error: {e}")
            return []

    async def reply(self, tweet_id: str, text: str) -> dict:
        """Reply to a tweet."""
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=tweet_id
            )
            logger.success(f"💬 Replied to tweet {tweet_id}")
            return response.data
        except tweepy.TweepyException as e:
            logger.error(f"Reply error: {e}")
            raise

    async def post_thread(self, tweets: list[str]) -> list[dict]:
        """Post a Twitter thread."""
        posted = []
        reply_to = None

        for tweet in tweets:
            try:
                kwargs = {"text": tweet}
                if reply_to:
                    kwargs["in_reply_to_tweet_id"] = reply_to

                response = self.client.create_tweet(**kwargs)
                tweet_id = response.data["id"]
                reply_to = tweet_id
                posted.append({"id": tweet_id, "text": tweet})
                logger.success(f"🧵 Thread tweet posted: {tweet_id}")

            except tweepy.TweepyException as e:
                logger.error(f"Thread tweet failed: {e}")
                break

        return posted

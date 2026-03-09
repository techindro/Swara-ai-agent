"""LinkedIn platform integration."""

import requests
from loguru import logger
from src.config import config


class LinkedInPlatform:
    """Handles LinkedIn post creation via API."""

    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self):
        self.access_token = config.linkedin.access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }
        self._person_id = None

    def _get_person_id(self) -> str:
        if self._person_id:
            return self._person_id

        response = requests.get(f"{self.BASE_URL}/me", headers=self.headers)
        response.raise_for_status()
        self._person_id = response.json()["id"]
        return self._person_id

    async def post(self, text: str) -> dict:
        """Create a LinkedIn post."""
        try:
            person_id = self._get_person_id()

            payload = {
                "author": f"urn:li:person:{person_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                },
            }

            response = requests.post(
                f"{self.BASE_URL}/ugcPosts",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()

            post_id = response.headers.get("X-RestLi-Id", "unknown")
            logger.success(f"💼 LinkedIn post created: {post_id}")
            return {"id": post_id, "text": text}

        except requests.RequestException as e:
            logger.error(f"LinkedIn post error: {e}")
            raise

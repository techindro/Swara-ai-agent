"""Analyze and categorize audience responses."""

import re
from collections import Counter
from dataclasses import dataclass, field
from loguru import logger
from src.analytics.sentiment import SentimentAnalyzer

TOPIC_KEYWORDS = {
    "AI": ["ai", "artificial intelligence", "machine learning", "gpt", "llm", "neural"],
    "Robotics": ["robot", "automation", "mechanical", "drone", "autonomous"],
    "Space": ["space", "nasa", "mars", "rocket", "satellite", "astronaut", "moon"],
    "Climate": ["climate", "carbon", "emission", "renewable", "solar", "green"],
}


@dataclass
class AnalyzedResponse:
    text: str
    topics: list[str] = field(default_factory=list)
    sentiment: str = "neutral"
    compound_score: float = 0.0
    is_question: bool = False
    word_count: int = 0


class ResponseAnalyzer:
    """Categorizes and analyzes audience responses."""

    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()

    def _detect_topics(self, text: str) -> list[str]:
        text_lower = text.lower()
        detected = []
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                detected.append(topic)
        return detected or ["General"]

    def _is_question(self, text: str) -> bool:
        return bool(re.search(r"\?|^(what|how|why|when|who|where|can|do|is|are)\b", 
                               text.lower()))

    def analyze(self, text: str) -> AnalyzedResponse:
        sentiment = self.sentiment_analyzer.analyze(text)
        return AnalyzedResponse(
            text=text,
            topics=self._detect_topics(text),
            sentiment=sentiment.label,
            compound_score=sentiment.compound,
            is_question=self._is_question(text),
            word_count=len(text.split()),
        )

    def analyze_batch(self, texts: list[str]) -> list[AnalyzedResponse]:
        return [self.analyze(t) for t in texts]

    def get_top_topics(self, responses: list[AnalyzedResponse], top_n: int = 5) -> list:
        all_topics = [t for r in responses for t in r.topics]
        return Counter(all_topics).most_common(top_n)

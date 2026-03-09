"""Sentiment analysis for social media responses."""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from dataclasses import dataclass
from loguru import logger


@dataclass
class SentimentResult:
    text: str
    compound: float      # -1.0 to 1.0
    positive: float
    negative: float
    neutral: float
    label: str           # "positive" | "negative" | "neutral"
    subjectivity: float  # 0.0 to 1.0


class SentimentAnalyzer:
    """Combines VADER + TextBlob for robust sentiment analysis."""

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> SentimentResult:
        """Analyze sentiment of a single text."""
        vader_scores = self.vader.polarity_scores(text)
        blob = TextBlob(text)

        compound = vader_scores["compound"]
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"

        return SentimentResult(
            text=text,
            compound=compound,
            positive=vader_scores["pos"],
            negative=vader_scores["neg"],
            neutral=vader_scores["neu"],
            label=label,
            subjectivity=blob.sentiment.subjectivity,
        )

    def analyze_batch(self, texts: list[str]) -> list[SentimentResult]:
        """Analyze a list of texts."""
        return [self.analyze(t) for t in texts]

    def aggregate(self, results: list[SentimentResult]) -> dict:
        """Aggregate sentiment across multiple results."""
        if not results:
            return {}

        total = len(results)
        positive = sum(1 for r in results if r.label == "positive")
        negative = sum(1 for r in results if r.label == "negative")
        neutral = total - positive - negative
        avg_compound = sum(r.compound for r in results) / total

        return {
            "total": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_pct": round(positive / total * 100, 1),
            "negative_pct": round(negative / total * 100, 1),
            "neutral_pct": round(neutral / total * 100, 1),
            "avg_compound": round(avg_compound, 4),
            "overall": "positive" if avg_compound > 0.05 else
                       "negative" if avg_compound < -0.05 else "neutral",
        }

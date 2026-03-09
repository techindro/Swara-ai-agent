"""Generates daily/weekly analytics reports."""

import json
import pandas as pd
from datetime import datetime, date
from pathlib import Path
from loguru import logger
from src.analytics.sentiment import SentimentAnalyzer
from src.analytics.response_analyzer import ResponseAnalyzer


REPORTS_DIR = Path("data/reports")
RESPONSES_DIR = Path("data/responses")


class Reporter:
    """Generates and saves analytics reports."""

    def __init__(self):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        self.sentiment = SentimentAnalyzer()
        self.analyzer = ResponseAnalyzer()

    async def generate_daily_report(self) -> str:
        """Generate today's report and save as JSON + CSV."""
        today = date.today().isoformat()
        logger.info(f"📊 Generating report for {today}")

        responses = self._load_todays_responses()

        if not responses:
            logger.warning("No responses found for today.")
            return ""

        analyzed = self.analyzer.analyze_batch(responses)
        sentiments = self.sentiment.analyze_batch(responses)
        aggregated = self.sentiment.aggregate(sentiments)
        top_topics = self.analyzer.get_top_topics(analyzed)

        report = {
            "date": today,
            "total_responses": len(responses),
            "sentiment": aggregated,
            "top_topics": top_topics,
            "questions_received": sum(1 for r in analyzed if r.is_question),
            "avg_word_count": round(
                sum(r.word_count for r in analyzed) / len(analyzed), 1
            ),
        }

        # Save JSON
        json_path = REPORTS_DIR / f"report_{today}.json"
        with open(json_path, "w") as f:
            json.dump(report, f, indent=2)

        # Save CSV
        csv_path = REPORTS_DIR / f"report_{today}.csv"
        df = pd.DataFrame([{
            "text": r.text,
            "topics": ",".join(r.topics),
            "sentiment": r.sentiment,
            "score": r.compound_score,
            "is_question": r.is_question,
        } for r in analyzed])
        df.to_csv(csv_path, index=False)

        logger.success(f"✅ Report saved: {json_path}")
        return str(json_path)

    def _load_todays_responses(self) -> list[str]:
        today = date.today().isoformat()
        response_file = RESPONSES_DIR / f"responses_{today}.json"

        if not response_file.exists():
            return []

        with open(response_file) as f:
            data = json.load(f)

        return [item.get("text", "") for item in data if item.get("text")]

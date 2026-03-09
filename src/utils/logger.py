"""Logging configuration using Loguru."""

import sys
from pathlib import Path
from loguru import logger

LOGS_DIR = Path("data/logs")


def setup_logger(level: str = "INFO") -> None:
    """Configure Loguru logger with file and console handlers."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()

    # Console handler — colorful
    logger.add(
        sys.stderr,
        level=level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> — "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # File handler — rotating daily
    logger.add(
        LOGS_DIR / "agent_{time:YYYY-MM-DD}.log",
        level="DEBUG",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} — {message}",
    )

    logger.info(f"Logger initialized at level: {level}")

import sys
from datetime import date

from loguru import logger

from src.settings import Settings


def configure_logging() -> None:
    """Call in entry scripts to configure logger"""
    settings = Settings()
    log_file = settings.log_dir / f"cli-{date.today()}.log"

    config = {
        "handlers": [
            {"sink": sys.stderr},
            {"sink": str(log_file)},
        ]
    }
    logger.configure(**config)


def log_command() -> None:
    """Log the command passed to the CLI"""
    logger.info(" ".join(sys.argv))

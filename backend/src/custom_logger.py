import datetime
import logging

import pytz


def setup_logger(timezone="UTC") -> logging.Logger:
    """
    Set up a custom logger with regional time.

    Args:
        timezone (str): The timezone to use for logging timestamps. Defaults to "UTC".
    """

    # Create a custom logger
    logger = logging.getLogger("Scheduler")
    logger.setLevel(logging.INFO)

    # Define log format with regional time
    log_format = logging.Formatter(
        "%(asctime)s %(name)s [%(levelname)s]: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Timezone
    tz = pytz.timezone(timezone)
    log_format.converter = lambda _: datetime.datetime.now(tz).timetuple()

    # Add console handler
    handler = logging.StreamHandler()

    handler.setFormatter(log_format)
    logger.addHandler(handler)

    return logger


# 他スクリプトで読み込むためのlogger
logger = setup_logger(
    timezone="Japan",
)

import logging
import sys

from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl, BaseSettings

from pathlib import Path
import my_app

PACKAGE_ROOT = Path(my_app.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
LOGS_DIR = ROOT / "logs"

class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'

    logging: LoggingSettings = LoggingSettings()

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        'http://localhost:3400',
        'http://localhost:8400',
        'https://localhost:3400',
        'https://localhost:8400',
    ]

    PROJECT_NAME: str = 'Spaceship Titanic API'

    class Config:
        case_sensitive = True

class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )

def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application"""

    LOGGERS = ('uvicorn.asgi', 'uvicorn.access')
    logging.getLogger().handlers = [InterceptHandler()]

    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    logger.configure(
        handlers=[{'sink':sys.stderr, 'level': config.logging.LOGGING_LEVEL}]
    )

settings = Settings()
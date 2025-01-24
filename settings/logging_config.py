import logging
from logging.config import dictConfig

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(levelname)s %(asctime)s - %(name)s - %(message)s",
        },
        "aiogram": {
            "format": "%(levelname)s %(asctime)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "myapp": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "aiogram": {
            "level": "INFO",  # Уровень логирования для aiogram
            "handlers": ["console"],
            "propagate": False,
        },
        "aiogram.bot": {
            "level": "DEBUG",  # Уровень логирования для aiogram.bot
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

dictConfig(logging_config)

# Логгер для вашего приложения
logger = logging.getLogger("hatikotask")

# Логгер для aiogram
aiogram_logger = logging.getLogger("aiogram")
bot_logger = logging.getLogger("aiogram.bot")
import logging as _logging

from .settings import settings

from typing import ClassVar

class LogFormatter(_logging.Formatter):
    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[35m",
        "INFO": "\033[36m",
        "WARNING": "\033[93m",
        "ERROR": "\033[31m",
    }

    RESET = "\033[0m"

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, self.RESET)
        return f"{color}{log_message}{self.RESET}"


def get_logger(debug: bool = False) -> _logging.Logger:
    logger = _logging.getLogger()
    level = _logging.DEBUG if debug else _logging.INFO
    logger.setLevel(level)

    if not logger.handlers:
        console_handler = _logging.StreamHandler()
        console_handler.setLevel(level)

        console_formatter = LogFormatter(
            "%(asctime)s | %(levelname)-8s | %(process)d | %(threadName)s | %(name)s | %(module)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger

logger = get_logger(debug=settings.DEBUG)
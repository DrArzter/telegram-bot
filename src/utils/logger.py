import logging
import sys

LEVEL_EMOJI: dict[str, str] = {
    "DEBUG": "🐛",
    "INFO": "ℹ️",
    "WARNING": "⚠️",
    "ERROR": "❌",
    "CRITICAL": "🔥",
}


class FixedFormatter(logging.Formatter):
    def format(self, record) -> str:
        """
        Format the given record into a string.

        This formatter adds the following fields to the record:

        - emoji: the emoji corresponding to the log level
        - shortname: the last two parts of the logger name, truncated to 15 characters
        - levelname: the log level name, padded to 8 characters

        Then it calls the parent's format method with the modified record.
        """
        record.emoji = LEVEL_EMOJI.get(record.levelname, "")
        parts = record.name.split(".")
        short = ".".join(parts[-2:])
        record.shortname = (short[:12] + "...") if len(short) > 15 else short.ljust(15)
        record.levelname = f"{record.levelname:<8}"
        return super().format(record)


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Returns a logger with the given name.

    If the logger does not have any handlers, sets up a handler with a
    StreamHandler, a FixedFormatter, and sets the log level to INFO.

    :param name: The name of the logger.
    :type name: str
    :return: A logger with the given name.
    :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler(sys.stdout)
        formatter = FixedFormatter(
            "%(asctime)s | %(emoji)s %(levelname)s | %(shortname)s | %(message)s",
            datefmt="%H:%M",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

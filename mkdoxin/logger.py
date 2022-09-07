#!/usr/bin/env python3
import logging
import textwrap
from shutil import get_terminal_size

from termcolor import colored


class DuplicateFilter:
    """Avoid logging duplicate messages."""

    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv


class ColorFormatter(logging.Formatter):
    colors = {
        "CRITICAL": "red",
        "ERROR": "red",
        "WARNING": "yellow",
        "DEBUG": "blue",
    }

    message_color = {
        "CRITICAL": "grey",
        "ERROR": "grey",
        "WARNING": "grey",
        "DEBUG": "white",
        "INFO": "blue",
    }

    text_wrapper = textwrap.TextWrapper(
        width=get_terminal_size(fallback=(0, 0)).columns,
        replace_whitespace=False,
        break_long_words=False,
        break_on_hyphens=False,
        initial_indent=" " * 12,
        subsequent_indent=" " * 12,
    )

    def format(self, record):
        message = super().format(record)
        prefix = f"{record.levelname:<8} -  "
        msg_color = self.message_color[record.levelname]
        if record.levelname in self.colors:
            prefix = colored(prefix, self.colors[record.levelname])
        if self.text_wrapper.width:
            # Only wrap text if a terminal width was detected
            msg = "\n".join(
                self.text_wrapper.fill(line) for line in message.splitlines()
            )
            # Prepend prefix after wrapping so that color codes don't affect length
            return prefix + colored(msg[12:], msg_color)
        return prefix + colored(message, msg_color)


def logger(name: str, level: str = logging.INFO):
    """Wraps and formats logging to match a similar style to MkDocs."""

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(name)

    # Don't restrict level on logger; use handler
    logger.setLevel(1)
    logger.propagate = False

    stream = logging.StreamHandler()
    stream.setFormatter(ColorFormatter())
    stream.setLevel(level)
    stream.name = "MkDoxinStreamHandler"
    logger.addHandler(stream)

    return logger

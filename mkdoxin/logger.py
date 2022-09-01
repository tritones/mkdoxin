#!/usr/bin/env python3

import logging


class DuplicateFilter:
    """Avoid logging duplicate messages."""

    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv


def logger(name):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(name)
    # log = logging.getLogger('mkdocs')
    # log.addFilter(DuplicateFilter())
    # log.setLevel(logging.INFO)

    return logger

#!/usr/bin/env python3
import os

from logger import logger

log = logger(__name__)


def _open_config_file(config_file):
    """ """

    # Default to the standard config filename.
    if config_file is None:
        paths_to_try = ["mkdoxin.yml", "mkdoxin.yaml"]
    # If it is a string, we can assume it is a path and attempt to open it.
    elif isinstance(config_file, str):
        paths_to_try = [config_file]
    else:
        raise f"Config file '{config_file}' must be a string."
    for path in paths_to_try:
        path = os.path.abspath(path)
        log.debug(f"Loading configuration file: {path}")
        try:
            result_config_file = open(path, "rb")
            break
        except:
            raise ValueError()
    else:
        raise ValueError(f"Config file '{paths_to_try[0]}' does not exist.")

    try:
        yield result_config_file
    finally:
        if hasattr(result_config_file, "close"):
            result_config_file.close()


def load_config(config_file: str = None):
    with _open_config_file(config_file) as fd:
        config_file_path = getattr(fd, "name", "")

        # Initialize the config with the default schema.
        # from mkdocs.config import defaults

        cfg = None
        # load the config file
        # cfg.load_file(fd)

    return cfg

#!/usr/bin/env python3

from logger import logger
import os
from shutil import rmtree
import subprocess
from time import time

log = logger(__name__)


def build(source_dir: str, build_dir: str):
    """
    Builds the docs using mkdocs. Expects a source and a destination (build) directory.
    """
    log.info("Running mkdocs...")
    os.system(f'mkdocs build -f "{source_dir}/mkdocs.yml" -d "{build_dir}"')


def install_python_dependencies(path: str):
    """ """
    start = time()

    log.info("Installing dependencies...")
    command = ["python3", "-m", "pip", "install", "-q", "-r", path]
    subprocess.Popen(command, shell=False).wait()
    log.info("Dependencies installed in %.2f seconds", time() - start)


def remove_local_repo(source_dir):
    """ """
    log.info("Removing local repository...")

    for files in os.listdir(source_dir):
        path = os.path.join(source_dir, files)
        try:
            rmtree(path)
        except OSError:
            os.remove(path)
    log.info(f"Local repository removed from {source_dir}")

#!/usr/bin/env python3
from os import environ
from time import time

from gitutils import parse_repository
from logger import logger
from repo_manager import *
from scheduler import scheduler
from server import serve

log = logger(__name__)

git_repo = environ.get("GIT_REPO")
# Max Size defaults to 1GB
one_GB_in_KB = 10**6
max_repo_size = environ.get("MAX_REPO_SIZE", one_GB_in_KB)
localize_site_url = environ.get("LOCALIZE_SITE_URL", True)
optimize_images = environ.get("OPTIMIZE_IMAGES", False)
clear_repo_before_clone = environ.get("CLEAR_REPO_BEFORE_CLONE", True)
scheduled_updates = environ.get("SCHEDULED_UPDATES", True)
update_interval = environ.get("UPDATE_INTERVAL", 1)
update_cadence = environ.get("UPDATE_CADENCE", "days")


def main():
    start = time()

    build_base_dir = "/docs/site"
    build_dir = f"{build_base_dir}/build"

    log.info("\n-------------------------------------")
    log.info("-------------------------------------")
    log.info("Starting MkDoxin")
    log.info("-------------------------------------")
    log.info("-------------------------------------")

    parsed_repo = parse_repository(git_repo)

    if not parsed_repo.valid:
        log.error(f"Invalid repository URL! {git_repo}")
        return

    normalized_repo = parsed_repo.normalized

    log.info(f"Remote Docs Repository: {normalized_repo}")
    log.info("-------------------------------------\n")

    repo_manager_arguments = {
        "normalized_repo": normalized_repo,
        "max_repo_size": max_repo_size,
        "clear_repo_before_clone": clear_repo_before_clone,
        "localize_site_url": localize_site_url,
    }

    if not scheduled_updates:
        rpm(**repo_manager_arguments)
    else:
        runner = scheduler(
            rpm,
            repo_manager_arguments,
            interval=update_interval,
            cadence=update_cadence,
            run_on_start=True,
        )

    log.info("Initialization completed in %.2f seconds", time() - start)
    serve(build_dir)


if __name__ == "__main__":
    main()

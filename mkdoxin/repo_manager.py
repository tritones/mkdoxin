#!/usr/bin/env python3
import os
import subprocess
from shutil import rmtree
from time import time

import gitutils
import utils
from localize_site_urls import localize_site_urls
from logger import logger

log = logger(__name__)

source_dir = "/docs/source"
build_base_dir = "/docs/site"
build_dir = f"{build_base_dir}/build"
version_file = f"{build_base_dir}/version/current_version.txt"


def rpm(
    normalized_repo, max_repo_size, clear_repo_before_clone, localize_site_url
):

    start = time()

    log.info("Checking for documentation / updates...")

    remote_git_commit = gitutils.get_remote_git_commit(normalized_repo)
    file_commit = gitutils.get_commit_version_file(version_file)

    is_version_current = gitutils.is_commit_version_current(
        file_commit, remote_git_commit
    )

    if not is_version_current:
        log.info("GIT Repository current commit differs than local:")
        log.info(
            f"Local commit: {file_commit} - Remote commit: {remote_git_commit}"
        )

        repo_size = gitutils.get_remote_git_size(normalized_repo)
        repo_size_converted = gitutils.convert_repo_size_to_MB(repo_size)

        log.info(f"GIT Repository Size: {repo_size_converted}")

        repo_size_allowed = gitutils.repo_size_is_allowed(
            repo_size, max_repo_size
        )
        max_repo_size_converted = gitutils.convert_repo_size_to_MB(
            max_repo_size
        )

        if not repo_size_allowed:
            log.error(
                "Repo Size is larger than the max allowed (Repo:"
                f" {repo_size_converted}, Max: {max_repo_size_converted})"
            )
            return

        if clear_repo_before_clone:
            utils.remove_local_repo(source_dir)

        gitutils.clone_repo(normalized_repo, source_dir)
        utils.install_python_dependencies("/docs/source/docs/requirements.txt")

        if localize_site_url:
            log.info(f"Localizing site URL references...")
            localize_site_urls("/docs/source/mkdocs.yml")

        utils.build(source_dir, build_dir)

        local_git_commit = gitutils.get_local_git_commit(source_dir)
        gitutils.set_commit_version_file(version_file, local_git_commit)
        log.info(
            "GIT Repository local commit has been updated to:"
            f" {local_git_commit}"
        )

        utils.remove_local_repo(source_dir)
    else:
        log.info(f"GIT Repository current commit matches local: {file_commit}")

    log.info("Documentation prepared in %.2f seconds", time() - start)

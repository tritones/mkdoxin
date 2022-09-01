#!/usr/bin/env python3

import gitutils
from localize_site_urls import localize_site_urls
from logger import logger
import os
from shutil import rmtree
import subprocess
from time import time

log = logger(__name__)

source_dir = "/docs/source"
build_base_dir = "/docs/site"
build_dir = f"{build_base_dir}/build"
version_file = f"{build_base_dir}/version/current_version.txt"


def build(source_dir: str, build_dir: str):
    """
    Builds the docs using mkdocs. Expects a source and a destination (build) directory.
    """
    log.info("Running mkdocs...")
    os.system(f'mkdocs build -f "{source_dir}/mkdocs.yml" -d "{build_dir}"')


def install_python_dependencies(path):
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


def rpm(
    normalized_repo, max_repo_size, clear_repo_before_clone, localize_site_url
):

    remote_git_commit = gitutils.get_remote_git_commit(normalized_repo)
    file_commit = gitutils.get_commit_version_file(version_file)

    is_version_current = gitutils.is_commit_version_current(
        file_commit, remote_git_commit
    )

    if not is_version_current:
        log.info(f"GIT Repository current commit differs than local:")
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
            remove_local_repo(source_dir)

        gitutils.clone_repo(normalized_repo, source_dir)
        install_python_dependencies("/docs/source/docs/requirements.txt")

        if localize_site_url:
            log.info(f"Localizing site URL references...")
            localize_site_urls("/docs/source/mkdocs.yml")

        build(source_dir, build_dir)

        local_git_commit = gitutils.get_local_git_commit(source_dir)
        gitutils.set_commit_version_file(version_file, local_git_commit)
        log.info(
            "GIT Repository local commit has been updated to:"
            f" {local_git_commit}"
        )

        remove_local_repo(source_dir)
    else:
        log.info(f"GIT Repository current commit matches local: {file_commit}")

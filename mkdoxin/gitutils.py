#!/usr/bin/env python3

from giturlparse import parse
from logger import logger
import os
from re import match
from requests import get as req_get
import subprocess
from time import time

log = logger(__name__)


def parse_repository(repository_url):
    """ """
    parsed_repo = parse(repository_url)

    return parsed_repo


def get_local_git_commit(directory):
    """ """
    log.debug("Getting local git commit...")
    command = ["git", "-C", directory, "rev-parse", "HEAD"]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)
    commit_hash = subprocess.check_output(("cut", "-f1"), stdin=ps.stdout)
    ps.wait()

    return commit_hash.decode().strip()


def get_commit_version_file(file):
    """ """
    if not os.path.exists(file):
        return None

    with open(file, "r") as f:
        file_contents = f.read()
        commit = match(r"Commit Hash: (?P<commit>\w{40})", file_contents)
        f.close()

    if commit is None:
        return commit
    else:
        return commit.group("commit")


def set_commit_version_file(file, commit):
    """ """
    contents = f"Commit Hash: {commit}"

    with open(file, "w") as f:
        f.write(contents)
        f.close()


def get_remote_git_size(normalized_repo):
    """ """
    parsed_repo = parse_repository(normalized_repo)

    is_github = parsed_repo.platform == "github"

    if not is_github:
        log.warn(
            "Repository is not hosted on GitHub; unable to determine the size"
        )
        return False
    else:
        url = f"https://api.github.com/repos/{parsed_repo.owner}/{parsed_repo.repo}"
        response = req_get(url)
        response_json = response.json()

        return response_json["size"]


def convert_repo_size_to_MB(size):
    """Expects an integer of size in KB, converts to readable size in MB."""
    converted_size = size / 1000
    return f"{converted_size:.1f}MB"


def repo_size_is_allowed(repo_size, max_size):
    """ """
    return repo_size <= max_size


def get_remote_git_commit(git_repo):
    """ """
    command = ["git", "ls-remote", git_repo, "HEAD"]
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)
    commit_hash = subprocess.check_output(("cut", "-f1"), stdin=ps.stdout)
    ps.wait()

    return commit_hash.decode().strip()


def is_commit_version_current(local_commit, remote_commit):
    """ """
    if local_commit is None:
        return False
    else:
        return local_commit == remote_commit


def clone_repo(git_repo, source_dir):
    """ """
    start = time()

    log.info(f"Cloning GIT Repository to {source_dir}...")
    command = ["git", "clone", git_repo, source_dir, "-q"]
    subprocess.Popen(command, shell=False).wait()
    log.info("GIT Repository cloned in %.2f seconds", time() - start)

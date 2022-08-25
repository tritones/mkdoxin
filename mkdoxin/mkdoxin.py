#!/usr/bin/env python3

from localize_site_urls import localize_site_urls

from giturlparse import parse
from http.server import HTTPServer, CGIHTTPRequestHandler
import logging
import os
import shutil
import re
import requests
import subprocess
from time import time


class DuplicateFilter:
    """Avoid logging duplicate messages."""

    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv


logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)
# log = logging.getLogger('mkdocs')
# log.addFilter(DuplicateFilter())
# log.setLevel(logging.INFO)

git_repo = os.environ.get("GIT_REPO")
# Max Size defaults to 1GB
one_GB_in_KB = 10**6
max_repo_size = os.environ.get("MAX_REPO_SIZE", one_GB_in_KB)
localize_site_url = os.environ.get("LOCALIZE_SITE_URL", True)
optimize_images = os.environ.get("OPTIMIZE_IMAGES", False)
clear_repo_before_clone = os.environ.get("CLEAR_REPO_BEFORE_CLONE", False)


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
        commit = re.match(r"Commit Hash: (?P<commit>\w{40})", file_contents)
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


def get_remote_git_size(parsed_repo):
    """ """
    is_github = parsed_repo.platform == "github"

    if not is_github:
        log.warn(
            "Repository is not hosted on GitHub; unable to determine the size"
        )
        return False
    else:
        url = f"https://api.github.com/repos/{parsed_repo.owner}/{parsed_repo.repo}"
        response = requests.get(url)
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


def remove_local_repo(source_dir):
    """ """
    log.info("Removing local repository...")

    for files in os.listdir(source_dir):
        path = os.path.join(source_dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    log.info(f"Local repository removed from {source_dir}")


def install_python_dependencies(path):
    """ """
    start = time()

    log.info("Installing dependencies...")
    command = ["python3", "-m", "pip", "install", "-q", "-r", path]
    subprocess.Popen(command, shell=False).wait()
    log.info("Dependencies installed in %.2f seconds", time() - start)


def build(source_dir: str, build_dir: str):
    """
    Builds the docs using mkdocs. Expects a source and a destination (build) directory.
    """
    log.info("Running mkdocs...")
    os.system(f'mkdocs build -f "{source_dir}/mkdocs.yml" -d "{build_dir}"')


def serve(build_dir):
    """ """
    os.chdir(build_dir)
    port = 8000

    server_object = HTTPServer(
        server_address=("", port), RequestHandlerClass=CGIHTTPRequestHandler
    )

    # Start the web server
    log.info(f"Started Server on http://localhost:{port}")
    log.info("-------------------------------------\n")
    server_object.serve_forever()


def main():
    start = time()

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

    source_dir = "/docs/source"
    build_base_dir = "/docs/site"
    build_dir = f"{build_base_dir}/build"
    version_file = f"{build_base_dir}/version/current_version.txt"

    remote_git_commit = get_remote_git_commit(normalized_repo)
    file_commit = get_commit_version_file(version_file)

    is_version_current = is_commit_version_current(
        file_commit, remote_git_commit
    )

    if not is_version_current:
        log.info(f"GIT Repository current commit differs than local:")
        log.info(
            f"Local commit: {file_commit} - Remote commit: {remote_git_commit}"
        )

        repo_size = get_remote_git_size(parsed_repo)
        repo_size_converted = convert_repo_size_to_MB(repo_size)

        log.info(f"GIT Repository Size: {repo_size_converted}")

        repo_size_allowed = repo_size_is_allowed(repo_size, max_repo_size)
        max_repo_size_converted = convert_repo_size_to_MB(max_repo_size)

        if not repo_size_allowed:
            log.error(
                "Repo Size is larger than the max allowed (Repo:"
                f" {repo_size_converted}, Max: {max_repo_size_converted})"
            )
            return

        if clear_repo_before_clone:
            remove_local_repo(source_dir)

        clone_repo(normalized_repo, source_dir)
        install_python_dependencies("/docs/source/docs/requirements.txt")

        if localize_site_url:
            log.info(f"Localizing site URL references...")
            localize_site_urls("/docs/source/mkdocs.yml")

        build(source_dir, build_dir)

        local_git_commit = get_local_git_commit(source_dir)
        set_commit_version_file(version_file, local_git_commit)
        log.info(
            "GIT Repository local commit has been updated to:"
            f" {local_git_commit}"
        )

        remove_local_repo(source_dir)
    else:
        log.info(f"GIT Repository current commit matches local: {file_commit}")

    log.info("Documentation prepared in %.2f seconds", time() - start)
    serve(build_dir)


if __name__ == "__main__":
    main()

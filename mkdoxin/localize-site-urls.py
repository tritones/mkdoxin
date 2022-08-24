#!/usr/bin/env python3

import re
import yaml


class ProxyPythonName(yaml.YAMLObject):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value


class SafeLoader(yaml.SafeLoader):  # pylint: disable=too-many-ancestors

    """
    Safe YAML loader.
    This loader parses special ``!!python/name:`` tags without actually
    importing or executing code. Every other special tag is ignored.
    Borrowed from https://stackoverflow.com/a/57121993
    Issue https://github.com/readthedocs/readthedocs.org/issues/7461
    """

    def ignore_unknown(
        self, node
    ):  # pylint: disable=no-self-use, unused-argument
        return None

    def construct_python_name(
        self, suffix, node
    ):  # pylint: disable=no-self-use, unused-argument
        return ProxyPythonName(suffix)


SafeLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:", SafeLoader.construct_python_name
)
SafeLoader.add_constructor(None, SafeLoader.ignore_unknown)


def fix_index_and_md(match):
    path = match.group(1)

    if path is None:
        path = "index"
    else:
        path = path.rstrip("/")

    return path + ".md"


def localize_site_urls(yaml_filename):
    with open(yaml_filename, "r") as yaml_file:
        try:
            config = yaml.load(yaml_file, Loader=SafeLoader)

            old_site_url = config["site_url"]
        except yaml.YAMLError as exc:
            print(exc)

        yaml_file = open(yaml_filename, "r")

        file_data = yaml_file.read()

        # Removes anchor references
        anchor_regex = (
            r"(?<!site_url: )"
            + re.escape(old_site_url)
            + r"\/?([A-Za-z0-9-_\/]+)?(\/?#[\w\-_]+)?"
        )

        file_data = re.sub(anchor_regex, fix_index_and_md, file_data)

        yaml_file = open(yaml_filename, "w")
        yaml_file.write(file_data)
        yaml_file.close()


def main():
    localize_site_urls("mkdocs.yml")


if __name__ == "__main__":
    main()

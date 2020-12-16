import re

import semver

from .config import config

REGEX_VERSION = re.compile(r"^v\d+.*")

class SemverTag(semver.VersionInfo):
    @classmethod
    def from_tag(cls, tag):
        self = cls.parse(_normalized_tag_string(tag))
        self.tag = tag
        return self

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tag = None

    def __repr__(self):
        return f"<{super().__repr__()}, {self.tag.__repr__()}>"


class VersionsList(list):
    def __init__(self, repo=None):
        super().__init__()
        self.refresh(repo)

    def refresh(self, repo=None):
        if not repo:
            repo = config.repo
        self.clear()
        for tag in repo.tags:
            try:
                self.append(SemverTag.from_tag(tag))
            except ValueError:
                ...  # Silence if tag is not a semver tag

    def last(self, number=1):
        return sorted(self, reverse=True)[:number]

    @property
    def latest(self):
        return max(self)

    def next_major(self):
        return self.latest.bump_major()

    def next_minor(self):
        return self.latest.bump_minor()

    def next_patch(self):
        return self.latest.bump_patch()

    def next_build(self):
        return self.latest.bump_build()


def _normalized_tag_string(tag):
    tag_name = tag.name
    if REGEX_VERSION.search(tag_name):
        tag_name = tag_name[1:]
    return tag_name


versions = VersionsList()

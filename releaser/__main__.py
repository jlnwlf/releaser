"""Main entrypoint for CLI interactions."""

from humanize import naturaldelta

from .config import config
from .versions import versions
from .templates import template
from .formatters import GitmojiFormatter

next_version = {
    'MAJOR': versions.next_major,
    'MINOR': versions.next_minor,
    'PATCH': versions.next_patch,
    'BUILD': versions.next_build,
}[config.next_version]()


def generate_draft():
    upcoming_commits = config.repo.iter_commits(f'{versions.latest.tag}..master')
    # for commit in upcoming_commits:
    #     print(f'* {commit.summary}')
    l = {
        'app_name': config.app_name,
        'config': config,
        'duration_text': naturaldelta(config.end - config.start),
        'summary': GitmojiFormatter(upcoming_commits).render(),
        'next_version': next_version,
        'current_version': versions.latest,
    }
    print(template.render(**l))


def main():
    {
        'draft': generate_draft
    }[config.command]()


if __name__ == '__main__':
    main()

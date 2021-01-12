"""Main entrypoint for CLI interactions."""

from humanize import naturaldelta

from .config import config
from .versions import versions
from .templates import template_mail, template_tag, template_changes
from .formatters import GitmojiFormatter

next_version = {
    'MAJOR': versions.next_major,
    'MINOR': versions.next_minor,
    'PATCH': versions.next_patch,
    'BUILD': versions.next_build,
}[config.next_version]()

def _commit_range():
    return config.repo.iter_commits(f'{versions.latest.tag}..{config.release_branch}')

def generate_draft():
    upcoming_commits = _commit_range()
    formatter = GitmojiFormatter(upcoming_commits)

    l = {
        'app_name': config.app_name,
        'config': config,
        'duration_text': naturaldelta(config.end - config.start),
        'summary': formatter.render(),
        'next_version': next_version,
        'current_version': versions.latest,
    }

    print(template_mail.render(**l))

def print_changes():
    upcoming_commits = _commit_range()
    formatter = GitmojiFormatter(upcoming_commits, postprocessor=None)

    l = {
        'next_version': next_version,
        'release_date': config.release_date.date(),
        'summary': formatter.render()
    }

    print(template_changes.render(**l))

def generate_tag():
    upcoming_commits = _commit_range()
    formatter = GitmojiFormatter(upcoming_commits, postprocessor=None,
                                 no_markdown=True)

    l = {
        'app_name': config.app_name,
        'summary': formatter.render(),
        'next_version': next_version,
        'title': f'{config.app_name} {next_version} ({config.release_date.date()})'
    }

    tag_text = template_tag.render(**l)
    print(tag_text)

    if input('Create tag @ HEAD with the given text ? (y/n)') == 'y':
        config.repo.create_tag(f'v{next_version}', message=tag_text, s=True)

def main():
    {
        'draft': generate_draft,
        'tag': generate_tag,
        'changes': print_changes,
    }[config.command]()


if __name__ == '__main__':
    main()

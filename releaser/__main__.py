"""Main entrypoint for CLI interactions."""

from .config import config


def generate_draft():
    ...  # TODO: Generate draft markdown here


def main():
    {
        'draft': generate_draft
    }[config.command]()


if __name__ == '__main__':
    main()

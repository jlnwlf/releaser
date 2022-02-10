from pathlib import Path
import re
from datetime import datetime, time

from configargparse import ArgParser
from git import Repo
import arrow
import humanize

ROOT = Path(__file__).parent.parent.absolute()


def relative_time(input_str, now=None):
    """Type parser for argparse for dates.

    Could be called recursively.

    Args:
        string_date (str): Examples
            - today
            - tomorrow
            - today @ 21:45

    Returns:
        datetime: The datetime representation of given string.
    """

    if not now:
        now = arrow.now()

    input_str = input_str.strip().lower()

    # Simple date

    if input_str == 'today':
        return now.date()
    elif input_str == 'tomorrow':
        return now.dehumanize('in 1 days').date()

    # Only time

    t = re.match(r"(\d+)(?::|h)(\d+)", input_str)
    if t:
        t = [int(v) for v in t.groups()]
        return datetime.combine(now.date(), time(*t)).astimezone()

    # Date + time

    splitted = _split_date_and_time_string(input_str)

    if splitted:
        d = relative_time(splitted['date'])
        t = relative_time(splitted['time']).time()
        return datetime.combine(d, t).astimezone()

    # Default

    return now.dehumanize(input_str).date().astimezone()


def _split_date_and_time_string(string_date):
    m = re.match(r"(?P<date>.+)\s+(@|at)\s*(?P<time>.+)", string_date)
    if m:
        return m.groupdict()


def _humanize_relative_datetime(s):
    return f"{humanize.naturalday(s)} at {s.strftime('%H:%M')}"


class Config:
    def __init__(self):
        self._config = self._create_parser().parse_known_args()[0]

    @property
    def start_text(self):
        return _humanize_relative_datetime(self._config.start)

    @property
    def end_text(self):
        return _humanize_relative_datetime(self._config.end)

    @staticmethod
    def _create_parser():
        parser = ArgParser(prog='releaser',
                           default_config_files=['.releaser'],
                           auto_env_var_prefix='releaser_')

        parser.add_argument('--config',
                            is_config_file=True)

        parser.add_argument('--repository',
                            dest='repo',
                            type=Repo,
                            default=Repo(Path.cwd()))

        parser.add_argument('--preprod-url',
                            dest='preprod_url',
                            default=None)

        parser.add_argument('--release-branch',
                            default='master')

        parser.add_argument('--app-name')
        parser.add_argument('--release-date',
                            default='today',
                            type=relative_time)
        parser.add_argument('--issue-tracker-url')

        next_version_group = parser.add_mutually_exclusive_group()
        next_version_group.add_argument('--build',
                                        action='store_const',
                                        const='BUILD',
                                        env_var='RELEASER_NEXT_VERSION',
                                        dest='next_version')
        next_version_group.add_argument('--patch',
                                        action='store_const',
                                        const='PATCH',
                                        env_var='RELEASER_NEXT_VERSION',
                                        dest='next_version')
        next_version_group.add_argument('--minor',
                                        action='store_const',
                                        const='MINOR',
                                        env_var='RELEASER_NEXT_VERSION',
                                        dest='next_version')
        next_version_group.add_argument('--major',
                                        action='store_const',
                                        const='MAJOR',
                                        env_var='RELEASER_NEXT_VERSION',
                                        dest='next_version')
        next_version_group.set_defaults(next_version='MINOR')

        subparsers = parser.add_subparsers(dest='command')
        versions_subparser = subparsers.add_parser('versions')
        subparsers.add_parser('changes')
        subparsers.add_parser('draft')
        subparsers.add_parser('tag')

        parser.add_argument('--template-mail',
                            type=Path,
                            dest='template_mail_path',
                            default=ROOT / 'releaser/templates/mail.md.j2')

        parser.add_argument('--template-tag',
                            type=Path,
                            dest='template_tag_path',
                            default=ROOT / 'releaser/templates/tag.md.j2')

        parser.add_argument('--template-changes',
                            type=Path,
                            dest='template_changes_path',
                            default=ROOT / 'releaser/templates/changes.md.j2')

        parser.add_argument('--start',
                            default='today @ 21:45',
                            type=relative_time)
        parser.add_argument('--end',
                            default='today @ 22:15',
                            type=relative_time)

        parser.set_defaults(command='changes')

        versions_subparser.add_argument('n',
                                        nargs='?',
                                        type=int,
                                        default=999999999)

        return parser

    def __getattr__(self, name):
        return getattr(self._config, name)

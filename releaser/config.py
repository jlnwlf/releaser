from pathlib import Path

from configargparse import ArgParser
from git import Repo
import maya

ROOT = Path(__file__).parent.parent.absolute()

class Config:
    def __init__(self):
        self._config = self._create_parser().parse_known_args()[0]

        self._config.start_text = self._config.start
        self._config.end_text = self._config.end

        self._config.start = maya.when(self._config.start,
                                       timezone='Europe/Zurich').local_datetime()
        self._config.end = maya.when(self._config.end,
                                     timezone='Europe/Zurich').local_datetime()

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

        parser.add_argument('--app-name')
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

        # Could be None, as the meaning depend on the sub-command and
        # evaluated at runtime...
        # parser.add_argument('--range',
        #                     dest='commit_range')

        subparsers = parser.add_subparsers(dest='command')
        draft_parser = subparsers.add_parser('draft')

        parser.add_argument('--template',
                                  type=Path,
                                  dest='template_path',
                                  default=ROOT / 'releaser/templates/change.md.j2')
        parser.add_argument('--start',
                            default='today @ 21:45')
        parser.add_argument('--end',
                            default='today @ 22:15')
        return parser

    def __getattr__(self, name):
        return getattr(self._config, name)

config = Config()

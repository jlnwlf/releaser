from pathlib import Path

from configargparse import ArgParser
from git import Repo

ROOT = Path(__file__).parent.parent.absolute()

class Config:
    def __init__(self):
        self._config = self._create_parser().parse_known_args()[0]

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

        # Could be None, as the meaning depend on the sub-command and
        # evalutated at runtime...
        parser.add_argument('--range',
                            dest='commit_range')

        subparsers = parser.add_subparsers(dest='command')

        draft_parser = subparsers.add_parser('draft')
        draft_parser.add_argument('--template',
                                  type=Path,
                                  dest='template_path',
                                  default=ROOT / 'templates/change.md.mako')
        return parser

    def __getattr__(self, name):
        return getattr(self._config, name)

config = Config()

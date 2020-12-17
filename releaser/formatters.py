from collections import OrderedDict
from io import StringIO

from .postprocessors import GitLabPostprocessor


class Formatter:

    def __init__(self, commits, postprocessor=GitLabPostprocessor):
        self.commits = commits
        self.postprocessor = postprocessor

    def render(self):
        rendered = self.preprocess()
        if self.postprocessor:
            rendered = self.postprocessor(rendered).render()
        return rendered

    def preprocess(self):
        raise NotImplementedError('Must code')


class GitmojiFormatter(Formatter):
    """Formatter for gitmoji commits"""

    DEFAULT_CATEGORIES = OrderedDict([
        ('Features', '✨'),
        ('Changes', '👽➕➖🔧🌐💬🗃'),
        ('Rollback', '⏪'),
        ('Operations', '🔨'),
        ('Refactoring', '♻️🚚🏗💥🎨'),
        ('UI/UX', '🚸♿️💄🍱💫'),
        ('Security', '🛂🔒⬆️⬇️📌📈'),
        ('Deprecations/Removal', '🔥🗑'),
        ('Bugfixes', '🚑🐛'),
        ('Testing', '✅'),
        ('Performance', '⚡️'),
        ('Misc', '📝🚀🎉🚨✏️📦⚗💡🍻🔊🔇📱🥚🌱'),
    ])

    def __init__(self, *args, no_markdown=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.no_markdown = no_markdown

    def preprocess(self):
        output = OrderedDict()
        commits = list(self.commits)
        treated = []

        for category_name, mojis in self.DEFAULT_CATEGORIES.items():
            for moji in mojis:
                for commit in commits:
                    if moji in commit.summary:
                        try:
                            output[category_name].append(commit)
                        except KeyError:
                            output[category_name] = [commit]
                        treated.append(commit)

        for commit in treated:
            commits.remove(commit)

        leftover_commits = commits

        s = StringIO()

        for title, commits in output.items():
            if self.no_markdown:
                s.write(f'{title}\n\n')
            else:
                s.write(f'### {title}\n\n')
            for commit in commits:
                s.write(f'* {commit.summary}\n')
            s.write('\n')

        if len(leftover_commits) > 0:
            if self.no_markdown:
                s.write('Other\n\n')
                for commit in leftover_commits:
                    s.write(f'* {commit.summary}\n')
            else:
                s.write('<!--\n\nUncategorized commits:\n\n')
                for commit in leftover_commits:
                    s.write(f'* {commit.summary}\n')
                s.write('\n-->\n')

        return s.getvalue()[:-1]

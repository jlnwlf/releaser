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
        ('Features', ('✨', )),
        ('Changes', ('👽', '➕', '➖', '🔧', '🌐', '💬', '🗃')),
        ('Rollback', ('⏪', )),
        ('Operations', ('🔨', '🐳')),
        ('Refactoring', ('♻️', '🚚', '🏗', '💥', '🎨')),
        ('UI/UX', ('🚸', '♿️', '💄', '🍱', '💫')),
        ('Security', ('🛂', '🔒', '⬆️', '⬇️', '📌', '📈')),
        ('Deprecations/Removal', ('🔥', '🗑')),
        ('Bugfixes', ('🚑', '🐛')),
        ('Error handling', ('🥅', )),
        ('Testing', ('✅', )),
        ('Performance', ('⚡️', )),
        ('Misc', ('📝', '🚀', '🎉', '🚨', '✏️', '📦',
                  '⚗', '💡', '🍻', '🔊', '🔇', '📱',
                  '🥚', '🌱')),
    ])

    DEFAULT_IGNORED = ('🔖', )

    def __init__(self, *args, no_markdown=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.no_markdown = no_markdown

    def preprocess(self):
        output = OrderedDict()
        commits = list(self.commits)
        treated = []

        for category_name, mojis in self.DEFAULT_CATEGORIES.items():
            for commit in commits:
                for moji in mojis:
                    if moji in commit.summary:
                        try:
                            output[category_name].append(commit)
                        except KeyError:
                            output[category_name] = [commit]
                        treated.append(commit)
                        break

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

        filtered_leftovers = []
        for commit in leftover_commits:
            if not any((m in commit.summary) for m in self.DEFAULT_IGNORED):
                filtered_leftovers.append(commit)


        if len(filtered_leftovers) > 0:
            if self.no_markdown:
                s.write('Other\n\n')
                for commit in filtered_leftovers:
                    s.write(f'* {commit.summary}\n')
            else:
                s.write('<!--\n\nUncategorized commits:\n\n')
                for commit in filtered_leftovers:
                    s.write(f'* {commit.summary}\n')
                s.write('\n-->\n')

        return s.getvalue()[:-1]

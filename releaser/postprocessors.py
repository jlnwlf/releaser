import re

from .config import config

class Postprocessor:
    def __init__(self, rendered_text):
        self.rendered_text = rendered_text

    def render(self):
        raise NotImplementedError('Code me')

class GitLabPostprocessor(Postprocessor):

    ISSUE_REGEX = re.compile(r'(?P<text>#(?P<issue_number>\d+))')

    def render(self):
        return self.ISSUE_REGEX.sub(f'[\g<text>]({config.issue_tracker_url}\g<issue_number>)', self.rendered_text)

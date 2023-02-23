from jinja2 import Template

from .config import Config

config = Config()

template_mail = Template(open(config.template_mail_path).read())
template_tag = Template(open(config.template_tag_path).read())
template_changes = Template(open(config.template_changes_path).read())

RANDOM_GREETINGS = [
    'New version incoming!',
    'Brace yourself! New version on the way!',
    'Heads up! Fresh release coming soon.',
    'Hey, guess what? A new version is on the horizon.',
    'Look alive! New version dropping soon.',
    'Alert! New version headed your way.',
    'Hold on tight! New version about to land.',
    'Psst! New version coming soon.',
    'Attention! New version in the works.',
    'Heads up! New version ready for launch.',
    'Get ready! New version release date set.',
    "It's happening! New version release imminent.",
]

RANDOM_INTRODUCTIONS = [
    "Here's what's new in the upcoming release:",
    "Check out the latest changes in the upcoming version:",
    "We've made some exciting updates in the upcoming release:",
    "Discover what's changed in the upcoming version:",
    "Curious about the new features? Take a look at what's coming in the upcoming release:",
    "The upcoming release brings some awesome changes - check them out:",
    "Exciting news! Here are the updates coming your way in the upcoming version:",
    "Take a sneak peek at the changes in the upcoming release:",
    "Wondering what's new? Here's a rundown of the changes in the upcoming version:",
    "We're excited to share the changes coming in the upcoming release:",
    "Here's a preview of the new features in the upcoming version:",
    "Behold! The upcoming release is packed with awesome new changes:",
]

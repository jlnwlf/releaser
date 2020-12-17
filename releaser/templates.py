from jinja2 import Template

from .config import config

template_mail = Template(open(config.template_mail_path).read())
template_tag = Template(open(config.template_tag_path).read())
template_changes = Template(open(config.template_changes_path).read())

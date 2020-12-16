from jinja2 import Template

from .config import config

template = Template(open(config.template_path).read())

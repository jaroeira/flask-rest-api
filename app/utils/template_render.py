import jinja2
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
template_directory = os.path.join(current_directory, '..', 'templates')

template_loader = jinja2.FileSystemLoader(template_directory)
template_env = jinja2.Environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

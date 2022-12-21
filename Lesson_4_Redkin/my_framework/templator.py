from urllib import request

from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """Рендерит шаблон"""
    env = Environment()
    # Папка для поиска шаблонов
    env.loader = FileSystemLoader(folder)
    # Поиск шаблона
    template = env.get_template(template_name)

    # Рендерим шаблон с параметрами
    return template.render(**kwargs)


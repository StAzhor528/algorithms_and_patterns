from time import time


class AppRoute:
    """Структурный паттерн - декоратор.
    Предназначен для связи контролера с путями.
    """

    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """Структурный паттерн - Декоратор"""

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """Подсчитывает время работы абстрактного метода"""
        def timeit(method):
            def timed(*args, **kwargs):
                time_start = time()
                result = method(*args, **kwargs)
                time_end = time()
                delta = time_end - time_start

                print(f'debug --> модуль {self.name} выполнялся {delta: 2.2f} ms')
                return result
            return timed
        return timeit(cls)

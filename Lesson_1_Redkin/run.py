from wsgiref.simple_server import make_server

from my_framework.main import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

with make_server('', 8000, application) as httpd:
    print("Запуск на порту 8000...")
    print("Страница index/: http://127.0.0.1:8000/")
    print("Страница about/: http://127.0.0.1:8000/about")
    httpd.serve_forever()

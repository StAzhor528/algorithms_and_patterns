from datetime import date

from my_framework.templator import render
from patterns.creational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    """Контроллер - Главная страница"""

    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


class About:
    """Контроллер - О проекте"""

    def __call__(self, request):
        return '200 OK', render('about.html')


class StudyPrograms:
    """Контроллер - Расписания"""

    def __call__(self, request):
        return '200 OK', render('study-programs.html', date=date.today())


class NotFound404:
    """Контроллер - 404"""

    def __call__(self, request):
        return '404 WHAT', '404 Страница не найдена'


class CreateCourse:
    """Контроллер - Создать курс"""
    category_id = 1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1 and name not in site.name_courses:
                site.name_courses.append(name)
                category = site.find_category_by_id(self.category_id)
                course = site.create_course('record', name, category)
                site.courses.append(course)
            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Еще не создано ни одной категории'


class CoursesList:
    """Контроллер - Список курсов"""

    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            print('lstcat', category)
            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'Ни одного курса еще не было добавлено'


class CopyCourse:
    """контроллер - Копировать курс"""

    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}{len(site.courses)}'
                new_course = old_course.clone()
                new_course.name = new_name
                new_course.category = old_course.category
                site.courses.append(new_course)

            return '200 OK', render('courses_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name,
                                    id=new_course.category.id)
        except KeyError:
            return '200 OK', 'Ни одного курса еще не было добавлено'


class CreateCategory:
    """Контроллер - Создать категорию"""

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if name not in site.name_categories:
                site.name_categories.append(name)
                new_category = site.create_category(name, category)
                site.categories.append(new_category)
            return '200 OK', render('index.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


class CategoryList:
    """Контроллер - Список категий"""

    def __call__(self, request):
        logger.log('Списко категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)

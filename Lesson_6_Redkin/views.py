from datetime import date

from my_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SMSNotifier, ListView, CreateView, BaseSerializer, \
    ConsoleWriter, FileWriter

site = Engine()
logger = Logger('main', ConsoleWriter())
email_notifier = EmailNotifier()
sms_notifier = SMSNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    """Контроллер - Главная страница"""

    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    """Контроллер - О проекте"""

    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    """Контроллер - Расписания"""

    def __call__(self, request):
        return '200 OK', render('study-programs.html', date=date.today())


class NotFound404:
    """Контроллер - 404"""

    def __call__(self, request):
        return '404 WHAT', '404 Страница не найдена'


@AppRoute(routes=routes, url='/create_course/')
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

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
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


@AppRoute(routes=routes, url='/courses_list/')
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


@AppRoute(routes=routes, url='/copy_course/')
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


@AppRoute(routes=routes, url='/create_category/')
class CreateCategory:
    """Контроллер - Создать категорию"""

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            site.name_categories.append(name)
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html',
                                    objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    """Контроллер - Список категий"""

    def __call__(self, request):
        logger.log('Списко категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/student_list/')
class StudentListView(ListView):
    """Контроллер - Список студентов"""
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    """Контроллер - Создание студента"""
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add_student/')
class AddStudentByCourseCreateView(CreateView):
    """Контроллер - Добавление студента на курс"""
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)
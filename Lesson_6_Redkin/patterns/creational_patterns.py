from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject


class User:
    """Абстрактный пользователь"""

    def __init__(self, name):
        self.name = name


class Teacher(User):
    """Учитель"""
    pass


class Student(User):
    """Студент"""

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:
    """Оберка для создания сущности(Student, Teacher)"""
    types = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def create(cls, type_, name):
        """Порождающий паттерн, фабричный метод"""
        return cls.types[type_](name)


class CoursePrototype:
    """Прототип курсов обучения"""

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    """Модель курса"""

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    """Объект интерактивного курса"""
    pass


class RecordCourse(Course):
    """Объект курса в записи"""
    pass


class CourseFactory:
    """Оберка для создания сущности(InteractiveCourse, RecordCourse)"""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
    }

    @classmethod
    def create(cls, type_, name, category):
        """Порождающий паттерн, фабричный метод"""
        return cls.types[type_](name, category)


class Category:
    """Модель категории"""
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """Движок проекта"""

    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []
        self.name_categories = []
        self.name_courses = []

    @staticmethod
    def create_user(type_, name):
        """Создает пользователя"""
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        """Создает категорию"""
        return Category(name, category)

    def find_category_by_id(self, id):
        """Находит категорию по id"""
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Категория с id = {id} отсутствует')

    @staticmethod
    def create_course(type_, name, category):
        """Создает курс"""
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        """Получает курс по имени"""
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        """Получает студента по имени"""
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        """Декодирует в читаемый вид"""
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Порождающий паттерн дял логирования"""

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        if name in cls._instance:
            return cls._instance[name]
        else:
            cls._instance[name] = super().__call__(*args, **kwargs)
            return cls._instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log--> {text}'
        self.writer.write(text)

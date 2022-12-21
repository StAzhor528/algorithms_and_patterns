from datetime import date
from views import Index, About, StudyPrograms, CreateCourse, CoursesList, CopyCourse, CreateCategory, CategoryList


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/study_programs/': StudyPrograms(),
    '/create_course/': CreateCourse(),
    '/courses_list/': CoursesList(),
    '/copy_course/': CopyCourse(),
    '/create_category/': CreateCategory(),
    '/category_list/': CategoryList(),
}

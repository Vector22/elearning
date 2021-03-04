from django.test import TestCase
from django.contrib.auth.models import User
# from django.urls import reverse

from courses.models import Subject, Course, Module, Text


class SubjectModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk

    def setUp(self):
        # Run once for every test method to setup clean data
        self.subject1 = Subject.objects.get(id=self.subject1_id)

    def test_title_label(self):
        field_label = self.subject1._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_slug_label(self):
        field_label = self.subject1._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_title_max_length(self):
        max_length = self.subject1._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_slug_max_length(self):
        max_length = self.subject1._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_title(self):
        expected_object_name = f'{self.subject1.title}'
        self.assertEquals(expected_object_name, self.subject1.__str__())

    def test_object_saved(self):
        subject = Subject.objects.get(slug='programing')
        subject.save()
        self.assertEqual(subject.title, self.subject1.title)

    def test_ordering(self):
        # By default it is ordered by Id
        # We ensure that ordering field of Meta is set to ['title']
        # It is an alphabetical order
        Subject.objects.create(title='Music', slug='music')
        Subject.objects.create(title='Art', slug='art')

        defaultOrder = "<QuerySet [<Subject: Programming>, <Subject: Music>, "
        # Avoid line too long error
        defaultOrder += "<Subject: Art>]>"
        orderByTitle = "<QuerySet [<Subject: Art>, <Subject: Music>, "
        orderByTitle += "<Subject: Programing>]>"

        subjectsList = str(Subject.objects.all().only('id', 'title'))

        self.assertNotEqual(subjectsList, defaultOrder)
        self.assertEqual(subjectsList, orderByTitle)


class CourseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk
        adminUser = User.objects.create(username="admin",
                                        email="admin@protonmail.com",
                                        first_name="Benoit",
                                        is_superuser=True)
        adminUser.set_password('B3nB3n256*')
        adminUser.save()

    def setUp(self):
        # Run once for every test method to setup clean data
        self.user = User.objects.last()
        # self.subject1 = Subject.objects.get(id=1)
        self.subject1 = Subject.objects.get(id=self.subject1_id)
        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.user,
                                             title='Course 1',
                                             slug='course-1')

    def test_course_subject(self):
        self.assertEqual(self.course1.subject, self.subject1)

    def test_course_owner(self):
        self.assertEqual(self.course1.owner, self.user)

    def test_title_label(self):
        field_label = self.course1._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_slug_label(self):
        field_label = self.course1._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'slug')

    def test_title_max_length(self):
        max_length = self.course1._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_slug_max_length(self):
        max_length = self.course1._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_title(self):
        expected_object_name = f'{self.course1.title}'
        self.assertEquals(expected_object_name, str(self.course1))

    def test_ordering(self):
        # By default it is ordered by Id
        # We ensure that ordering field of Meta is set to ['-created']
        # It is a descending DateTime order
        Course.objects.create(subject=self.subject1,
                              owner=self.user,
                              title='Course 3',
                              slug='course-3')
        Course.objects.create(subject=self.subject1,
                              owner=self.user,
                              title='Course 2',
                              slug='course-2')

        defaultOrder = "<QuerySet [<Course: Course 1>, <Course: Course 3>, "
        # Avoid line too long error
        defaultOrder += "<Course: Course 2>]>"
        orderByCreated = "<QuerySet [<Course: Course 2>, <Course: Course 3>, "
        orderByCreated += "<Course: Course 1>]>"

        courseList = str(Course.objects.all().only('id', 'title'))

        self.assertNotEqual(courseList, defaultOrder)
        self.assertEqual(courseList, orderByCreated)


class ModuleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk
        adminUser = User.objects.create(username="admin",
                                        email="admin@protonmail.com",
                                        first_name="Benoit",
                                        is_superuser=True)
        adminUser.set_password('B3nB3n256*')
        adminUser.save()

    def setUp(self):
        # Run once for every test method to setup clean data
        self.user = User.objects.last()
        # self.subject1 = Subject.objects.get(id=1)
        self.subject1 = Subject.objects.get(id=self.subject1_id)
        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.user,
                                             title='Course 1',
                                             slug='course-1')
        self.module1 = Module.objects.create(course=self.course1,
                                             title='Module 1')

    def test_module_course(self):
        self.assertEqual(self.module1.course, self.course1)

    def test_title_label(self):
        field_label = self.module1._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        max_length = self.module1._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_order_dot_space_title(self):
        # f'{order}. {title}' => 1. Module 1 or 2. Module 2
        expected_object_name = f'{self.module1.order}. {self.module1.title}'
        self.assertEquals(expected_object_name, str(self.module1))

    def test_ordering(self):
        # We created a custom order field, w'll check if it's
        # as we think
        self.assertEqual(self.module1.order, 0)

        # Create a second module to the same course and check
        module2 = Module.objects.create(course=self.course1, title='Module 2')
        self.assertEqual(module2.order, 1)

        # Create a third module and overide the default order computation
        # +1 on the highest module order
        module3 = Module.objects.create(course=self.course1,
                                        title='Module 3',
                                        order=4)
        self.assertNotEqual(module3.order, 2)
        self.assertEqual(module3.order, 4)

        # The next module created for the same course will have
        # highest order + 1 (for us 4+1=5)
        module4 = Module.objects.create(course=self.course1, title='Module 4')
        self.assertEqual(module4.order, 5)

        # Create new course and add new module to check that module order
        # are specific to course they belong to
        course2 = Course.objects.create(subject=self.subject1,
                                        owner=self.user,
                                        title='Course 2',
                                        slug='course-2')
        module5 = Module.objects.create(course=course2, title='Module 5')

        self.assertEqual(module5.order, 0)


class ContentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk
        user = User.objects.create(username="admin",
                                   email="admin@protonmail.com",
                                   first_name="Benoit",
                                   is_superuser=True)
        user.set_password('B3nB3n256*')
        user.save()

    def setUp(self):
        self.user = User.objects.last()
        content_string = """A long text content."""
        self.text_content = Text.objects.create(title='content 1',
                                                content=content_string,
                                                owner=self.user)

    def test_object_name_is_title(self):
        self.assertEquals(self.text_content.__str__(), 'content 1')

    def test_render_correct_template(self):
        self.assertEquals(self.text_content.render(),
                          '<p>A long text content.</p>')

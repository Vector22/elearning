from django.test import TestCase
from django.contrib.auth.models import User

from courses.templatetags.course import model_name
from courses.models import Subject, Course, Module


class ModelNameTest(TestCase):
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
        self.subject1 = Subject.objects.get(id=self.subject1_id)
        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.user,
                                             title='Course 1',
                                             slug='course-1')
        self.module1 = Module.objects.create(course=self.course1,
                                             title='Module 1')

    def test_model_name(self):
        class NoMeta():
            pass

        no_meta = NoMeta()
        name = model_name(self.subject1)
        self.assertEquals(name, self.subject1._meta.model_name)
        self.assertEquals(None, model_name(no_meta))

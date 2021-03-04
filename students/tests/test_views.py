from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User, Group, Permission

from courses.models import Subject, Course, Module
# from django.contrib.auth.forms import UserCreationForm


class StudentRegistrationViewTest(TestCase):
    """
    Tests for the StudentRegistrationView
    """
    def setUp(self):
        self.user = User.objects.create(username='Babacar',
                                        password='S3cr3t**',
                                        email='baba@example.com')

    def test_registration_view(self):
        """
        Test that the registration view rejects invalid submissions,
        and creates a new user and redirects after a valid submission.
        """
        # Invalid data fails.
        response = self.client.post(
            reverse('students:student_registration'),
            data={
                'username': 'Babacar',  # Will fail on username uniqueness.
                'email': 'baba@example.com',
                'password1': 'foo',
                'password2': 'foo'
            })
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failUnless(response.context['form'].errors)

        response = self.client.post(reverse('students:student_registration'),
                                    data={
                                        'username': 'ulrich',
                                        'email': 'ulrich@example.com',
                                        'password1': 'R3K1n2@2@',
                                        'password2': 'R3K1n2@2@'
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         reverse('students:student_course_list'))
        self.assertEqual(User.objects.count(), 2)


class StudentCourseListViewTest(TestCase):
    """
    Tests for the StudentCourseListView
    """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk

    def setUp(self):
        # Create permissions and add them to the Instructors group
        instructor_group = Group.objects.create(name="Instructors")
        perm_add = Permission.objects.get(codename='add_course')
        perm_edit = Permission.objects.get(codename='change_course')
        perm_del = Permission.objects.get(codename='delete_course')
        instructor_group.permissions.set([perm_add, perm_edit, perm_del])
        instructor_group.save()

        self.instructor = User.objects.create(username="instructor",
                                              email="instruk@protonmail.com",
                                              first_name="Timothee",
                                              last_name="Guichert")
        self.instructor.set_password('B3nB3n256*')
        self.instructor.groups.add(instructor_group)
        self.instructor.save()

        # self.student = User.objects.create(username='Ulrich',
        #                                    password='S3cr3t**',
        #                                    email='baba@example.com')
        # self.student.save()
        self.subject1 = Subject.objects.get(id=self.subject1_id)

        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.instructor,
                                             title='Course 1',
                                             slug='course-1')

        self.student1 = self.course1.students.create_user(
            username='Ulrich', password='S3cr3t**', email='baba@example.com')
        self.student1.save()

        self.course1.students.add(self.student1)
        self.course1.save()

        self.cousrse2 = self.student1.courses_joined.create(
            subject=self.subject1,
            owner=self.instructor,
            title='Course 2',
            slug='course-2')

    def test_queryset(self):
        self.client.login(username='Ulrich', password='S3cr3t**')
        response = self.client.get(reverse('students:student_course_list'))
        self.assertEqual(response.status_code, 200)

        self.assertTrue(len(response.context['object_list']) == 2)


class StudentCourseDetailViewTest(TestCase):
    """
    Tests for the StudentCourseListView
    """
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk

    def setUp(self):
        # Create permissions and add them to the Instructors group
        instructor_group = Group.objects.create(name="Instructors")
        perm_add = Permission.objects.get(codename='add_course')
        perm_edit = Permission.objects.get(codename='change_course')
        perm_del = Permission.objects.get(codename='delete_course')
        instructor_group.permissions.set([perm_add, perm_edit, perm_del])
        instructor_group.save()

        self.instructor = User.objects.create(username="instructor",
                                              email="instruk@protonmail.com",
                                              first_name="Timothee",
                                              last_name="Guichert")
        self.instructor.set_password('B3nB3n256*')
        self.instructor.groups.add(instructor_group)
        self.instructor.save()

        # self.student = User.objects.create(username='Ulrich',
        #                                    password='S3cr3t**',
        #                                    email='baba@example.com')
        # self.student.save()
        self.subject1 = Subject.objects.get(id=self.subject1_id)

        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.instructor,
                                             title='Course 1',
                                             slug='course-1')
        self.module1 = Module.objects.create(course=self.course1,
                                             title='Module 1')

        self.student1 = self.course1.students.create_user(
            username='Ulrich', password='S3cr3t**', email='baba@example.com')
        self.student1.save()

        self.course1.students.add(self.student1)
        self.course1.save()

        self.cousrse2 = self.student1.courses_joined.create(
            subject=self.subject1,
            owner=self.instructor,
            title='Course 2',
            slug='course-2')

    def test_context_data(self):
        self.client.login(username='Ulrich', password='S3cr3t**')
        response = self.client.get(
            reverse('students:student_course_detail', args=['1']))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(self.course1, response.context['course'])

    def test_context_data_with_module(self):
        self.client.login(username='Ulrich', password='S3cr3t**')
        response = self.client.get(
            reverse('students:student_course_detail_module', args=['1', '1']))
        self.assertEqual(response.status_code, 200)
        # The course and it's first module are in the context
        self.assertEquals(self.course1, response.context['course'])
        self.assertEquals(self.module1, response.context['module'])

from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group, Permission

# For selenium
from django.conf import settings
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from courses.models import Subject, Course


class CourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk

        cls.admin = User.objects.create(username="admin",
                                        email="admin@protonmail.com",
                                        first_name="Administrator",
                                        is_superuser=True)
        cls.admin.set_password('B3nB3n256*')
        cls.admin.save()

        cls.anyuser = User.objects.create(username="anyUser",
                                          email="anyuser@protonmail.com",
                                          first_name="Benoit")
        cls.anyuser.set_password('K4rlsTR0m*')
        cls.anyuser.save()

    def setUp(self):
        # Run once for every test method to setup clean data
        # self.user = User.objects.get(id=1)
        self.subject1 = Subject.objects.get(id=self.subject1_id)
        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.admin,
                                             title='Course 1',
                                             slug='course-1')

    def test_root_view_url_is_accessible(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_root_view_url_accessible_by_name(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)

    def test_subject_view_url_is_accessible(self):
        response = self.client.get('/course/subject/programing/')
        self.assertEqual(response.status_code, 200)

    def test_subject_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse('courses:course_list_subject', args=['programing']))
        self.assertEqual(response.status_code, 200)

    def test_root_view_uses_correct_template(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course/list.html')

    def test_subject_view_uses_correct_template(self):
        response = self.client.get(
            reverse('courses:course_list_subject', args=['programing']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course/list.html')

    def test_list_all_courses(self):
        # Only one course is created so far
        response1 = self.client.get(reverse('course_list'))
        response2 = self.client.get(
            reverse('courses:course_list_subject', args=['programing']))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        # Both views retrives the same number of courses
        self.assertTrue(len(response1.context['courses']) == 1)
        self.assertTrue(len(response2.context['courses']) == 1)
        # Second view by subject has 'subject' set in the context
        self.assertTrue(response2.context['subject'] is not None)

    def test_list_courses_by_subject(self):
        # Create some subjects and courses
        subject2 = Subject.objects.create(title='Music', slug='music')
        Course.objects.create(subject=self.subject1,
                              owner=self.admin,
                              title='Course 2',
                              slug='course-2')
        Course.objects.create(subject=subject2,
                              owner=self.admin,
                              title='Course 3',
                              slug='course-3')

        response1 = self.client.get(reverse('course_list'))
        response2 = self.client.get(
            reverse('courses:course_list_subject', args=['programing']))
        response3 = self.client.get(
            reverse('courses:course_list_subject', args=['music']))

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

        # First response list: all courses(3)
        self.assertTrue(len(response1.context['courses']) == 3)
        # Second view list: 2 courses
        self.assertTrue(len(response2.context['courses']) == 2)
        # Thirst response list: one course
        self.assertTrue(len(response3.context['courses']) == 1)


class CourseDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        cls.admin = User.objects.create(username="admin",
                                        email="admin@protonmail.com",
                                        first_name="Administrator",
                                        is_superuser=True)
        cls.admin.set_password('B3nB3n256*')
        cls.admin.save()

        cls.anyuser = User.objects.create(username="anyUser",
                                          email="anyuser@protonmail.com",
                                          first_name="Benoit")
        cls.anyuser.set_password('K4rlsTR0m*')
        cls.anyuser.save()

        cls.subject1_id = Subject.objects.create(title='Programing',
                                                 slug='programing').pk

    def setUp(self):
        # Run once for every test method to setup clean data
        self.subject1 = Subject.objects.get(id=self.subject1_id)
        self.slug1 = self.subject1.slug
        self.course1 = Course.objects.create(subject=self.subject1,
                                             owner=self.admin,
                                             title='Course 1',
                                             slug='course-1')

    def test_view_url_accessible_by_name(self):
        # url = /course/course-1
        response = self.client.get(
            reverse('courses:course_detail', kwargs={'slug': 'course-1'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse('courses:course_detail', kwargs={'slug': 'course-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'courses/course/detail.html')

    def test_view_uses_correct_object(self):
        course = get_object_or_404(Course, slug='course-1')
        response = self.client.get(
            reverse('courses:course_detail', kwargs={'slug': 'course-1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['object'] == course)


# Test instructors private views


# Manage Course object views
class ManageCourseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        # Create permissions and add them to the Instructors group
        instructor_group = Group.objects.create(name="Instructors")
        perm_add = Permission.objects.get(codename='add_course')
        perm_edit = Permission.objects.get(codename='change_course')
        perm_del = Permission.objects.get(codename='delete_course')
        instructor_group.permissions.set([perm_add, perm_edit, perm_del])
        instructor_group.save()

        cls.instructor = User.objects.create(username="instructor",
                                             email="instruk@protonmail.com",
                                             first_name="Timothee",
                                             last_name="Guichert")
        cls.instructor.set_password('B3nB3n256*')
        cls.instructor.groups.add(instructor_group)
        cls.instructor.save()

        # # A not instructor user
        # user = User.objects.create(username="user",
        #                            email="user@protonmail.com",
        #                            first_name="Benoit")
        # user.set_password('K4rlsTR0m*')
        # user.save()

    def setUp(self):
        # Initialise some stuff at each test
        pass

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('courses:manage_course_list'))
        self.assertRedirects(response,
                             '/accounts/login/?next=/course/my_courses/')

    def test_logged_in_uses_correct_template(self):
        # Log the instructor
        self.client.login(username='instructor', password='B3nB3n256*')
        response = self.client.get(reverse('courses:manage_course_list'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'instructor')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response,
                                'courses/manage/course/manage_list.html')


# Some functionnals tests with selenium

# class SeleniumTest(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         if settings.DEBUG:
#             cls.selenium = WebDriver(
#                 executable_path='/home/vector22/bin/geckodriver/geckodriver')
#         else:
#             # Geckodriver is on the server
#             cls.selenium = WebDriver(
#                 executable_path='/home/ulrich/bin/geckodriver/geckodriver')
#         cls.selenium.implicitly_wait(3)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def test_login(self):
#         login_url = f'{self.live_server_url}/accounts/login'
#         self.selenium.get(login_url)
#         username_input = self.selenium.find_element_by_id("id_username")
#         username_input.send_keys('karl')
#         password_input = self.selenium.find_element_by_id("id_password")
#         password_input.send_keys('V3ct0r22*')

#         self.selenium.find_element_by_class_name('login-btn').click()

#         # Check the returned result
#         labels = ['Username', 'Password']

#         # assert the presence of some wignets label
#         for label in labels:
#             assert label in self.selenium.page_source

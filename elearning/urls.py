"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from courses.views import CourseListView

import debug_toolbar


# dumy error to test sentry
def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # We want to display the list of courses in the URL http://127.0.0.1:8000/
    # and all other URLs for the courses application have the /course/ prefix.
    path('', CourseListView.as_view(), name='course_list'),
    # Sentry error view
    path('sentry-debug/', trigger_error),
    # Django debug toolbar
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('course/', include('courses.urls')),

    # Students urls
    path('students/', include('students.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

"""DevClubLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from users import views as user_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('register/', user_views.register, name='register'),
    path('course/<str:code>/', user_views.course_detail_view, name='course'),
    path('course/addassignment/<str:code>/', user_views.course_assignment, name='course-assignment'),
    path('course/download/<str:code>/<path:filename>/<path:name>', user_views.download_file, name='download-file'),
    path('course/addnote/<str:code>/', user_views.course_note, name='course-note'),
    path('course/<str:code>/participants', user_views.course_participants, name='course-participants'),
    path('course/add', user_views.add_course, name='course-add'),
    path('course/<str:code>/viewassignment/<path:name>', user_views.submit_assignment, name='submit-assignment'),
    path('course/<str:code>/viewassignmentsubmissions/<path:name>', user_views.view_submissions, name='view-submissions'),
    path('course/<str:code>/editassignment/<path:name>', user_views.edit_assignment, name='edit-assignment'),
    path('course/<str:code>/announcements', user_views.course_announcements, name='course-announcements'),
    path('course/<str:code>/announcement/<path:name>', user_views.course_announcement_page, name='course-announcement-page')
      
]

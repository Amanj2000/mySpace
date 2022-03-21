"""my_space URL Configuration

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
from django.urls import path
from mySpace_app import views

urlpatterns = [
    path('',views.show_login_page,name="show_login"),
    path('doLogin',views.do_login,name="do_login"),
    path('admin/', admin.site.urls),

    #Faculty URLs
    path('faculty_home', views.faculty_home, name="faculty_home"),

    #Student URLs
    path('student_home', views.student_home, name="student_home"),
]

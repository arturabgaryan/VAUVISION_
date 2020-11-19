"""music URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from Music.views import *


urlpatterns = [
    path('', enter),
    path('reg_page',registration),
    path('create',create),
    path('log_in',log_in),
    path('log_out',log_out),
    path('main',main),
    path('form/', form),
    path('form-admin/', panel),
    path('form-admin/logout/', admin_logout),
    path('form-admin/login/', admin_login),
    path('form-admin/generate_code/', generate_auth_code),
    path('form-admin/signup/', admin_signup),
    path('form-admin/submit-request/', submit_request),
    path('form-admin/delete-request/', delete_request),
    path('form-admin/change-track-name/', change_name),
    path('authorization',authorization),
    path('main',main),
    path('account',account),
    path('change_profile_info',change_profile_info_page),
    path('change',change),
    path('back',back),
    path('log_in',log_in),
    path('send_email',send_email),
    path('index',index),
    path('upload',upload)
]

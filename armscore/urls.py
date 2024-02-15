"""
URL configuration for armscore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from score import views
from django.contrib.auth import views as authViews
# from django_pdfkit import PDFView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', authViews.LogoutView.as_view(next_page=''), name='exit'),
    path('accounts/password_change/', views.user_password_change, name='password_change'),
    path('accounts/password_change/done/', views.user_password_change_done, name='password_change_done'),
    path('accounts/password_reset/', views.user_password_reset, name='password_reset'),
    path('accounts/password_reset/done/', views.user_password_reset_done, name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('accounts/reset/done/', views.password_reset_done, name='password_reset_done'),
    path('accounts/registration/', views.user_registration),
    path('dashboard/match/', views.match),
    # path(r'^my-pdf/$', PDFView.as_view(template_name='results.html'), name='results'),
    path('dashboard/table/', views.one_table, name='table'),
    path('dashboard/select_user/', views.select_user, name='select_user'),
    path('validate_username', views.validate_username, name='validate_username'),
    path('check_username', views.check_username, name='check_username'),
    path('set_winner', views.set_winner, name='set_winner'),
    path('set_weight', views.set_weight, name='set_weight'),
    path('set_table', views.set_table, name='set_table'),
    path('rollback', views.rollback, name='rollback'),
    path('dashboard/matches/', views.show_match_list),
    path('download/', views.download_file),
    path('info/', views.info),
    path('members/', views.show_members, name='show_members'),
    path('set_user_photo/', views.set_user_photo),

]

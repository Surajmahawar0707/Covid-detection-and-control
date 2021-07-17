
from django.contrib import admin
from django.urls import path
from expapp import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home", views.home, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("register", views.register, name='register'),
    path("accounts/login/", views.login, name='login'),
    path("login", views.login, name='login'),
    path("profile", views.profile_view, name='profile_view'),
    path("input", views.input_view, name='input_view'),
    path("output", views.output_view, name='output_view'),
    path("logout", views.logout, name='logout'),
    path("contact_after_login", views.contact_after_login, name='contact_after_login'),
    path("about_after_login", views.about_after_login, name='about_after_login'),
    path("edit_profile", views.edit_profile, name='edit_profile'),
    path("forgot_password", views.forgot_password, name='forgot_password'),
    path("password_reset", views.password_reset, name='password_reset'),
    path("del_acc", views.del_acc, name='del_acc')
]
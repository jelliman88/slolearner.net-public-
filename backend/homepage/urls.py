from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'homepage'
urlpatterns = [
    path("", views.homepage, name='homepage'),
    path("login", views.login_form, name='login'),
    path('logout', views.logout_form, name='logout'),
    path("signup", views.signup_form, name='signup'),
    path("signup", views.signup_form, name='signup'),
    path("verify-email", views.verify_email, name='verify-email'),
    path("podcast", views.podcast, name='podcast'),
    path("sample", views.sample, name='sample'),
    path("reset-password", auth_views.PasswordResetView.as_view(template_name='reset-password.html'), name='reset_password'),
    

]
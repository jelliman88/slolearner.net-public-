from django.urls import path
from . import views


app_name = 'learn'
urlpatterns = [
    path('dash', views.dash, name='dash'),
    path('my-account/', views.my_account, name='my-account'),
    path('select-lesson/<int:level>', views.select_lesson, name='select-lesson'),
    path('lesson/<int:level>/<int:id>', views.lesson, name='lesson'),
    path('add-remove-homework/', views.add_remove_homework, name='add-remove-homework'),
    path('homework/', views.homework, name='homework'),
    path("check-username-exists/", views.ajax_check_username_exists, name='check-username-exists'),
    path('adjust-progress/', views.adjust_progress, name='adjust-progress'),
    path('no-cheating/', views.no_cheating, name='no-cheating'),
    

] 
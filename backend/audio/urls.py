from django.urls import path
from . import views



app_name = 'audio'
urlpatterns = [
    path('', views.dash, name='dash'),
    path('match-audio/<int:level>/<int:lesson>/<int:chunks>', views.match_audio, name='match-audio'),
]
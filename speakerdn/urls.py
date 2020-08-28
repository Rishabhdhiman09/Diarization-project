from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('transcript', views.transcript, name = 'transcript'),
    path('namechange', views.namechange, name = 'nameChange'),

]

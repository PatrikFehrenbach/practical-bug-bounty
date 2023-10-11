from django.urls import path
from . import views


urlpatterns = [

    path('resources/', views.resources, name='resources'),

]
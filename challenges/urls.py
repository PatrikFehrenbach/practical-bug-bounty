from django.urls import path
from . import views


urlpatterns = [

    path('challenges/', views.challenges, name='challenges'),

]
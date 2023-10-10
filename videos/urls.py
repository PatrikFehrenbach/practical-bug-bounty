from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contribute/', views.contribute, name='contribute'),
    path('philosophy/', views.philosophy, name='philosophy'),
    path('contact/', views.contact, name='contact'),
    path('community/', views.community, name='community'),
    path('resources/', views.resources, name='resources'),
    path('challenges/', views.challenges, name='challenges'),
#    path('category/<int:category_id>/', views.category_videos, name='category_videos'),

]

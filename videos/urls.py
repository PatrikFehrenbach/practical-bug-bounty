from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contribute/', views.contribute, name='contribute'),
    path('philosophy/', views.philosophy, name='philosophy'),
    path('contact/', views.contact, name='contact'),
#    path('category/<int:category_id>/', views.category_videos, name='category_videos'),

]

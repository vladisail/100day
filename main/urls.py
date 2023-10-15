from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('course_assignments', views.course_assignments)
]

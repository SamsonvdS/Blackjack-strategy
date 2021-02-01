from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('infinite_bj', views.infinite_bj, name='infinite_bj'),
]
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('infinite_blackjack', views.infinite_blackjack, name='infinite_blackjack'),
]
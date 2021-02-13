from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('infinite_blackjack', views.infinite_blackjack, name='infinite_blackjack'),
    path('infinite_blackjack/calculate_hand', views.infinite_calculate_hand, name='infinite_calculate_hand'),
]
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('infinite_blackjack', views.infinite_blackjack, name='infinite_blackjack'),
    path('infinite_blackjack/calculate_hand', views.infinite_calculate_hand, name='infinite_calculate_hand'),
    path('infinite_blackjack/new_shoe', views.infinite_new_shoe, name='infinite_new_shoe'),
    path('infinite_blackjack/new_round', views.infinite_new_round, name='infinite_new_round'),
]
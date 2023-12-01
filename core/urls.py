# core/urls.py
from django.urls import path
from .views import random_page,home,search_anime


app_name = 'core'  # Defina o app_name para usar com o namespace

urlpatterns = [
    path('random/', random_page, name='random_page'),
    path('', home, name='home'),
    path('search/', search_anime, name='search_anime'),

]
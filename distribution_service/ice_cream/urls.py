
from django.urls import path

from ice_cream.views import ice_cream_list

urlpatterns = [
    path('ice-cream/', ice_cream_list, name='ice_cream_list'),
]

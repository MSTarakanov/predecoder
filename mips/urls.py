from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='mips_main'),
    path('process/', process, name='process')
]

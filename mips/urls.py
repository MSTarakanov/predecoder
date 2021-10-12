from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='mips_main'),
    path('examples/<int:example_id>/', show_example),
]

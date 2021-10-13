from django.urls import path
from .views import *


urlpatterns = [
    path('<int:example_id>/', index, name='x86_main')
]
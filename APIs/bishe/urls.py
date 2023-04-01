from django.test import TestCase

# Create your tests here.

from django.urls import path
from django.urls import include
# Create your tests here.
from . import views

urlpatterns = [
     path('testioc/', views.testioc),  #这样  接口地址就是 127.0.0.1:8001/bishe/testapi
]
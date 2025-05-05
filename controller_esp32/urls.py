from django.urls import path
from controller_esp32.views import control_led

urlpatterns = [path('control_led/', control_led)]

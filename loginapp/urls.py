from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('device/status/<int:device_id>/', views.device_status, name='device_status'),  # This matches the device status route
]

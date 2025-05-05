from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('loginapp.urls')),
path('', include('controller_esp32.urls')),
]

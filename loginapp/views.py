from django.shortcuts import render, redirect
from .models import DeviceControl
from django.http import JsonResponse

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "admin":
            return redirect("dashboard")
        else:
            error = "Invalid credentials"
    return render(request, "login.html", {"error": error})


def dashboard(request):
    print("Request method:", request.method)
    print("POST data:", request.POST)  # ✅ Inspect form data

    device, _ = DeviceControl.objects.get_or_create(device_id=1)

    if request.method == 'POST':
        if 'on' in request.POST:
            device.status = True
        elif 'off' in request.POST:
            device.status = False
        device.save()

    return render(request, 'dashboard.html', {'device': device})
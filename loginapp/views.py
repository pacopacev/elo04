from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone  # ✅ CORRECT import

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
    print("POST data:", request.POST)

    device, _ = DeviceControl.objects.get_or_create(device_id=1)

    if request.method == 'POST':
        if 'on' in request.POST:
            device.status = True
        elif 'off' in request.POST:
            device.status = False
        device.last_triggered = timezone.now()  # Log the time when the action happened
        device.save()

        # Optionally, show a message after a change
        success_message = "Device turned ON" if device.status else "Device turned OFF"

        return render(request, 'dashboard.html', {
            'device': device,
            'last_triggered': device.last_triggered,
            'success_message': success_message
        })

    return render(request, 'dashboard.html', {
        'device': device,
        'last_triggered': device.last_triggered
    })


@csrf_exempt
def device_status(request, device_id):
    try:
        device = DeviceControl.objects.get(device_id=device_id)

        if request.method == 'GET':
            # Just return the current status and time
            return JsonResponse({
                'status': device.status,
                'last_triggered': device.last_triggered.strftime("%Y-%m-%d %H:%M:%S") if device.last_triggered else None
            })

        elif request.method == 'POST':
            # Handle updates (on/off actions here)
            if 'on' in request.POST:
                device.status = True
            elif 'off' in request.POST:
                device.status = False

            device.last_triggered = timezone.now()  # Log the action time
            device.save()
            return JsonResponse({'message': 'Status updated', 'status': device.status})

    except DeviceControl.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)

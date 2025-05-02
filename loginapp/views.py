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
    device, _ = DeviceControl.objects.get_or_create(device_id=1)

    if request.method == 'POST':
        if 'on' in request.POST:
            device.status = True
        elif 'off' in request.POST:
            device.status = False
        device.last_triggered = timezone.now()
        device.save()

        # Return JSON for AJAX
        return JsonResponse({
            'message': 'Status updated',
            'status': device.status,
            'last_triggered': device.last_triggered.strftime("%Y-%m-%d %H:%M:%S")
        })

    return render(request, 'dashboard.html', {
        'message': 'Status updated',
        'device': device,
        'last_triggered': device.last_triggered
    })


@csrf_exempt
def device_status(request, device_id):
    try:
        device = DeviceControl.objects.get(device_id=device_id)

        if request.method == 'GET':
            print(device_id)
            return JsonResponse({
                'device_id': device_id,
                'message': 'Status updated',
                'status': device.status,
                'last_triggered': device.last_triggered.strftime("%Y-%m-%d %H:%M:%S") if device.last_triggered else None
            })

        elif request.method == 'POST':
            # Read the action from POST body (e.g., "on" or "off")
            if 'on' in request.POST:
                device.status = True
            elif 'off' in request.POST:
                device.status = False
            else:
                return JsonResponse({'error': 'Invalid command'}, status=400)

            device.last_triggered = timezone.now()
            device.save()

            return JsonResponse({
                'device_id': device_id,
                'message': 'Status updated',
                'status': device.status,
                'last_triggered': device.last_triggered.strftime("%Y-%m-%d %H:%M:%S") if device.last_triggered else None

            })

        return render(request, 'dashboard.html', {
            'device_id': device_id,
            'message': 'Status updated',
            'device': device,
            'last_triggered': device.last_triggered
        })

    except DeviceControl.DoesNotExist:
        return JsonResponse({'error': 'Device not found'}, status=404)
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

WEBSOCKET_SERVER_URL = 'https://esp32nodeserver.onrender.com'

@csrf_exempt
def control_led(request):
    if request.method == 'POST':
        cmd = request.POST.get('command')
        try:
            requests.post(WEBSOCKET_SERVER_URL, data=cmd)  # or use a WebSocket client here
        except Exception as e:
            return HttpResponse(f"Error: {e}", status=500)
    return render(request, 'index.html')

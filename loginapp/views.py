from django.shortcuts import render, redirect

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == "admin" and password == "password":
            return redirect("dashboard")
        else:
            error = "Invalid credentials"
    return render(request, "login.html", {"error": error})

def dashboard_view(request):
    return render(request, "dashboard.html")


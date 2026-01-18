from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Step 1: Authenticate credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Step 2: Create session & log user in
            login(request, user)
            return redirect("users/dashboard")

        else:
            return render(
                request,
                "users/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def dashboard(request):
    return render(request, "users/dashboard.html")
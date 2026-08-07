from django.shortcuts import render, redirect
from .models import User


def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = {}

        if password != confirm_password:
            errors['password_error'] = "Passwords do not match!"

        if User.objects.filter(username=username).exists():
            errors['username_error'] = "Username already exists!"

        if User.objects.filter(email=email).exists():
            errors['email_error'] = "Email already exists!"

        if User.objects.filter(phone=phone).exists():
            errors['phone_error'] = "Phone number already exists!"

        if errors:
            return render(request, 'signup.html', {
                'errors': errors,
                'first_name': first_name,
                'middle_name': middle_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'phone': phone
            })

        User.objects.create(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')


# LOGIN
def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(
                username=username,
                password=password
            )

            request.session["user_id"] = user.id

            return redirect("home")

        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# PROFILE
def profile(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(
        id=request.session["user_id"]
    )

    return render(request, "profile.html", {
        "user": user
    })


# LOGOUT
def logout_page(request):
    request.session.flush()
    return redirect("login")


# HOME
def home(request):
    user = None
    is_logged_in = False

    if request.session.get("user_id"):
        user = User.objects.filter(
            id=request.session["user_id"]
        ).first()

        is_logged_in = user is not None

    return render(request, "index.html", {
        "user": user,
        "is_logged_in": is_logged_in,
    })

def account(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])

    return render(request, "account.html", {
        "user": user
    })
def edit_profile(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.middle_name = request.POST.get("middle_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.email = request.POST.get("email", "")
        user.phone = request.POST.get("phone", "")
        user.gender = request.POST.get("gender", "")
        user.languages_spoken = request.POST.get("languages_spoken", "")
        user.occupation = request.POST.get("occupation", "")
        user.about_me = request.POST.get("about_me", "")
        user.business_name = request.POST.get("business_name", "")
        user.pin_code = request.POST.get("pin_code", "")
        user.city = request.POST.get("city", "")
        user.state = request.POST.get("state", "")

        if request.FILES.get("profile_photo"):
            user.profile_photo = request.FILES["profile_photo"]

        user.save()

        return redirect("profile")

    return render(request, "edit_profile.html", {
        "user": user
    })


def help_center(request):
    return render(request, "help_center.html")


def payment_refund(request):
    return render(request, "payment_refund.html")


def forgot_password(request):
    return render(request, "forgot_password.html")


def reset_password(request):
    return render(request, "reset_password.html")


def verify_otp(request):
    return render(request, "verify_otp.html")
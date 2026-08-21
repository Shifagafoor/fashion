import random

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .models import User


# =========================
# SIGNUP
# =========================

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


# =========================
# LOGIN + OTP
# =========================

def login_page(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        try:

            user = User.objects.get(
                username=username,
                password=password
            )

            # Generate 6 digit OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP in session
            request.session["otp"] = otp

            # Save user ID in session
            request.session["otp_user_id"] = user.id

            # Send OTP to user's email
            send_mail(
                subject="Your Majestic Login OTP",
                message=f"""
Hello {user.first_name},

Your OTP for login is:

{otp}

Please enter this OTP on the verification page.

Thank you,
Majestic
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Open OTP verification page
            return redirect("verify_otp")

        except User.DoesNotExist:

            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


# =========================
# VERIFY OTP
# =========================

def verify_otp(request):

    if request.method == "POST":

        otp1 = request.POST.get("otp1", "")
        otp2 = request.POST.get("otp2", "")
        otp3 = request.POST.get("otp3", "")
        otp4 = request.POST.get("otp4", "")
        otp5 = request.POST.get("otp5", "")
        otp6 = request.POST.get("otp6", "")

        entered_otp = (
            otp1 +
            otp2 +
            otp3 +
            otp4 +
            otp5 +
            otp6
        )

        saved_otp = request.session.get("otp")
        user_id = request.session.get("otp_user_id")

        # Check whether OTP exists
        if not saved_otp or not user_id:

            return render(request, "verify-otp.html", {
                "error": "OTP expired. Please login again."
            })

        # Check OTP
        if entered_otp == saved_otp:

            # Login user
            request.session["user_id"] = user_id

            # Remove OTP from session
            request.session.pop("otp", None)
            request.session.pop("otp_user_id", None)

            # Go to home
            return redirect("home")

        else:

            return render(request, "verify-otp.html", {
                "error": "Invalid OTP. Please try again."
            })

    return render(request, "verify-otp.html")


# =========================
# PROFILE
# =========================

def profile(request):

    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(
        id=request.session["user_id"]
    )

    return render(request, "profile.html", {
        "user": user
    })


# =========================
# ACCOUNT
# =========================

def account(request):

    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(
        id=request.session["user_id"]
    )

    return render(request, "account.html", {
        "user": user
    })


# =========================
# EDIT PROFILE
# =========================

def edit_profile(request):

    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(
        id=request.session["user_id"]
    )

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


# =========================
# LOGOUT
# =========================

def logout_page(request):

    request.session.flush()

    return redirect("login")


# =========================
# HOME
# =========================

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


# =========================
# HELP CENTER
# =========================

def help_center(request):

    return render(request, "help_center.html")


# =========================
# PAYMENT & REFUND
# =========================

def payment_refund(request):

    return render(request, "payment_refund.html")


# =========================
# FORGOT PASSWORD
# =========================

def forgot_password(request):

    return render(request, "forgot_password.html")


# =========================
# RESET PASSWORD
# =========================

def reset_password(request):

    return render(request, "reset_password.html")
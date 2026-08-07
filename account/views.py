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

        print("First Name:", first_name)
        print("password:", password)
        print("Confirm Password:", confirm_password)

        errors = {}

        #password check
        if password != confirm_password:
            errors['password_error'] ="password do not match"

        #username already exists
        if User.objects.filter(username=username).exists():
            errors['username_error']="username already exist!"

        #email already exists
        if User.objects.filter(email=email).exists():
            errors['email_error'] = "Email already exists!"

            #phone
            if User.objects.filter(phone=phone).exists():
                errors['phone_error'] = "Phone number already exists!"

        #if any error 
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
        else:
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


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username, password=password)
            request.session["user_id"] = user.id
            return redirect("home")
        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "login.html")


def profile(request):
    if "user_id" not in request.session:
        return redirect("login")

    user = User.objects.get(id=request.session["user_id"])
    return render(request, "profile.html", {"user": user})


def logout_page(request):
    request.session.flush()
    return redirect("login")


def home(request):
    user = None
    is_logged_in = False

    if request.session.get("user_id"):
        user = User.objects.filter(id=request.session["user_id"]).first()
        is_logged_in = user is not None

    return render(request, 'index.html', {
        'user': user,
        'is_logged_in': is_logged_in,
    })


def forgot_password(request):
    return render(request, 'forgot_password.html')


def reset_password(request):
    return render(request, 'reset_password.html')


def verify_otp(request):
    return render(request, 'verify_otp.html')
from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username, password=password)
            return redirect('home')
        except User.DoesNotExist:
            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })
    return render (request, 'login.html')

def home(request):
    return render(request, 'index.html')
def forgot_password(request):
    return render(request, 'forgot_password.html')
def reset_password(request):
    return render(request, 'reset_password.html')
def verify_otp(request):
    return render(request, 'verify_otp.html')
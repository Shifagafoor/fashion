from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')
@login_required
def login_page(request):

    return render(request, 'login.html')
def signup_page(request):
    return render(request, 'signup.html')
def forgot_password(request):
    return render(request, 'forgot_password.html')
def reset_password(request):
    return render(request, 'reset_password.html')
def verify_otp(request):
    return render(request, 'verify_otp.html')
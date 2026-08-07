from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),

    path('account/', views.account, name='account'),

    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('help-center/', views.help_center, name='help_center'),
    path('payment-refund/', views.payment_refund, name='payment_refund'),

    path('logout/', views.logout_page, name='logout'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]
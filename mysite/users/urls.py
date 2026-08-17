from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from .views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile'),
path('password-change/', PasswordChangeView.as_view(
    template_name='users/password_change_form.html'), name='password_change'),
path('password-change/done/', PasswordChangeDoneView.as_view(
    template_name='users/password_change_done.html'), name='password_change_done'),
]

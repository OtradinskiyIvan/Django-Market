from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView, PasswordChangeView, PasswordChangeDoneView, 
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import *

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('profile/topup/', topup, name='topup'),
    path('profile/withdraw/', withdraw, name='withdraw'),
path('password-change/', PasswordChangeView.as_view(
    template_name='users/password_change_form.html'), name='password_change'),
path('password-change/done/', PasswordChangeDoneView.as_view(
    template_name='users/password_change_done.html'), name='password_change_done'),
path('password-reset/done/', PasswordResetDoneView.as_view(
    template_name='users/password_reset_done.html'), name='password_reset_done'),
path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
    template_name='users/password_reset_confirm.html',
    success_url=reverse_lazy('password_reset_complete'),
    ), name='password_reset_confirm'),
path('password-reset/complete/', PasswordResetCompleteView.as_view(
    template_name='users/password_reset_complete.html'), name='password_reset_complete'),
path('password-reset/', PasswordResetView.as_view(
    template_name='users/password_reset_form.html',
    email_template_name='users/password_reset_email.html',
    success_url=reverse_lazy('password_reset_done'),
), name='password_reset'),
path('register/done/', register_done, name='register_done'),
path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
path('<int:profile_id>/', user_page, name='user_page'),
path('<int:profile_id>/review/', leave_review, name='leave_review'),
]

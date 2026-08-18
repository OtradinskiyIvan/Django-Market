from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.db.models import Avg
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import CreateView, UpdateView

from .forms import *
from .models import Profile, SellerReview


class LoginUser(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'
    extra = {'title': 'Authentication'}

    def get_success_url(self):
        return reverse_lazy('catalog_main')


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Registration'}

    def form_valid(self, form):
        with transaction.atomic():
            User.objects.filter(
                Q(username=form.cleaned_data['username']) |
                Q(email=form.cleaned_data['email']),
                is_active=False,
            ).delete()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            user.is_active = False
            user.save()
            user.profile.name = form.cleaned_data['name']
            user.profile.phone = str(form.cleaned_data['phone'])
            user.profile.role = int(form.cleaned_data['role'])
            user.profile.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        link = f"http://{domain}{reverse('verify_email', args=[uid, token])}"
        message = render_to_string('users/verify_email.html', {'user': user, 'link': link})
        send_mail('Verify registration', message, None, [user.email])
        return redirect('register_done')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = Profile

    form_class = ProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Profile'}

    def get_object(self, queryset=None):       
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile')

def verify_email(request: HttpRequest, uidb64, token) -> HttpResponse:
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.profile.is_verified = True
        user.profile.save(update_fields=['is_verified'])
        return redirect('login')

    return render(request, 'users/verify_invalid.html', {'title': 'Invalid link'})

def register_done(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/register_done.html', {'title': 'Check your email'})


@login_required
def topup(request: HttpRequest) -> HttpResponse:
    form = TopUpForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        profile.balance += form.cleaned_data['amount']
        profile.save(update_fields=['balance'])
        messages.success(request, 'Balance topped up')
    return redirect('profile')


@login_required
def withdraw(request: HttpRequest) -> HttpResponse:
    form = WithdrawForm(request.POST)
    if form.is_valid():
        profile = request.user.profile
        amount = form.cleaned_data['amount']
        if amount > profile.balance:
            messages.error(request, 'Not enough funds')
        else:
            profile.balance -= amount
            profile.save(update_fields=['balance'])
            messages.success(request, 'Withdrawn')
    return redirect('profile')


def user_page(request: HttpRequest, profile_id: int) -> HttpResponse:
    profile = get_object_or_404(Profile, pk=profile_id)
    if request.user.is_authenticated and profile.pk == request.user.profile.pk:
        return redirect('profile')

    data = {
        'title': profile.name,
        'profile': profile,
        'avg_rating': None,
        'reviews': [],
        'form': None,
    }
    if profile.role == Profile.Role.SELLER:
        avg = profile.review_received.aggregate(Avg('rating'))['rating__avg']
        data['avg_rating'] = avg
        data['reviews'] = profile.review_received.select_related('customer').order_by('-created_at')
        if request.user.is_authenticated:
            data['form'] = SellerReviewForm()
    return render(request, 'users/user_page.html', data)


@login_required
def leave_review(request: HttpRequest, profile_id: int) -> HttpResponse:
    seller = get_object_or_404(Profile, pk=profile_id)
    if seller.pk == request.user.profile.pk:
        messages.error(request, 'You cannot review yourself')
        return redirect('user_page', profile_id)
    form = SellerReviewForm(request.POST)
    if form.is_valid():
        SellerReview.objects.update_or_create(
            customer=request.user.profile,
            seller=seller,
            defaults={
                'rating': form.cleaned_data['rating'],
                'comment': form.cleaned_data['comment'],
            },
        )
        messages.success(request, 'Review saved')
    else:
        messages.error(request, 'Invalid review data')
    return redirect('user_page', profile_id)

# accounts/views.py
import random, string
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import EmailUserCreationForm, PasswordResetRequestForm, PasswordResetVerifyForm
from .models import PasswordResetToken
from django.contrib.auth.models import User

def unified_auth(request, active_tab='login', error_message=None):
    signup_form = EmailUserCreationForm()
    login_form = AuthenticationForm()
    context = {
        'signup_form': signup_form,
        'login_form': login_form,
        'active_tab': active_tab,
        'error_message': error_message,  # inline error HTML
    }
    return render(request, 'accounts/auth_slider.html', context)

def signup_view(request):
    if request.method == 'POST':
        signup_form = EmailUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect_url': '/tasks/'})
            else:
                return redirect('task_list')
        else:
            form_html = render_to_string('accounts/signup_form_partial.html', {'signup_form': signup_form})
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'form_html': form_html})
            else:
                return unified_auth(request, active_tab='signup', error_message=form_html)
    return unified_auth(request, active_tab='signup')

def login_view(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'redirect_url': '/tasks/'})
            else:
                return redirect('task_list')
        else:
            form_html = render_to_string('accounts/login_form_partial.html', {'login_form': login_form})
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'form_html': form_html})
            else:
                return unified_auth(request, active_tab='login', error_message=form_html)
    return unified_auth(request, active_tab='login')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

# -------------------------------
# Password Reset Flow
# -------------------------------

def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                form.add_error(None, "No user found with that username and email.")
            else:
                # Generate a 6-character verification code
                token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                # Remove any previous token and create a new one
                PasswordResetToken.objects.filter(user=user).delete()
                PasswordResetToken.objects.create(user=user, token=token)
                # Send email with the verification code
                send_mail(
                    'Your Password Reset Verification Code',
                    f'Hello {username},\n\nYour password reset verification code is: {token}\nIt is valid for 1 hour.',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return redirect('password_reset_verify')
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset_request.html', {'form': form})

def password_reset_verify_view(request):
    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            token_input = form.cleaned_data['token']
            try:
                user = User.objects.get(username=username)
                prt = PasswordResetToken.objects.get(user=user, token=token_input)
                if not prt.is_valid():
                    form.add_error(None, "The verification code has expired. Please request a new code.")
                else:
                    # Store user id in session for password reset
                    request.session['password_reset_user_id'] = user.id
                    return redirect('password_reset_complete')
            except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
                form.add_error(None, "Invalid username or verification code.")
    else:
        form = PasswordResetVerifyForm()
    return render(request, 'accounts/password_reset_verify.html', {'form': form})

def password_reset_complete_view(request):
    user_id = request.session.get('password_reset_user_id')
    if not user_id:
        return redirect('password_reset_request')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            PasswordResetToken.objects.filter(user=user).delete()
            del request.session['password_reset_user_id']
            return redirect('login')
    else:
        form = SetPasswordForm(user)
    return render(request, 'accounts/password_reset_complete.html', {'form': form})

from django.urls import path
from .views import (
    login_view, signup_view, logout_view,
    password_reset_request_view, password_reset_verify_view, password_reset_complete_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_request_view, name='password_reset_request'),
    path('password-reset/verify/', password_reset_verify_view, name='password_reset_verify'),
    path('password-reset/complete/', password_reset_complete_view, name='password_reset_complete'),
]

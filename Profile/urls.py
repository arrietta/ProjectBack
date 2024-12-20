from django.urls import path

from Profile.views import LoginView, RegisterView, PasswordResetRequestView, PasswordResetConfirmView, \
    send_test_email

urlpatterns = [
    path('api/v1/login/', LoginView.as_view(), name='login'),
    path('api/v1/register/', RegisterView.as_view(), name='register'),
    path('api/v1/password_reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('api/v1/password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path("MailTest/", send_test_email, name="MailTest"),
]

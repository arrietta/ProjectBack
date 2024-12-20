from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from Project import settings
from Profile.serializers import UserSerializer, UserProfileSerializer, RegisterSerializer
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str


class PasswordResetRequestView(APIView):
    """
    Handles password reset request (sends email with reset link)
    """

    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Construct the password reset link
                reset_link = f"{request.scheme}://{request.get_host()}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
                # Send reset email
                send_mail(
                    'Password Reset Request',
                    render_to_string('password_reset_email.html', {'reset_link': reset_link}),
                    'no-reply@example.com',
                    [email],
                )
                return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    Handles the confirmation of the password reset.
    """

    def post(self, request, uidb64, token):
        try:
            # Decode UID and Token
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                # Token is valid, reset the password
                new_password = request.data.get('new_password')
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    return Response({"message": "Password has been successfully reset."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)


def send_test_email(request):
    subject = 'Test Email from Django'
    message = 'This is a test email sent from Django.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['recipient@example.com']  # Replace with actual recipient

    # Sending the email
    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Test email sent successfully!")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user_profile = request.user.profile
        if request.method == 'GET':
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({"access_token": str(refresh.access_token), "refresh_token": str(refresh)})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
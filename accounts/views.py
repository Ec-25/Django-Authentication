from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.shortcuts import redirect
# from django.contrib.auth import login
# from django.contrib.auth.views import PasswordChangeView, FormView
# from django.urls import reverse_lazy

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsAuthenticatedAndTokenValid
from .models import User
from .serializers import (UserRegisterSerializer, VerifyEmailSerializer,
                          UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer,
                          UserPasswordResetSerializer, UserLogoutSerializer, UserDeleteSerializer,
                          UserUpdateSerializer)
from .utils import send_verification_email
# from .forms import (UserRegisterForm, UserLoginForm, UserChangePasswordForm)


# Templates Views
# class UserRegisterView(FormView):
#     form_class = UserRegisterForm
#     template_name = 'accounts/register.html'
#     success_url = reverse_lazy('main-page')

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return super().form_invalid(form)

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('main-page')
#         return super().dispatch(request, *args, **kwargs)


# class UserLoginView(FormView):
#     form_class = UserLoginForm
#     template_name = 'accounts/login.html'
#     success_url = reverse_lazy('main-page')

#     def form_valid(self, form):
#         user = form.get_user()
#         login(self.request, user)
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return super().form_invalid(form)

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('main-page')
#         return super().dispatch(request, *args, **kwargs)


# class UserChangePasswordView(PasswordChangeView):
#     form_class = UserChangePasswordForm
#     template_name = 'accounts/change_password.html'
#     success_url = reverse_lazy('main-page')

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return super().form_invalid(form)

#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect('main-page')
#         return super().dispatch(request, *args, **kwargs)


# Api Views
class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_verification_email(request, serializer.data.get("email"))
            return Response("Successfully registered!", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request):
        serializer = self.serializer_class(
            data={"code": request.GET.get("code")})
        if serializer.is_valid(raise_exception=True):
            return Response("Email verified successfully!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticatedAndTokenValid]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    serializer_class = UserChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                "We have sent you a link to reset your password",
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordVerifyResetView(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    data={"validated_data": False}, status=status.HTTP_401_UNAUTHORIZED
                )

            return Response(data={"validated_data": True}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response(
                data={"validated_data": False}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserPasswordResetView(APIView):
    serializer_class = UserPasswordResetSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Password reset successfully!", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticatedAndTokenValid]
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.id, delete_all=False)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.id, delete_all=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticatedAndTokenValid]
    serializer_class = UserDeleteSerializer

    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticatedAndTokenValid]
    serializer_class = UserUpdateSerializer

    def put(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request}
            )
            serializer.validate(
                request.data, User.objects.get(id=request.user.id))
            serializer.update(User.objects.get(
                id=request.user.id), request.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

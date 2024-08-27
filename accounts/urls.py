from django.urls import path
# from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import PasswordChangeDoneView

# from .views import (UserRegisterView, UserLoginView, UserChangePasswordView)
from .views import (UserRegisterView, VerifyEmail, UserLoginView, UserLogoutView, UserProfileView,
                    UserUpdateView, UserDeleteView, UserChangePasswordView, UserPasswordVerifyResetView, UserPasswordResetView)


# Templates Urls
# urlpatterns = [
#     path('register/', UserRegisterView.as_view(), name='register'),
#     path('login/', UserLoginView.as_view(), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logged_out.html'), name='logout'),
#     path('password/change/', UserChangePasswordView.as_view(),
#          name='password_change'),
#     path('password/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
#     path('password/reset/', auth_views.PasswordResetView.as_view(
#         template_name='accounts/reset_password/password_reset.html',
#         email_template_name='accounts/reset_password/password_reset_email.html',
#         subject_template_name='accounts/reset_password/password_reset_subject.txt'
#     ), name='password_reset'),
#     path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(
#         template_name='accounts/reset_password/password_reset_done.html'
#     ), name='password_reset_done'),
#     path('password/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
#         template_name='accounts/reset_password/password_reset_confirm.html'
#     ), name='password_reset_confirm'),
#     path('password/reset/done/', auth_views.PasswordResetCompleteView.as_view(
#         template_name='accounts/reset_password/password_reset_complete.html'
#     ), name='password_reset_complete'),
# ]


# Api Urls
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("register/verify", VerifyEmail.as_view(), name="verify-email"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/view/", UserProfileView.as_view(), name="profile-view"),
    path("profile/update/", UserUpdateView.as_view(), name="profile-edit"),
    path("profile/delete/", UserDeleteView.as_view(), name="profile-delete"),
    path("password/change/", UserChangePasswordView.as_view(),
         name="user-password-change"),
    path("password/verify/<str:uidb64>/<str:token>/",
         UserPasswordVerifyResetView.as_view(), name="user-password-reset"),
    path("password/reset/", UserPasswordResetView.as_view(),
         name="user-password-reset"),
]

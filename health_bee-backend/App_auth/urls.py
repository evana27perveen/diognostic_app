from django.urls import path

from App_auth.views.password_functionality import ForgotPasswordView, ResetPasswordView
from App_auth.views.authorization_functionality import CustomTokenObtainPairView, CustomTokenRefreshView, CreateUserView


app_name = 'App_auth'

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name="create-user"),
    path('login/', CustomTokenObtainPairView.as_view(), name="login-user"),
    path('login/refresh/', CustomTokenRefreshView.as_view(), name="token-refresh"),
    path('password-reset/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('password-reset/confirm/', ResetPasswordView.as_view(), name="reset-password"),
]
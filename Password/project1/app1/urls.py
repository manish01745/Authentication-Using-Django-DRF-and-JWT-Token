from django.urls import path,include
from app1.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendpasswordResetEmailView,UserPasswordResetView

urlpatterns = [
    path('register',UserRegistrationView.as_view(),name='register'),
    path('login',UserLoginView.as_view(),name='login'),
    path('profile',UserProfileView.as_view(),name='profile'),
    path('change',UserChangePasswordView.as_view(),name='change'),
    path('Sendpassword',SendpasswordResetEmailView.as_view(),name='Sendpassword'),
    path('ResetView/<uid>/<token>',UserPasswordResetView.as_view(),name='ResetView'),
]
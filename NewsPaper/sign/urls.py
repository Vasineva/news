from .views import  BaseRegisterView, upgrade_me, ProfileUpdateView
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('upgrade/', upgrade_me, name='upgrade'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
]
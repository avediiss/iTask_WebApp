# accounts/urls.py
from django.urls import path
from .views import SignUpView, MyLogoutView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', MyLogoutView.as_view(), name='logout'), 
    
]
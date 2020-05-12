from django.urls import path
from .views import SignUpView, LoginView

urlpatterns = [
    path('', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
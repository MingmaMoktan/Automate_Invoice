# accounts/urls.py
from django.urls import path
from .views import SignUpView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('select-plan/<str:plan_type>/', views.update_plan, name='select_plan'),
]
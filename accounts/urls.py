# accounts/urls.py
from django.urls import path
from .views import SignUpView
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('select-plan/<str:plan_type>/', views.update_plan, name='select_plan'),
]
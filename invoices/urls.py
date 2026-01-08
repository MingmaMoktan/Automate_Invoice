from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_invoice, name='upload'),
    path('invoice/<int:pk>/', views.invoice_detail, name='detail'),
]
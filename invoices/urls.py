from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'invoices'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_invoice, name='upload'),
    path('invoice/<int:pk>/', views.invoice_detail, name='detail'),
    path('delete/<int:pk>/', views.delete_invoice, name='delete'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('demo/', views.demo_upload, name='demo_upload')
]

# Only serve media files this way during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
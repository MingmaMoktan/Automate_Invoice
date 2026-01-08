from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts import views as account_views
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Accounts & Authentication
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # 2. Marketing & Static Pages
    path('features/', TemplateView.as_view(template_name='pages/features.html'), name='features'),
    path('pricing/', TemplateView.as_view(template_name='pages/pricing.html'), name='pricing'),
    path('docs/', TemplateView.as_view(template_name='pages/docs.html'), name='docs'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
    path('help/', TemplateView.as_view(template_name='pages/help_center.html'), name='help_center'),
    path('privacy/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy'),
    
    # 3. Plan Selection Logic
    path('pricing/select/<str:plan_type>/', account_views.update_plan, name='select_plan'),

    # 4. Main App Logic (Invoices)
    path('', include('invoices.urls')),
]

# Serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os

def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/<year>/<month>/<filename>
    return f'user_{instance.user.id}/{models.functions.Now().date:%Y/%m}/' + filename

class Invoice(models.Model):
    # 1. OWNERSHIP
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    # 2. THE FILE (Supports PDF, JPG, PNG, CSV, XLSX)
    file = models.FileField(
        upload_to='invoices/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'csv', 'xlsx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 3. EXTRACTED DATA (Common across all formats)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default='USD')

    # 4. TRACKING & STATUS
    STATUS_CHOICES = [
        ('pending', 'Pending Processing'),
        ('processing', 'Processing (OCR/Parsing)'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # To distinguish between OCR-heavy files (Images) and direct Data files (CSV)
    is_structured_data = models.BooleanField(default=False, help_text="True if CSV/Excel, False if PDF/Image")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.vendor_name or 'New Upload'} - {self.uploaded_at.strftime('%Y-%m-%d')}"

    @property
    def filename(self):
        return os.path.basename(self.file.name)
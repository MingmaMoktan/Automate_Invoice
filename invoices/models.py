from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os

# Optional: If you want to use the user_directory_path function, 
# it needs to be defined like this to avoid errors:
def user_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/user_<id>/filename
    return f'user_{instance.user.id}/{filename}'

class Invoice(models.Model):
    # 1. OWNERSHIP
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    # 2. THE FILE
    file = models.FileField(
        upload_to='invoices/%Y/%m/%d/', # Organizes files by date on your server
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'csv', 'xlsx'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 3. EXTRACTED DATA (The fields the AI will try to fill)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Pro Tip: AI often returns dates as strings. 
    # If the date format is messy, a DateField might error. 
    # For now, we use DateField, but be prepared to catch formatting errors in utils.py.
    invoice_date = models.DateField(blank=True, null=True)
    
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default='USD')
    
    # Store the full text for searchability
    raw_text = models.TextField(blank=True, null=True)

    # 4. TRACKING & STATUS
    STATUS_CHOICES = [
        ('pending', 'Pending Processing'),
        ('processing', 'Processing (OCR/Parsing)'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    is_structured_data = models.BooleanField(default=False, help_text="True if CSV/Excel, False if PDF/Image")

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.vendor_name or 'New Upload'} - {self.uploaded_at.strftime('%Y-%m-%d')}"

    @property
    def filename(self):
        return os.path.basename(self.file.name)
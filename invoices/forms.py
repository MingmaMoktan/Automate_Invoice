from django import forms
from .models import Invoice

class InvoiceUploadForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'file-input', 
                'accept': '.pdf,.jpg,.jpeg,.png,.csv,.xlsx'
            }),
        }
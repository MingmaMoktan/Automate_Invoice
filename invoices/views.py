from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import InvoiceUploadForm

def landing_page(request):
    return render(request, 'invoices/landing.html') # Or use the HttpResponse from before

@login_required
def upload_invoice(request):
    if request.method == 'POST':
        form = InvoiceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user  # Link to logged-in user
            invoice.save()
            return redirect('invoices:dashboard') # We will create this next
    else:
        form = InvoiceUploadForm()
    return render(request, 'invoices/upload.html', {'form': form})

@login_required
def dashboard(request):
    invoices = request.user.invoices.all()
    return render(request, 'invoices/dashboard.html', {'invoices': invoices})

from .utils import extract_invoice_data # Import our new brain

@login_required
def upload_invoice(request):
    if request.method == 'POST':
        form = InvoiceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.status = 'processing' # Set status to processing
            invoice.save() # Save the file to the disk first

            # Trigger the AI extraction
            try:
                data = extract_invoice_data(invoice.file.path)
                invoice.vendor_name = data['vendor_name']
                invoice.total_amount = data['total_amount']
                # We could also save the raw_text if you added that field to your model
                invoice.status = 'completed'
            except Exception as e:
                print(f"AI Error: {e}")
                invoice.status = 'failed'
            
            invoice.save() # Save the AI results
            return redirect('invoices:dashboard')
    else:
        form = InvoiceUploadForm()
    return render(request, 'invoices/upload.html', {'form': form})

from .models import Invoice

@login_required
def invoice_detail(request, pk):
    # Fetch the specific invoice or show a 404 error if it doesn't exist
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # This allows the user to manually correct the AI data
        invoice.vendor_name = request.POST.get('vendor')
        invoice.total_amount = request.POST.get('amount')
        # date logic could go here
        invoice.save()
        return redirect('invoices:dashboard')

    return render(request, 'invoices/detail.html', {'invoice': invoice})
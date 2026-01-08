from django.shortcuts import render, redirect
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
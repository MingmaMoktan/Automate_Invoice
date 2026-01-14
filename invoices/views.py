from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import InvoiceUploadForm
from .models import Invoice
from .utils import extract_invoice_data

def landing_page(request):
    return render(request, 'invoices/landing.html')

@login_required
def upload_invoice(request):
    # 1. Define Plan Limits (Matched to your Pricing Page)
    PLAN_LIMITS = {
        'free': 3,
        'starter': 200,
        'advanced': 1000,
        'professional': 3000,
        'enterprise': 999999,
    }

    user_profile = request.user.profile
    current_plan = user_profile.plan
    limit = PLAN_LIMITS.get(current_plan, 3)

    # 2. Calculate usage for the current month
    now = timezone.now()
    usage_count = Invoice.objects.filter(
        user=request.user, 
        uploaded_at__year=now.year, 
        uploaded_at__month=now.month
    ).count()

    # 3. Handle POST Request
    if request.method == 'POST':
        # CHECK LIMITS FIRST
        if usage_count >= limit:
            messages.error(request, f"Usage limit reached for your {current_plan.capitalize()} plan. Please upgrade to upload more.")
            return redirect('pricing')

        form = InvoiceUploadForm(request.POST, request.FILES)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.status = 'processing'
            invoice.save()

            # Trigger AI Extraction
            try:
                data = extract_invoice_data(invoice.file.path)
                invoice.vendor_name = data.get('vendor_name', 'Unknown')
                invoice.total_amount = data.get('total_amount', 0.00)
                invoice.status = 'completed'
            except Exception as e:
                print(f"AI Error: {e}")
                invoice.status = 'failed'
            
            invoice.save()
            return redirect('invoices:dashboard')
    else:
        form = InvoiceUploadForm()

    return render(request, 'invoices/upload.html', {
        'form': form,
        'usage_count': usage_count,
        'limit': limit,
        'remaining': limit - usage_count,
        'is_limited': usage_count >= limit
    })

@login_required
def dashboard(request):
    invoices = request.user.invoices.all().order_by('-uploaded_at')
    return render(request, 'invoices/dashboard.html', {'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    
    if request.method == 'POST':
        invoice.vendor_name = request.POST.get('vendor')
        invoice.total_amount = request.POST.get('amount')
        # ADD THIS LINE:
        invoice.invoice_date = request.POST.get('date') 
        
        invoice.save()
        messages.success(request, "Invoice updated successfully!")
        return redirect('invoices:dashboard')

    return render(request, 'invoices/detail.html', {'invoice': invoice})

@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, "Invoice deleted successfully.")
    return redirect('invoices:dashboard')

import csv
from django.http import HttpResponse

@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, user=request.user)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, "Invoice removed successfully.")
    return redirect('invoices:dashboard')

@login_required
def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="invoices_export_{timezone.now().date()}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Vendor', 'Date', 'Amount', 'Status', 'Uploaded At'])

    invoices = request.user.invoices.all()
    for inv in invoices:
        writer.writerow([inv.vendor_name, inv.invoice_date, inv.total_amount, inv.status, inv.uploaded_at])

    return response

# Demo logic
import uuid
from django.shortcuts import render
from .utils import perform_ai_extraction # Assuming your AI logic is here

def demo_upload(request):
    # Initialize session counter if it doesn't exist
    if 'demo_count' not in request.session:
        request.session['demo_count'] = 0
    
    usage = request.session['demo_count']
    limit = 3
    is_limited = usage >= limit

    if request.method == 'POST' and not is_limited:
        uploaded_file = request.FILES.get('file')
        
        # 1. Perform AI extraction WITHOUT saving to DB
        # We pass the file stream directly to your AI function
        extracted_data = perform_ai_extraction(uploaded_file)
        
        # 2. Increment the session counter
        request.session['demo_count'] += 1
        request.session.modified = True 
        
        # 3. Show the result page with the data (but it's not in the DB!)
        return render(request, 'invoices/demo_result.html', {
            'data': extracted_data,
            'remaining': limit - request.session['demo_count']
        })

    return render(request, 'invoices/demo_upload.html', {
        'usage_count': usage,
        'limit': limit,
        'is_limited': is_limited
    })
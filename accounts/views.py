from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Profile

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def update_plan(request, plan_type):
    # This view updates the plan on the user's profile
    # The URL pattern should be: path('select-plan/<str:plan_type>/', views.update_plan, name='select_plan')
    profile = request.user.profile
    profile.plan = plan_type
    profile.save()
    
    messages.success(request, f"Plan updated to {plan_type.capitalize()} successfully!")
    return redirect('invoices:dashboard')
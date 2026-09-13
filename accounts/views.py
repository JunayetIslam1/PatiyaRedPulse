from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DonorRegistrationForm, DonorUpdateForm
from .models import Donor, DonationHistory

def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Patiya RedPulse.')
            return redirect('dashboard') # রেজিস্ট্রেশনের পর ড্যাশবোর্ডে যাবে
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DonorRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Donor Registration'
    }
    return render(request, 'accounts/register.html', context)

@login_required
def dashboard(request):
    """ইউজার ড্যাশবোর্ড যা রক্তদানের ইতিহাস এবং এলিজিবিলিটি দেখাবে"""
    try:
        donor = request.user.donor
        donations = donor.donations.all() # এটি DonationHistory থেকে ডাটা আনবে
        context = {
            'donor': donor,
            'donations': donations,
            'title': 'Donor Dashboard'
        }
        return render(request, 'accounts/dashboard.html', context)
    except Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found.')
        return redirect('register')

@login_required
def profile(request):
    try:
        donor = request.user.donor
    except Donor.DoesNotExist:
        messages.error(request, 'Donor profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = DonorUpdateForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DonorUpdateForm(instance=donor)
    
    context = {
        'form': form,
        'donor': donor,
        'title': 'My Profile'
    }
    return render(request, 'accounts/profile.html', context)

def donor_list(request):
    blood_group = request.GET.get('blood_group', '')
    district = request.GET.get('district', '')
    upazila = request.GET.get('upazila', '')
    
    donors = Donor.objects.filter(is_active=True) # সব ডোনার দেখাবে ফিল্টারিং এর জন্য
    
    if blood_group:
        donors = donors.filter(blood_group=blood_group)
    if district:
        donors = donors.filter(district__icontains=district)
    if upazila:
        donors = donors.filter(upazila__icontains=upazila)
    
    context = {
        'donors': donors,
        'blood_groups': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
        'selected_blood_group': blood_group,
        'selected_district': district,
        'selected_upazila': upazila,
        'title': 'Find Blood Donors'
    }
    return render(request, 'accounts/donor_list.html', context)

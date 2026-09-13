from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import Donor
from blood_requests.models import BloodRequest


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin panel.')
        return redirect('home')
    
    total_donors = Donor.objects.filter(is_active=True).count()
    available_donors = Donor.objects.filter(is_active=True, availability_status='Available').count()
    total_requests = BloodRequest.objects.filter(is_active=True).count()
    emergency_requests = BloodRequest.objects.filter(is_active=True, emergency_level='Emergency').count()
    
    recent_donors = Donor.objects.filter(is_active=True).order_by('-registration_date')[:10]
    recent_requests = BloodRequest.objects.filter(is_active=True).order_by('-request_date')[:10]
    
    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'total_requests': total_requests,
        'emergency_requests': emergency_requests,
        'recent_donors': recent_donors,
        'recent_requests': recent_requests,
        'title': 'Admin Dashboard'
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def manage_donors(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    donors = Donor.objects.all().order_by('-registration_date')
    
    context = {
        'donors': donors,
        'title': 'Manage Donors'
    }
    return render(request, 'admin_panel/manage_donors.html', context)


@login_required
def toggle_donor_status(request, donor_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    donor = get_object_or_404(Donor, id=donor_id)
    donor.is_active = not donor.is_active
    donor.save()
    
    status = 'activated' if donor.is_active else 'deactivated'
    messages.success(request, f'Donor {donor.full_name} has been {status}.')
    return redirect('manage_donors')


@login_required
def manage_requests(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    requests = BloodRequest.objects.all().order_by('-request_date')
    
    context = {
        'requests': requests,
        'title': 'Manage Blood Requests'
    }
    return render(request, 'admin_panel/manage_requests.html', context)


@login_required
def delete_request(request, request_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('home')
    
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    blood_request.delete()
    messages.success(request, 'Blood request deleted successfully.')
    return redirect('manage_requests')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField
from .forms import BloodRequestForm
from .models import BloodRequest
from accounts.models import Donor

BLOOD_GROUPS_ORDER = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']


def home(request):
    # Bug fix: previously "total_donors" was silently filtered to
    # Available-only donors, and the template's "available_donors" stat
    # was never supplied by the view (always rendered blank/zero).
    total_donors = Donor.objects.filter(is_active=True).count()
    available_donors = Donor.objects.filter(is_active=True, availability_status='Available').count()
    total_requests = BloodRequest.objects.filter(is_active=True).count()
    emergency_requests = BloodRequest.objects.filter(is_active=True, emergency_level='Emergency').count()

    # Feature: blood-group availability breakdown, shown as a small bar
    # chart on the homepage so seekers can see supply at a glance before
    # they even search.
    group_counts = {
        bg: Donor.objects.filter(is_active=True, availability_status='Available', blood_group=bg).count()
        for bg in BLOOD_GROUPS_ORDER
    }
    max_group_count = max(group_counts.values()) if group_counts else 0
    blood_group_breakdown = [
        {
            'group': bg,
            'count': count,
            'percent': round((count / max_group_count) * 100) if max_group_count else 0,
        }
        for bg, count in group_counts.items()
    ]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'total_requests': total_requests,
        'emergency_requests': emergency_requests,
        'blood_group_breakdown': blood_group_breakdown,
        'title': 'Patiya RedPulse - Blood Donor Directory'
    }
    return render(request, 'blood_requests/home.html', context)


def submit_blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.is_active = True
            blood_request.save()
            
            messages.success(request, 'Blood request submitted successfully! We will review it shortly.')
            return redirect('blood_requests_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BloodRequestForm()
    
    context = {
        'form': form,
        'title': 'Submit Blood Request'
    }
    return render(request, 'blood_requests/submit_request.html', context)


def compatibility_guide(request):
    """
    Public, no-login informational tool: an interactive blood-type
    compatibility checker. Pure presentation view — the matching logic
    runs client-side in JS so it works instantly with no server round trip.
    """
    context = {
        'title': 'Blood Compatibility Checker',
        'blood_groups': ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
    }
    return render(request, 'blood_requests/compatibility.html', context)


def blood_requests_list(request):
    # Feature/fix: Emergency requests are now always pinned above Normal
    # ones (previously the list was sorted purely by submission time, so an
    # urgent request could get buried under newer routine ones).
    requests = BloodRequest.objects.filter(is_active=True).annotate(
        _priority=Case(
            When(emergency_level='Emergency', then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by('_priority', '-request_date')

    context = {
        'requests': requests,
        'title': 'Blood Requests'
    }
    return render(request, 'blood_requests/requests_list.html', context)
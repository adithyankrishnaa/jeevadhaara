"""
Views for the Jeevadhara Donor Management System.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from .models import Donor, BLOOD_GROUP_CHOICES
from .forms import DonorRegistrationForm


def home(request):
    """
    Renders the Jeevadhara homepage with statistics, awareness info, and action CTAs.
    """
    total_donors = Donor.objects.count()
    available_donors = Donor.objects.filter(is_available=True).count()
    
    # Blood group breakdown for quick overview
    blood_group_counts = (
        Donor.objects.values('blood_group')
        .annotate(total=Count('id'))
        .order_by('blood_group')
    )
    group_stats = {item['blood_group']: item['total'] for item in blood_group_counts}
    
    # Prepare list of all 8 blood groups with their count
    blood_groups_summary = [
        {
            'code': code,
            'label': label,
            'count': group_stats.get(code, 0)
        }
        for code, label in BLOOD_GROUP_CHOICES
    ]
    
    # Recent donors preview
    recent_donors = Donor.objects.filter(is_available=True).order_by('-created_at')[:4]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'blood_groups_summary': blood_groups_summary,
        'recent_donors': recent_donors,
    }
    return render(request, 'donors/home.html', context)


def register_donor(request):
    """
    Handles donor registration through ModelForm.
    GET: Displays the empty registration form.
    POST: Validates input, saves donor record, sends success message, redirects to donor list.
    """
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save()
            messages.success(
                request,
                f"Thank you, {donor.full_name}! You have been registered successfully as a blood donor ({donor.blood_group})."
            )
            return redirect('donor_list')
        else:
            messages.error(
                request,
                "Please correct the errors in the form below before submitting."
            )
    else:
        form = DonorRegistrationForm(initial={'is_available': True})

    context = {
        'form': form,
        'blood_groups': BLOOD_GROUP_CHOICES,
    }
    return render(request, 'donors/register.html', context)


def donor_list(request):
    """
    Displays donor directory with search by city/name, filter by blood group and availability status.
    """
    queryset = Donor.objects.all().order_by('-created_at')

    # Query parameters
    search_query = request.GET.get('search', '').strip()
    blood_group_filter = request.GET.get('blood_group', '').strip()
    availability_filter = request.GET.get('availability', '').strip()

    # Apply search filter (city or name)
    if search_query:
        queryset = queryset.filter(
            Q(city__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    # Apply blood group filter
    if blood_group_filter:
        queryset = queryset.filter(blood_group=blood_group_filter)

    # Apply availability filter
    if availability_filter == 'available':
        queryset = queryset.filter(is_available=True)
    elif availability_filter == 'unavailable':
        queryset = queryset.filter(is_available=False)

    total_results = queryset.count()
    total_in_db = Donor.objects.count()

    # Distinct cities for quick suggestions/filter
    available_cities = (
        Donor.objects.values_list('city', flat=True)
        .distinct()
        .order_by('city')[:12]
    )

    context = {
        'donors': queryset,
        'blood_groups': BLOOD_GROUP_CHOICES,
        'selected_blood_group': blood_group_filter,
        'selected_search': search_query,
        'selected_availability': availability_filter,
        'total_results': total_results,
        'total_in_db': total_in_db,
        'available_cities': available_cities,
    }
    return render(request, 'donors/donor_list.html', context)

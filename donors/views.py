"""
Views for the Jeevadhara Donor Management System.
Includes both server-rendered Django templates and REST API endpoints for SPA frontend.
"""
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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
        'backend_url': getattr(settings, 'BACKEND_URL', 'http://127.0.0.1:8000'),
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
        'backend_url': getattr(settings, 'BACKEND_URL', 'http://127.0.0.1:8000'),
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
        'backend_url': getattr(settings, 'BACKEND_URL', 'http://127.0.0.1:8000'),
    }
    return render(request, 'donors/donor_list.html', context)


def single_page_app(request):
    """
    Renders the complete interactive Single Page Application (SPA) frontend.
    """
    context = {
        'backend_url': getattr(settings, 'BACKEND_URL', 'http://127.0.0.1:8000'),
    }
    return render(request, 'donors/app.html', context)


# ==========================================
# JSON REST API Endpoints for Frontend (SPA)
# ==========================================

def api_donors_list(request):
    """
    REST API endpoint returning JSON list of registered donors.
    Accepts optional ?district= query parameter.
    """
    district = request.GET.get('district', '').strip()
    queryset = Donor.objects.filter(is_available=True).order_by('-created_at')
    
    if district and district != 'All':
        queryset = queryset.filter(city__iexact=district)

    data = [
        {
            'id': donor.id,
            'name': donor.full_name,
            'bloodGroup': donor.blood_group,
            'contact': donor.phone,
            'district': donor.city,
            'area': donor.address or donor.city,
            'is_available': donor.is_available,
        }
        for donor in queryset
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def api_register_donor(request):
    """
    REST API endpoint to register a new donor via JSON or Form POST.
    Persists data directly into SQLite database.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)

    try:
        if request.content_type == 'application/json':
            payload = json.loads(request.body)
        else:
            payload = request.POST.dict()

        name = payload.get('name', '').strip()
        blood_group = payload.get('bloodGroup', '').strip()
        contact = payload.get('contact', '').strip()
        district = payload.get('district', '').strip()
        area = payload.get('area', '').strip()

        if not name or not blood_group or not contact or not district:
            return JsonResponse({
                'status': 'error',
                'message': 'All required fields (name, bloodGroup, contact, district) must be provided.'
            }, status=400)

        # Create and persist donor in SQLite database
        donor = Donor.objects.create(
            full_name=name,
            email=payload.get('email', f"{name.lower().replace(' ', '.')}@jeevadhaara.org"),
            phone=contact,
            age=int(payload.get('age', 25)),
            gender=payload.get('gender', 'Male'),
            blood_group=blood_group,
            city=district,
            address=area,
            is_available=True,
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Successfully registered as a donor!',
            'donor': {
                'id': donor.id,
                'name': donor.full_name,
                'bloodGroup': donor.blood_group,
                'contact': donor.phone,
                'district': donor.city,
                'area': donor.address,
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

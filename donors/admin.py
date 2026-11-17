"""
Django Admin configuration for Jeevadhara Donor Management System.
"""
from django.contrib import admin
from .models import Donor


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    """
    Administration interface for Donor model with filtering, search, and inline actions.
    """
    list_display = (
        'full_name',
        'blood_group',
        'city',
        'phone',
        'email',
        'age',
        'gender',
        'is_available',
        'created_at',
    )
    list_filter = (
        'blood_group',
        'is_available',
        'gender',
        'city',
        'created_at',
    )
    search_fields = (
        'full_name',
        'city',
        'phone',
        'email',
        'address',
    )
    list_editable = (
        'is_available',
    )
    ordering = (
        '-created_at',
    )
    date_hierarchy = 'created_at'
    list_per_page = 25

    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'gender', 'age', 'blood_group')
        }),
        ('Contact & Location Details', {
            'fields': ('phone', 'email', 'city', 'address')
        }),
        ('Donation Status', {
            'fields': ('is_available',)
        }),
    )

    actions = ['mark_as_available', 'mark_as_unavailable']

    @admin.action(description="Mark selected donors as Available")
    def mark_as_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} donor(s) successfully marked as available.")

    @admin.action(description="Mark selected donors as Unavailable")
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} donor(s) marked as unavailable.")

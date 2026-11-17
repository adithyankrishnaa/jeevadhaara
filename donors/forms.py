"""
Form definitions for Jeevadhara Donor Management System with Tailwind CSS widgets.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Donor

TAILWIND_INPUT_CLASS = "mt-1 block w-full rounded-md border-slate-300 shadow-sm border p-2.5 focus:border-red-500 focus:ring-red-500 transition-colors bg-slate-50 outline-none text-slate-900 text-sm"
TAILWIND_SELECT_CLASS = "mt-1 block w-full rounded-md border-slate-300 shadow-sm border p-2.5 focus:border-red-500 focus:ring-red-500 transition-colors bg-slate-50 outline-none text-slate-900 text-sm"
TAILWIND_CHECKBOX_CLASS = "h-4 w-4 rounded border-slate-300 text-red-600 focus:ring-red-500"


class DonorRegistrationForm(forms.ModelForm):
    """
    ModelForm for registering a new blood donor with clean Tailwind CSS styling.
    """
    class Meta:
        model = Donor
        fields = [
            'full_name',
            'email',
            'phone',
            'age',
            'gender',
            'blood_group',
            'city',
            'address',
            'is_available',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'placeholder': 'e.g. Rahul Nair',
                'required': True,
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'placeholder': 'rahul@example.com',
                'required': True,
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'placeholder': '+91 98765 43210',
                'required': True,
                'autocomplete': 'tel',
            }),
            'age': forms.NumberInput(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'placeholder': '18 - 65',
                'min': '18',
                'max': '65',
                'required': True,
            }),
            'gender': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS,
                'required': True,
            }),
            'blood_group': forms.Select(attrs={
                'class': TAILWIND_SELECT_CLASS,
                'required': True,
            }),
            'city': forms.TextInput(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'placeholder': 'e.g. Ernakulam, Kozhikode, Thiruvananthapuram',
                'required': True,
            }),
            'address': forms.Textarea(attrs={
                'class': TAILWIND_INPUT_CLASS,
                'rows': 2,
                'placeholder': 'e.g. Kakkanad, Marine Drive',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': TAILWIND_CHECKBOX_CLASS,
                'id': 'is_available',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Contact Number',
            'age': 'Age (Years)',
            'gender': 'Gender',
            'blood_group': 'Blood Group',
            'city': 'District / City',
            'address': 'Local Area / Address',
            'is_available': 'I am currently active and available to donate blood upon request',
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 18 or age > 65:
                raise ValidationError("Donors must be between 18 and 65 years of age according to health guidelines.")
        return age

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if len(full_name) < 2:
            raise ValidationError("Please provide a valid full name (at least 2 characters).")
        return full_name

    def clean_city(self):
        city = self.cleaned_data.get('city', '').strip()
        if len(city) < 2:
            raise ValidationError("Please provide a valid district or city name.")
        return city

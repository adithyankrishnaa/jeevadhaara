"""
Form definitions for Jeevadhara Donor Management System.
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Donor


class DonorRegistrationForm(forms.ModelForm):
    """
    ModelForm for registering a new blood donor with Bootstrap 5 widgets and validation.
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
                'class': 'form-control',
                'placeholder': 'e.g. Rahul Sharma',
                'required': True,
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': True,
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210',
                'required': True,
                'autocomplete': 'tel',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age (18 - 65)',
                'min': '18',
                'max': '65',
                'required': True,
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kochi, Bengaluru, Chennai',
                'required': True,
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter street address, locality or landmark (optional)',
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'is_available',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'age': 'Age (Years)',
            'gender': 'Gender',
            'blood_group': 'Blood Group',
            'city': 'City / Town',
            'address': 'Residential Address',
            'is_available': 'I am currently available and willing to donate blood upon request',
        }
        help_texts = {
            'age': 'Eligible donors must be between 18 and 65 years old.',
            'phone': 'Include 10 digits or international dial code (e.g. +91 9876543210).',
            'blood_group': 'Select your medically verified blood group.',
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
            raise ValidationError("Please provide a valid city or locality name.")
        return city

"""
Automated unit and integration tests for Jeevadhara Donor Management System.
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Donor
from .forms import DonorRegistrationForm


class DonorModelTestCase(TestCase):
    def setUp(self):
        self.donor = Donor.objects.create(
            full_name="Abhishek Verma",
            email="abhishek@example.com",
            phone="+91 9876543210",
            age=25,
            gender="Male",
            blood_group="O+",
            city="Kochi",
            address="Panampilly Nagar",
            is_available=True
        )

    def test_donor_str_representation(self):
        self.assertEqual(str(self.donor), "Abhishek Verma (O+) - Kochi")

    def test_blood_group_badge(self):
        self.assertEqual(self.donor.blood_group_badge, "O+")

    def test_default_availability(self):
        donor2 = Donor.objects.create(
            full_name="Kavya Nair",
            email="kavya@example.com",
            phone="9876543211",
            age=30,
            gender="Female",
            blood_group="B+",
            city="Thrissur"
        )
        self.assertTrue(donor2.is_available)


class DonorFormTestCase(TestCase):
    def test_valid_form(self):
        form_data = {
            'full_name': 'Meera Sen',
            'email': 'meera.sen@example.com',
            'phone': '+91 9988776655',
            'age': 28,
            'gender': 'Female',
            'blood_group': 'A+',
            'city': 'Kozhikode',
            'address': 'Beach Road',
            'is_available': True,
        }
        form = DonorRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_age_underage(self):
        form_data = {
            'full_name': 'Minor User',
            'email': 'minor@example.com',
            'phone': '9876543210',
            'age': 16,  # Under 18
            'gender': 'Male',
            'blood_group': 'O+',
            'city': 'Kochi',
            'is_available': True,
        }
        form = DonorRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)

    def test_invalid_age_overage(self):
        form_data = {
            'full_name': 'Senior Citizen',
            'email': 'senior@example.com',
            'phone': '9876543210',
            'age': 72,  # Over 65
            'gender': 'Male',
            'blood_group': 'O+',
            'city': 'Kochi',
            'is_available': True,
        }
        form = DonorRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('age', form.errors)


class DonorViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.donor1 = Donor.objects.create(
            full_name="Arjun Varma",
            email="arjun@test.com",
            phone="9876543210",
            age=27,
            gender="Male",
            blood_group="O+",
            city="Kochi",
            is_available=True
        )
        self.donor2 = Donor.objects.create(
            full_name="Deepika Patel",
            email="deepika@test.com",
            phone="9876543212",
            age=31,
            gender="Female",
            blood_group="A-",
            city="Bengaluru",
            is_available=False
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donors/home.html')
        self.assertEqual(response.context['total_donors'], 2)
        self.assertEqual(response.context['available_donors'], 1)

    def test_donor_registration_get(self):
        response = self.client.get(reverse('register_donor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donors/register.html')
        self.assertIsInstance(response.context['form'], DonorRegistrationForm)

    def test_donor_registration_post_success(self):
        post_data = {
            'full_name': 'Nikhil Nair',
            'email': 'nikhil.n@example.com',
            'phone': '+91 9123456789',
            'age': 24,
            'gender': 'Male',
            'blood_group': 'B+',
            'city': 'Thiruvananthapuram',
            'address': 'Statue Junction',
            'is_available': True,
        }
        response = self.client.post(reverse('register_donor'), post_data)
        # Should redirect to donor list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('donor_list'))
        # Should exist in database
        self.assertTrue(Donor.objects.filter(email='nikhil.n@example.com').exists())

    def test_donor_list_view_all(self):
        response = self.client.get(reverse('donor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donors/donor_list.html')
        self.assertEqual(len(response.context['donors']), 2)

    def test_donor_list_filter_blood_group(self):
        response = self.client.get(reverse('donor_list'), {'blood_group': 'O+'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['donors']), 1)
        self.assertEqual(response.context['donors'][0].full_name, "Arjun Varma")

    def test_donor_list_search_city(self):
        response = self.client.get(reverse('donor_list'), {'search': 'Bengaluru'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['donors']), 1)
        self.assertEqual(response.context['donors'][0].city, "Bengaluru")

    def test_donor_list_empty_search(self):
        response = self.client.get(reverse('donor_list'), {'search': 'NonExistentCityXYZ'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['donors']), 0)
        self.assertEqual(response.context['total_results'], 0)

    def test_single_page_app_view(self):
        response = self.client.get(reverse('single_page_app'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'donors/app.html')

    def test_api_donors_list(self):
        response = self.client.get(reverse('api_donors_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Arjun Varma")

    def test_api_register_donor(self):
        payload = {
            'name': 'Gautam Krishna',
            'bloodGroup': 'AB+',
            'contact': '+91 9447123456',
            'district': 'Kozhikode',
            'area': 'Mavoor Road',
        }
        response = self.client.post(
            reverse('api_register_donor'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Donor.objects.filter(full_name='Gautam Krishna').exists())


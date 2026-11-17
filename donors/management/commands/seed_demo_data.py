"""
Management command to seed realistic demo blood donors into the Jeevadhara database.
Usage: python manage.py seed_demo_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from donors.models import Donor


DEMO_DONORS = [
    {
        'full_name': 'Rahul Sharma',
        'email': 'rahul.sharma@example.com',
        'phone': '+91 98470 12345',
        'age': 28,
        'gender': 'Male',
        'blood_group': 'O+',
        'city': 'Kochi',
        'address': 'Flat 4B, Skyline Riverdale, Edappally',
        'is_available': True,
    },
    {
        'full_name': 'Ananya Menon',
        'email': 'ananya.menon@example.com',
        'phone': '+91 94471 23456',
        'age': 24,
        'gender': 'Female',
        'blood_group': 'A+',
        'city': 'Thiruvananthapuram',
        'address': 'House No. 12, Jawahar Nagar, Kowdiar',
        'is_available': True,
    },
    {
        'full_name': 'Mohammed Fasil',
        'email': 'm.fasil@example.com',
        'phone': '+91 97452 34567',
        'age': 32,
        'gender': 'Male',
        'blood_group': 'B+',
        'city': 'Kozhikode',
        'address': 'Green Valley, Mavoor Road',
        'is_available': True,
    },
    {
        'full_name': 'Sneha Suresh',
        'email': 'sneha.suresh@example.com',
        'phone': '+91 98463 45678',
        'age': 22,
        'gender': 'Female',
        'blood_group': 'AB+',
        'city': 'Thrissur',
        'address': 'Near Round South, Kuruppam Road',
        'is_available': True,
    },
    {
        'full_name': 'Arjun Nair',
        'email': 'arjun.nair@example.com',
        'phone': '+91 94954 56789',
        'age': 35,
        'gender': 'Male',
        'blood_group': 'O-',
        'city': 'Kochi',
        'address': '22/304, Marine Drive Promenade',
        'is_available': True,
    },
    {
        'full_name': 'Deepa Mathew',
        'email': 'deepa.mathew@example.com',
        'phone': '+91 98475 67890',
        'age': 29,
        'gender': 'Female',
        'blood_group': 'A-',
        'city': 'Kottayam',
        'address': 'Rose Villa, Kanjikuzhy',
        'is_available': False,
    },
    {
        'full_name': 'Karthik Raja',
        'email': 'karthik.raja@example.com',
        'phone': '+91 94466 78901',
        'age': 31,
        'gender': 'Male',
        'blood_group': 'B-',
        'city': 'Palakkad',
        'address': 'Shanti Nagar, Fort Maidan Area',
        'is_available': True,
    },
    {
        'full_name': 'Meera Krishnan',
        'email': 'meera.k@example.com',
        'phone': '+91 97477 89012',
        'age': 26,
        'gender': 'Female',
        'blood_group': 'AB-',
        'city': 'Alappuzha',
        'address': 'Canal View Road, Mullakkal',
        'is_available': True,
    },
    {
        'full_name': 'Vikramaditya Roy',
        'email': 'vikram.roy@example.com',
        'phone': '+91 98958 90123',
        'age': 40,
        'gender': 'Male',
        'blood_group': 'O+',
        'city': 'Bengaluru',
        'address': '7th Cross, Indiranagar',
        'is_available': True,
    },
    {
        'full_name': 'Aparna Pillai',
        'email': 'aparna.pillai@example.com',
        'phone': '+91 94969 01234',
        'age': 27,
        'gender': 'Female',
        'blood_group': 'A+',
        'city': 'Kollam',
        'address': 'Beach Road, Asramam',
        'is_available': True,
    },
    {
        'full_name': 'Roshan Paul',
        'email': 'roshan.paul@example.com',
        'phone': '+91 98460 11223',
        'age': 34,
        'gender': 'Male',
        'blood_group': 'B+',
        'city': 'Ernakulam',
        'address': 'MG Road, Jos Junction',
        'is_available': False,
    },
    {
        'full_name': 'Pooja Hegde',
        'email': 'pooja.hegde@example.com',
        'phone': '+91 97451 22334',
        'age': 23,
        'gender': 'Female',
        'blood_group': 'O+',
        'city': 'Bengaluru',
        'address': '4th Block, Koramangala',
        'is_available': True,
    },
]


class Command(BaseCommand):
    help = 'Seeds realistic sample blood donors across various blood groups and locations.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Jeevadhara demo donors..."))
        created_count = 0
        updated_count = 0

        for data in DEMO_DONORS:
            donor, created = Donor.objects.update_or_create(
                email=data['email'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f" [+] Created: {donor.full_name} ({donor.blood_group}) - {donor.city}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f" [~] Updated: {donor.full_name} ({donor.blood_group})"))

        # Ensure demo superuser exists for admin panel access
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@jeevadhara.org', 'admin123')
            self.stdout.write(self.style.SUCCESS(" [+] Created Admin Superuser: username='admin', password='admin123'"))
        else:
            self.stdout.write(self.style.NOTICE(" [i] Admin Superuser 'admin' already exists."))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully seeded demo data: {created_count} added, {updated_count} refreshed. Total donors in DB: {Donor.objects.count()}"
            )
        )

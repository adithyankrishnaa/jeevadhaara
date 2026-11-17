from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# Choice definitions
BLOOD_GROUP_CHOICES = [
    ('A+', 'A+ (A Positive)'),
    ('A-', 'A- (A Negative)'),
    ('B+', 'B+ (B Positive)'),
    ('B-', 'B- (B Negative)'),
    ('AB+', 'AB+ (AB Positive)'),
    ('AB-', 'AB- (AB Negative)'),
    ('O+', 'O+ (O Positive)'),
    ('O-', 'O- (O Negative)'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

# Telephone validation regex: supports optional leading '+', digits, and optional hyphens/spaces
phone_regex = RegexValidator(
    regex=r'^\+?[0-9\s\-]{10,16}$',
    message="Enter a valid phone number with 10 to 15 digits (e.g., +91 9876543210 or 9876543210)."
)


class Donor(models.Model):
    """
    Donor entity model storing comprehensive blood donor information.
    """
    full_name = models.CharField(
        max_length=120,
        verbose_name="Full Name"
    )
    email = models.EmailField(
        max_length=120,
        verbose_name="Email Address"
    )
    phone = models.CharField(
        max_length=20,
        validators=[phone_regex],
        verbose_name="Phone Number"
    )
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Donor must be at least 18 years old."),
            MaxValueValidator(65, message="Donor must be 65 years or younger.")
        ],
        verbose_name="Age (Years)",
        help_text="Eligible blood donor age is between 18 and 65 years."
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male',
        verbose_name="Gender"
    )
    blood_group = models.CharField(
        max_length=5,
        choices=BLOOD_GROUP_CHOICES,
        verbose_name="Blood Group"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="City / Municipality"
    )
    address = models.TextField(
        blank=True,
        default='',
        verbose_name="Full Residential Address"
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name="Available to Donate"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registration Date"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blood Donor"
        verbose_name_plural = "Blood Donors"
        indexes = [
            models.Index(fields=['blood_group'], name='donor_blood_grp_idx'),
            models.Index(fields=['city'], name='donor_city_idx'),
            models.Index(fields=['is_available'], name='donor_avail_idx'),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.blood_group}) - {self.city}"

    @property
    def blood_group_badge(self):
        """Returns clean short blood group name."""
        return self.blood_group

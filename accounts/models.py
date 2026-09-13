from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Donor(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    AVAILABILITY_STATUS = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    district = models.CharField(max_length=50)
    upazila = models.CharField(max_length=50)
    last_donation_date = models.DateField()
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_STATUS, default='Available')
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.blood_group}"
    
    @property
    def days_since_last_donation(self):
        today = timezone.now().date()
        return (today - self.last_donation_date).days

    @property
    def eligibility_gap_days(self):
        """
        Minimum gap required between two donations, per Bangladesh Red
        Crescent / DGHS transfusion guidance: 90 days for male donors,
        120 days for female donors (women need a longer recovery window).
        """
        return 90 if self.gender == 'Male' else 120

    @property
    def is_eligible(self):
        return self.days_since_last_donation >= self.eligibility_gap_days
    
    @property
    def days_until_eligible(self):
        """পরবর্তী রক্তদানের জন্য কতদিন বাকি তা হিসেব করবে"""
        if self.is_eligible:
            return 0
        return self.eligibility_gap_days - self.days_since_last_donation

    @property
    def eligibility_status(self):
        if self.is_eligible:
            return "Eligible to Donate"
        else:
            return f"Not Eligible ({self.days_until_eligible} days remaining)"

    @property
    def donation_count(self):
        return self.donations.count()

    @property
    def lifesaver_tier(self):
        """
        Feature: recognise repeat donors with a simple tier badge, using the
        DonationHistory records that already existed in the data model but
        weren't surfaced anywhere in the UI.
        """
        count = self.donation_count
        if count >= 6:
            return 'gold'
        if count >= 3:
            return 'silver'
        if count >= 1:
            return 'bronze'
        return 'new'
    
    class Meta:
        ordering = ['-registration_date']

class DonationHistory(models.Model):
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    donation_date = models.DateField()
    hospital_name = models.CharField(max_length=200, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.full_name} - {self.donation_date}"

    class Meta:
        ordering = ['-donation_date']

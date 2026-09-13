from django.db import models
from django.utils import timezone


class BloodRequest(models.Model):
    EMERGENCY_LEVELS = [
        ('Normal', 'Normal'),
        ('Emergency', 'Emergency'),
    ]
    
    PATIENT_CONDITIONS = [
        ('Stable', 'Stable'),
        ('Critical', 'Critical'),
        ('Life Threatening', 'Life Threatening'),
        ('Surgery', 'Surgery'),
        ('Accident', 'Accident'),
        ('Maternity', 'Maternity'),
        ('Other', 'Other'),
    ]
    
    BLOOD_GROUPS = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    patient_name = models.CharField(max_length=100)
    required_blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    number_of_bags = models.IntegerField(default=1)
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    patient_condition = models.CharField(max_length=20, choices=PATIENT_CONDITIONS, default='Stable')
    emergency_level = models.CharField(max_length=10, choices=EMERGENCY_LEVELS, default='Normal')
    required_date = models.DateField()
    contact_phone = models.CharField(max_length=15)
    additional_info = models.TextField(blank=True, null=True)
    request_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.required_blood_group} - {self.emergency_level}"
    
    @property
    def is_emergency(self):
        return self.emergency_level == 'Emergency'
    
    class Meta:
        ordering = ['-request_date']
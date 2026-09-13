from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Donor
from django.utils import timezone
from datetime import datetime, date


class DonorRegistrationForm(UserCreationForm):
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
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUPS,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your age',
            'min': '18'
        })
    )
    
    mobile_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your mobile number'
        })
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email (optional)'
        })
    )
    
    district = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your district'
        })
    )
    
    upazila = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your upazila',
            'list': 'patiyaUnions'
        })
    )
    
    last_donation_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    availability_status = forms.ChoiceField(
        choices=[('Available', 'Available'), ('Not Available', 'Not Available')],
        initial='Available',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 18:
            raise forms.ValidationError('You must be 18 years or older to register as a donor.')
        return age

    def clean_mobile_number(self):
        """
        Bug fix: the number was previously accepted in any format, which
        silently broke the one-click "tel:" and WhatsApp ("wa.me/88...")
        links elsewhere in the site. Bangladeshi mobile numbers are 11
        digits starting with 01 (e.g. 01712345678).
        """
        number = self.cleaned_data.get('mobile_number', '').strip().replace(' ', '').replace('-', '')
        if not number.isdigit() or not (number.startswith('01') and len(number) == 11):
            raise forms.ValidationError('Enter a valid 11-digit Bangladeshi mobile number, e.g. 01712345678.')
        return number
    
    def clean_last_donation_date(self):
        last_donation_date = self.cleaned_data.get('last_donation_date')
        if last_donation_date:
            if last_donation_date > date.today():
                raise forms.ValidationError('Last donation date cannot be in the future.')
        return last_donation_date
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            donor = Donor.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                blood_group=self.cleaned_data['blood_group'],
                gender=self.cleaned_data['gender'],
                age=self.cleaned_data['age'],
                mobile_number=self.cleaned_data['mobile_number'],
                email=self.cleaned_data.get('email', ''),
                district=self.cleaned_data['district'],
                upazila=self.cleaned_data['upazila'],
                last_donation_date=self.cleaned_data['last_donation_date'],
                availability_status=self.cleaned_data['availability_status']
            )
        return user


class DonorUpdateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['full_name', 'blood_group', 'gender', 'age', 'mobile_number', 
                 'email', 'district', 'upazila', 'last_donation_date', 'availability_status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '18'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control', 'list': 'patiyaUnions'}),
            'last_donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'availability_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_mobile_number(self):
        number = self.cleaned_data.get('mobile_number', '').strip().replace(' ', '').replace('-', '')
        if not number.isdigit() or not (number.startswith('01') and len(number) == 11):
            raise forms.ValidationError('Enter a valid 11-digit Bangladeshi mobile number, e.g. 01712345678.')
        return number
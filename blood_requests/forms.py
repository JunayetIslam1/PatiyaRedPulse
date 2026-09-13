from django import forms
from .models import BloodRequest
from django.utils import timezone
from datetime import date


class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'required_blood_group', 'number_of_bags', 
                 'hospital_name', 'hospital_address', 'patient_condition', 'emergency_level', 
                 'required_date', 'contact_phone', 'additional_info']
        
        widgets = {
            'patient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient name'
            }),
            'required_blood_group': forms.Select(attrs={
                'class': 'form-control'
            }),
            'number_of_bags': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'hospital_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital name'
            }),
            'hospital_address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital address',
                'rows': 3
            }),
            'patient_condition': forms.Select(attrs={
                'class': 'form-control'
            }),
            'emergency_level': forms.Select(attrs={
                'class': 'form-control'
            }),
            'required_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact phone number'
            }),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional information (optional)',
                'rows': 3,
                'required': False
            }),
        }
    
    def clean_required_date(self):
        required_date = self.cleaned_data.get('required_date')
        if required_date:
            if required_date < date.today():
                raise forms.ValidationError('Required date cannot be in the past.')
        return required_date

    def clean_contact_phone(self):
        """Same tel:/WhatsApp-safe format check as the donor's mobile number."""
        number = self.cleaned_data.get('contact_phone', '').strip().replace(' ', '').replace('-', '')
        if not number.isdigit() or not (number.startswith('01') and len(number) == 11):
            raise forms.ValidationError('Enter a valid 11-digit Bangladeshi mobile number, e.g. 01712345678.')
        return number

    def clean_number_of_bags(self):
        bags = self.cleaned_data.get('number_of_bags')
        if bags is not None and bags < 1:
            raise forms.ValidationError('Number of bags must be at least 1.')
        return bags
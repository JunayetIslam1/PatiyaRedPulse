from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'required_blood_group', 'patient_condition', 'number_of_bags', 
                   'hospital_name', 'emergency_level', 'required_date', 
                   'contact_phone', 'request_date', 'is_active']
    list_filter = ['emergency_level', 'patient_condition', 'required_blood_group', 'is_active', 'request_date']
    search_fields = ['patient_name', 'hospital_name', 'contact_phone']
    list_editable = ['is_active']
    
    def is_emergency(self, obj):
        return obj.is_emergency
    is_emergency.boolean = True
    is_emergency.short_description = 'Emergency'
from django.contrib import admin
from .models import Donor, DonationHistory

class DonationHistoryInline(admin.TabularInline):
    model = DonationHistory
    extra = 1  # নতুন ইতিহাস যোগ করার জন্য কয়টি খালি ঘর দেখাবে

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'blood_group', 'mobile_number', 'district', 'upazila', 
                    'last_donation_date', 'eligibility_status', 'availability_status', 'is_active']
    list_filter = ['blood_group', 'availability_status', 'is_active', 'district']
    search_fields = ['full_name', 'mobile_number', 'district', 'upazila']
    list_editable = ['availability_status', 'is_active']
    readonly_fields = ['registration_date', 'get_eligibility_status']
    
    inlines = [DonationHistoryInline]
    
    def get_eligibility_status(self, obj):
        return obj.eligibility_status
    get_eligibility_status.short_description = 'Eligibility Status'

@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ('donor', 'donation_date', 'hospital_name')
    list_filter = ('donation_date',)
    search_fields = ('donor__full_name', 'hospital_name')

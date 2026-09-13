from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('donors/', views.manage_donors, name='manage_donors'),
    path('donors/toggle/<int:donor_id>/', views.toggle_donor_status, name='toggle_donor_status'),
    path('requests/', views.manage_requests, name='manage_requests'),
    path('requests/delete/<int:request_id>/', views.delete_request, name='delete_request'),
]
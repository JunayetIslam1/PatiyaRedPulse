from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit-request/', views.submit_blood_request, name='submit_blood_request'),
    path('blood-requests/', views.blood_requests_list, name='blood_requests_list'),
    path('compatibility/', views.compatibility_guide, name='compatibility_guide'),
]
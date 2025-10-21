from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),  # Main attendance page
    path('mark/', views.mark_attendance, name='mark_attendance'),  # Mark attendance
    path('farmers/', views.farmer_list, name='farmer_list'),  # List farmers
    path('farmers/add/', views.farmer_create, name='farmer_create'),  # Add farmer
    path('farmers/json/', views.get_farmers_json, name='farmers_json'),  # Get farmers as JSON
]

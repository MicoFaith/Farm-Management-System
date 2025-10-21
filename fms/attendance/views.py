
from django.shortcuts import render, redirect
from django.utils import timezone
from django.core import serializers
from django.http import JsonResponse
from .models import Farmer, Attendence
from .forms import FarmerForm, AttendenceForm

def get_farmers_json(request):
    farmers = Farmer.objects.all()
    data = serializers.serialize('json', farmers)
    return JsonResponse({'farmers': data}, safe=False)

def farmer_list(request):
    farmers = Farmer.objects.all()
    return render(request, 'attendance/farmer_list.html', {'farmers': farmers})

def farmer_create(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmer_list')
    else:
        form = FarmerForm()
    return render(request, 'attendance/farmer_form.html', {'form': form})

def attendance_list(request):
    date = request.GET.get('date', timezone.now().date())
    if isinstance(date, str):
        date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
    
    records = Attendence.objects.filter(date=date).select_related('farmer')
    farmers = Farmer.objects.all()
    
    # Create a dictionary of farmer attendance status
    attendance_dict = {record.farmer_id: record.present for record in records}
    
    # Prepare data for template
    farmer_attendance = []
    for farmer in farmers:
        farmer_attendance.append({
            'farmer': farmer,
            'present': attendance_dict.get(farmer.id, None)
        })
    
    context = {
        'date': date,
        'farmer_attendance': farmer_attendance,
    }
    return render(request, 'attendance/attendance_list.html', context)

def mark_attendance(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        if not date:
            return render(request, 'attendance/mark_attendance.html', {
                'farmers': Farmer.objects.all(),
                'date': timezone.now().date(),
                'error': 'Date is required'
            })
            
        try:
            selected_date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            
            # Check if the selected date is today or in the past
            if selected_date > timezone.now().date():
                return render(request, 'attendance/mark_attendance.html', {
                    'farmers': Farmer.objects.all(),
                    'date': selected_date,
                    'error': 'Cannot mark attendance for future dates'
                })
                
            # Check if attendance for this date has already been marked
            attendance_exists = Attendence.objects.filter(date=selected_date).exists()
            if attendance_exists:
                return render(request, 'attendance/mark_attendance.html', {
                    'farmers': Farmer.objects.all(),
                    'date': selected_date,
                    'error': f'Attendance for {selected_date} has already been marked'
                })
            
            # Get all farmers
            farmers = Farmer.objects.all()
            
            from django.db import transaction
            try:
                with transaction.atomic():
                    # Create attendance records
                    for farmer in farmers:
                        checkbox_name = f'farmer_{farmer.id}'
                        is_present = checkbox_name in request.POST
                        
                        # Create new attendance record
                        Attendence.objects.create(
                            farmer=farmer,
                            date=selected_date,
                            present=is_present
                        )
                
                return redirect('attendance_list')
                
            except Exception as e:
                return render(request, 'attendance/mark_attendance.html', {
                    'farmers': farmers,
                    'date': selected_date,
                    'error': f'Error saving attendance: {str(e)}'
                })
                
        except ValueError:
            return render(request, 'attendance/mark_attendance.html', {
                'farmers': Farmer.objects.all(),
                'date': timezone.now().date(),
                'error': 'Invalid date format'
            })
    
    context = {
        'farmers': Farmer.objects.all(),
        'date': timezone.now().date(),
    }
    return render(request, 'attendance/mark_attendance.html', context)
    
    context = {
        'farmers': Farmer.objects.all(),
        'date': timezone.now().date(),
    }
    return render(request, 'attendance/mark_attendance.html', context)

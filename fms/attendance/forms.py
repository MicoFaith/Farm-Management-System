from django import forms
from .models import Farmer, Attendence

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'farm', 'gender', 'contract_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter farmer name'}),
            'farm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter farm name'}),
            'gender': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'contract_type': forms.Select(attrs={'class': 'form-control'}),
        }

class AttendenceForm(forms.ModelForm):
    class Meta:
        model = Attendence
        fields = ['farmer', 'date', 'present']

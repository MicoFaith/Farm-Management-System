from django.utils import timezone
from django.db import models

# Create your models here.

class Farmer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    CONTRACT_CHOICES = [
        ('casual', 'Casual'),
        ('contract', 'Contract'),
    ]
    
    name = models.CharField(max_length=100)
    farm = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    contract_type = models.CharField(max_length=10, choices=CONTRACT_CHOICES, default='casual')
  
    class Meta:
        db_table = "farmer"

    def __str__(self):
        return f"{self.name} - {self.farm} ({self.get_contract_type_display()})"

class Attendence(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=False)

    class Meta:
        db_table = "attendance"

    def __str__(self):
        return f"{self.farmer.name} - {self.date} - {'Present' if self.present else 'Absent'}"
    pass
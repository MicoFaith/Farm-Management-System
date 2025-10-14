from django.utils import timezone
from django.db import models

# Create your models here.

class Farmer(models.Model):
    name = models.CharField(max_length=100)
    farm = models.CharField(max_length=50)
  
    class Meta:
        db_table = "farmer"

    def __str__(self):
        return f"{self.name} - {self.farm}"
pass

class Attendence(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=False)

    class Meta:
        db_table = "attendance"

    def __str__(self):
        return f"{self.farmer.name} - {self.date} - {'Present' if self.present else 'Absent'}"
    pass
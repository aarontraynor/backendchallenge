from django.db import models
from django.core.validators import MaxValueValidator
from datetime import datetime

# Create your models here.
class Branch(models.Model):
    """Database model for branches in the system"""
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8)

    def __str__(self):
        """Return a String representation of the branch"""
        return city + ", " + postcode


class Driver(models.Model):
    """Database model for drivers in the system"""
    first_name = models.CharField(max_length=50)
    middle_names = models.CharField(max_length=255)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        """Return a String representation of the driver"""
        return self.first_name + " " + self.middle_names + " " + self.last_name


class Car(models.Model):
    """Database model for cars in the system"""
    car_make = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50)
    year_of_manufacture = models.PositiveIntegerField(
        # Ensure that the year of manufacture is not later than the current year
        validators=[MaxValueValidator(datetime.now().year),]
    )
    at_branch = models.BooleanField(default=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)

    def __str(self):
        """Return a String representation of the car"""
        return self.car_make + " " + self.car_model + ", " + year_of_manufacture

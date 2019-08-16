from django.db import models
from django.core.validators import MaxValueValidator
from django.conf import settings
from datetime import datetime

# Create your models here.
class Branch(models.Model):
    """Database model for branches in the system"""
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=8)

    def __str__(self):
        """Return a String representation of the branch"""
        return self.city + ", " + self.postcode


class Driver(models.Model):
    """Database model for drivers in the system"""
    first_name = models.CharField(max_length=50)
    middle_names = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()

    def __str__(self):
        """Return a String representation of the driver"""
        if(self.middle_names == None):
            return f'{self.first_name} {self.last_name}'
        else:
         return f'{self.first_name} {self.middle_names} {self.last_name}'


class Car(models.Model):
    """Database model for cars in the system"""
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year_of_manufacture = models.PositiveIntegerField(
        # Ensure that the year of manufacture is not later than the current year
        validators=[MaxValueValidator(datetime.now().year),]
    )

    def __str__(self):
        """Return a String representation of the car"""
        return f'ID: {self.id} ({self.make} {self.model}, {self.year_of_manufacture})'

class BranchInventory(models.Model):
    """Database model for associations between a car and the branch it is located at"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)

    def __str__(self):
        """Return a String representation of the car/branch association"""
        return f'{self.car} is at {self.branch}'

class DriverInventory(models.Model):
    """Database model for associations between a car and the driver that is in posession of it"""
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)

    def __str__(self):
        """Return a String representation of the car/driver association"""
        return f'{self.car} is with {self.driver}'

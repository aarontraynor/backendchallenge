from rest_framework import serializers

from carmanagement_api import models

class CarSerializer(serializers.ModelSerializer):
    """Serializes a car object"""

    class Meta:
        model = models.Car
        fields = ('id', 'make', 'model', 'year_of_manufacture')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class BranchSerializer(serializers.ModelSerializer):
    """Serializes a branch object"""

    class Meta:
        model = models.Branch
        fields = ('id', 'city', 'postcode')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class DriverSerializer(serializers.ModelSerializer):
    """Serializes a driver object"""

    class Meta:
        model = models.Driver
        fields = ('id', 'first_name', 'middle_names', 'last_name', 'date_of_birth')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

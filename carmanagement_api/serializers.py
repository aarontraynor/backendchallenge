from rest_framework import serializers

from carmanagement_api import models

class CarSerializer(serializers.ModelSerializer):
    """Serializes a car object"""

    class Meta:
        model = models.Car
        fields = ('id', 'make', 'model', 'year_of_manufacture', 'currently_with_type', 'currently_with_id')
        extra_kwargs = {
            'id': {'read_only': True},
            'currently_with_type': {'read_only': True},
            'currently_with_id': {'read_only': True}
        }


class BranchSerializer(serializers.ModelSerializer):
    """Serializes a branch object"""

    class Meta:
        model = models.Branch
        fields = ('id', 'city', 'postcode', 'capacity')
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

class BranchInventorySerializer(serializers.ModelSerializer):
    """"Serializes an association between a Car and a Branch"""

    class Meta:
        model = models.BranchInventory
        fields = ('id', 'car', 'branch')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class DriverInventorySerializer(serializers.ModelSerializer):
    """Serializes an association between a Car and a Driver"""

    class Meta:
        model = models.DriverInventory
        fields = ('id', 'car', 'driver')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

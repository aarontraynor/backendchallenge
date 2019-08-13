from rest_framework import serializers

from carmanagement_api import models

class CarSerializer(serializers.ModelSerializer):
    """Serializes a car object"""

    class Meta:
        model = models.Car
        fields = ('id', 'car_make', 'car_model', 'year_of_manufacture', 'at_branch')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        car = models.Car.objects.create_user(
            car_make = validated_data['car_make'],
            car_model = validated_data['car_model'],
            year_of_manufacture = validated_data['year_of_manufacture']
        )

        return car

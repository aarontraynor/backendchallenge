from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

from carmanagement_api import serializers
from carmanagement_api import models


class CarViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating cars in the system"""

    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('make', 'model', 'year_of_manufacture')

class BranchViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating branches in the system"""

    serializer_class = serializers.BranchSerializer
    queryset = models.Branch.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city', 'postcode')

class DriverViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating drivers in the system"""

    serializer_class = serializers.DriverSerializer
    queryset = models.Driver.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'middle_names', 'last_name', 'date_of_birth')

class BranchInventoryViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating associations between cars and branches"""

    serializer_class = serializers.BranchInventorySerializer
    queryset = models.BranchInventory.objects.all()

class DriverInventoryViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating associations between cars and drivers"""

    serializer_class = serializers.DriverInventorySerializer
    queryset = models.DriverInventory.objects.all()

    def create(self, request):
        """Remove a Car from a Branch and assign it to a Driver"""
        serializer = self.serializer_class(data=request.data)

        # Confirm that the given input is valid and return an error if not
        if serializer.is_valid():
            car = serializer.validated_data['car']
            driver = serializer.validated_data['driver']

            # Only proceed if the car is not already assigned to a driver
            if(models.DriverInventory.objects.filter(car=car).count() == 0):
                # Remove the car from the branch's inventory
                models.BranchInventory.objects.filter(car=car).delete()

                # Assign the car to the driver
                models.DriverInventory.objects.create(
                    car = car,
                    driver = driver
                )

                # Return a message to confirm that the association has been successfully added
                return Response({'message': f'Car {car} has been assigned to Driver {driver}'})
            else:
                # Inform the user that the car is already assigned to a driver
                current_driver = models.DriverInventory.objects.get(car=car).driver
                return Response({'error': f'Car {car} is already assigned to {current_driver}'}, status.HTTP_400_BAD_REQUEST)
        else:
            # Return the error that occurred
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

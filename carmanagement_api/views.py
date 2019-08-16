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

    def list(self, request):
        """Return a list of cars as a JSON that includes the currently_with information"""
        car_json = []

        # Create a new Dictionary for each car
        for c in models.Car.objects.all():
            currently_with_json = {}

            # Determine if currently_with is of type Branch or Driver and set attribute accordingly
            if type(c.currently_with) == models.Branch:
                currently_with_json.update({
                    'id': c.currently_with.id,
                    'city': c.currently_with.city,
                    'postcode': c.currently_with.postcode,
                })
            elif type(c.currently_with) == models.Driver:
                currently_with_json.update({
                    'id': c.currently_with.id,
                    'first_name': c.currently_with.first_name,
                    'middle_names': c.currently_with.middle_names,
                    'last_name': c.currently_with.last_name,
                    'date_of_birth': c.currently_with.date_of_birth
                })

            # Append the current car to the list
            car_json.append({
                'id': c.id,
                'make': c.make,
                'model': c.model,
                'year_of_manufacture': c.year_of_manufacture,
                'currently_with': currently_with_json
            })
        return Response(car_json)


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

    def create(self, request):
        """Remove a Car from a Driver and assign it to a Branch"""
        serializer = self.serializer_class(data=request.data)

        # Confirm that the given input is valid and return an error if not
        if serializer.is_valid():
            car = serializer.validated_data['car']
            branch = serializer.validated_data['branch']

            # Only proceed if the car is not already with a branch
            if(models.BranchInventory.objects.filter(car=car).count() == 0):
                # Remove the car from the driver's inventory
                models.DriverInventory.objects.filter(car=car).delete()

                # Assign the car to the branch
                models.BranchInventory.objects.create(
                    car = car,
                    branch = branch
                )
                car.currently_with=branch
                car.save()
                #models.Car.objects.filter(id=car.id).update(currently_with=models.Branch.objects.get(id=branch.id))

                # Return a message to confirm that the association has been successfully added
                return Response({'message': f'Car {car} has been returned to {branch}'})
            else:
                # Inform the user that the car is already assigned to a branch
                current_branch = models.BranchInventory.objects.get(car=car).branch
                return Response({'error': f'Car {car} is already with the branch {current_branch}'}, status.HTTP_400_BAD_REQUEST)
        else:
            # Return the error that occurred
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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

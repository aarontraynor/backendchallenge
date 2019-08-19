from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

from carmanagement_api import serializers
from carmanagement_api import models

import requests


class CarViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating cars in the system"""
    # Setup
    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('make', 'model', 'year_of_manufacture')

    def list(self, request):
        """Custom list implementation to correctly show Cars with currently_with attribute"""

        # Arrays used to store results
        query_results = None
        cars_json = []

        # Get all cars if no search parameter is provided, or get only matching cars if there is one given
        if request.query_params.get('search') == None:
            # Get all cars in the database
            query_results = models.Car.objects.all()
        else:
            # Get all cars in the database that match the search string given in either the make, model or year of manufacture
            search_str = request.query_params.get('search')
            query_results = models.Car.objects.filter(Q(make__contains=search_str) | Q(model__contains=search_str) | Q(year_of_manufacture__contains=search_str))

        # Generate a dict for each car
        for c in list(query_results):
            cars_json = cars_json + [self.get_car_as_json(c),]

        # Return the response as JSON
        return Response({"cars": cars_json})

    def retrieve(self, request, pk=None):
        """Custom retrieve implementation to correctly show a Car with currently_with attribute"""
        c = models.Car.objects.get(pk=pk)
        return Response(self.get_car_as_json(c))

    def get_car_as_json(self, c):
        """Creates a dict used to show a given Car as JSON"""

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
        else:
            currently_with_json.update({
                'message': 'Currently unassigned. Please assign this car to a Branch or Driver'
            })

        return {
            'id': c.id,
            'make': c.make,
            'model': c.model,
            'year_of_manufacture': c.year_of_manufacture,
            'currently_with': currently_with_json
        }


class BranchViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating branches in the system"""
    # Setup
    serializer_class = serializers.BranchSerializer
    queryset = models.Branch.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('city', 'postcode')

    def create(self, request):
        """Custom implementation of create method to include postcode validation"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            city = serializer.validated_data['city']
            postcode = serializer.validated_data['postcode']
            capacity = None
            response_json = requests.get(f'https://api.postcodes.io/postcodes/{postcode}/validate').json()

            try:
                capacity = serializer.validated_data['capacity']
            except:
                capacity = -1

            if response_json['status'] == 200:
                if response_json['result'] == True:
                    if capacity == -1:
                        branch = models.Branch.objects.create(
                            city = city,
                            postcode = postcode
                        )
                    else:
                        branch = models.Branch.objects.create(
                            city = city,
                            postcode = postcode,
                            capacity = capacity
                        )

                    return Response({'message': f'A branch in {branch} was created successfully.'})
                else:
                    return Response({'postcode': 'An invalid postcode was given.'}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'postcode': 'There was an error validating your postcode. Please try again later.'}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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
    http_method_names = ['get', 'post', 'head']

    def create(self, request):
        """Remove a Car from a Driver and assign it to a Branch"""
        serializer = self.serializer_class(data=request.data)

        # Confirm that the given input is valid and return an error if not
        if serializer.is_valid():
            car = serializer.validated_data['car']
            branch = serializer.validated_data['branch']

            # Only proceed if the car is not already with a branch
            if(models.BranchInventory.objects.filter(car=car).count() == 0):
                if branch.capacity > models.BranchInventory.objects.filter(branch=branch).count():
                    # Remove the car from the driver's inventory
                    models.DriverInventory.objects.filter(car=car).delete()

                    # Assign the car to the branch
                    models.BranchInventory.objects.create(
                        car = car,
                        branch = branch
                    )

                    # Update the Car's currently_with attribute
                    car.currently_with = branch
                    car.save()

                    # Return a message to confirm that the association has been successfully added
                    return Response({'message': f'Car {car} has been returned to {branch}'}, status.HTTP_201_CREATED)
                else:
                    return Response({'error': f'The branch {branch} is currently at full capacity.'}, status.HTTP_400_BAD_REQUEST)
            else:
                # Inform the user that the car is already assigned to a branch
                current_branch = models.BranchInventory.objects.get(car=car).branch
                models.BranchInventory.objects.filter(car=car).delete()

                models.BranchInventory.objects.create(
                    car = car,
                    branch = branch
                )

                car.currently_with = branch
                car.save()

                return Response({'message': f'Car {car} has been moved from {current_branch} to {branch}'}, status.HTTP_201_CREATED)
        else:
            # Return the error that occurred
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class DriverInventoryViewSet(viewsets.ModelViewSet):
    """Handle creating, viewing and updating associations between cars and drivers"""

    serializer_class = serializers.DriverInventorySerializer
    queryset = models.DriverInventory.objects.all()
    http_method_names = ['get', 'post', 'head']

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

                # Update the Car's currently_with attribute
                car.currently_with=driver
                car.save()

                # Return a message to confirm that the association has been successfully added
                return Response({'message': f'Car {car} has been assigned to Driver {driver}'}, status.HTTP_201_CREATED)
            else:
                # Inform the user that the car is already assigned to a driver
                current_driver = models.DriverInventory.objects.get(car=car).driver
                return Response({'error': f'Car {car} is already assigned to {current_driver}'}, status.HTTP_400_BAD_REQUEST)
        else:
            # Return the error that occurred
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

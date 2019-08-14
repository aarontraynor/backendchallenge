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

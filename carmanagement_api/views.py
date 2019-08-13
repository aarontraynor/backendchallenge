from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from carmanagement_api import serializers
from carmanagement_api import models


class TestViewSet(viewsets.ViewSet):
    """API ViewSet for Cars in the system"""

    def list(self, request):
        """Return an initial message"""

        return Response({'message': 'Hello!'})

class CarViewSet(viewsets.ModelViewSet):
    """Handle creating viewing and updating cars in the system"""

    serializer_class = serializers.CarSerializer
    queryset = models.Car.objects.all()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


class CarViewSet(viewsets.ViewSet):
    """API ViewSet for Cars in the system"""

    def list(self, request):
        """Return an initial message"""

        return Response({'message': 'Hello!'})

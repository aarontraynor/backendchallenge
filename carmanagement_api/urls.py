from django.urls import path, include
from rest_framework.routers import DefaultRouter

from carmanagement_api import views

# Create a router and register views
router = DefaultRouter()
router.register('cars', views.CarViewSet)
router.register('branches', views.BranchViewSet)
router.register('drivers', views.DriverViewSet)
router.register('branch-inventory', views.BranchInventoryViewSet)
router.register('driver-inventory', views.DriverInventoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlantViewSet, BedPlantViewSet

router = DefaultRouter()
router.register(r'plant', PlantViewSet)
router.register(r'bedplant', BedPlantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FertilizerViewSet, BedPlantFertilizerViewSet

router = DefaultRouter()
router.register(r'fertilizers', FertilizerViewSet)
router.register(r'bedplantfertilizers', BedPlantFertilizerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

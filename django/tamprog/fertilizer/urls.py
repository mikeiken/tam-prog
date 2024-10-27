from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FertilizerViewSet, BedPlantFertilizerViewSet

router = DefaultRouter()
router.register(r'fertilizer', FertilizerViewSet)
router.register(r'bedfertilizer', BedPlantFertilizerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, BedViewSet

router = DefaultRouter()
router.register(r'field', FieldViewSet)
router.register(r'bed', BedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

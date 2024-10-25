
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, BedViewSet

router = DefaultRouter()
router.register(r'fields', FieldViewSet)
router.register(r'beds', BedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

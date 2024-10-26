from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, AgronomistViewSet, WorkerViewSet

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'agronomists', AgronomistViewSet)
router.register(r'workers', WorkerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

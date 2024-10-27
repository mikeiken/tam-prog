from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, AgronomistViewSet, WorkerViewSet
from django.urls import path
from .views import RegisterViewSet, LoginView

router = DefaultRouter()
router.register(r'person', PersonViewSet)
router.register(r'agronomists', AgronomistViewSet)
router.register(r'workers', WorkerViewSet)
router1 = DefaultRouter()
router1.register(r'register', RegisterViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router1.urls)),
    path('login/', LoginView.as_view(), name='login'),
]

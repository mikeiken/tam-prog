from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, WorkerViewSet
from django.urls import path
from .views import RegisterViewSet, LoginView

router = DefaultRouter()
router.register(r'person', PersonViewSet)
router.register(r'worker', WorkerViewSet)
router_reg = DefaultRouter()
router_reg.register(r'register', RegisterViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_reg.urls)),
    path('login/', LoginView.as_view(), name='login'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, WorkerViewSet
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'person', PersonViewSet)
router.register(r'worker', WorkerViewSet)
router_reg = DefaultRouter()
router_reg.register(r'register', RegisterViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_reg.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

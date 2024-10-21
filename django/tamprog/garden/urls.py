from django.urls import path, include
from rest_framework import routers
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

schema_view = SpectacularAPIView.as_view()

router_agronomist = routers.SimpleRouter()
router_agronomist.register(r'agronomist', AgronomistViewSet)

router_supplier = routers.SimpleRouter()
router_supplier.register(r'supplier', SupplierViewSet)

router_worker = routers.SimpleRouter()
router_worker.register(r'worker', WorkerViewSet)

router_garden = routers.SimpleRouter()
router_garden.register(r'garden', GardenBedViewSet)

router_fertilizer = routers.SimpleRouter()
router_fertilizer.register(r'fertilizer', FertilizerViewSet)

router_user = routers.SimpleRouter()
router_user.register(r'user', UserViewSet)

router_plant = routers.SimpleRouter()
router_plant.register(r'plant', PlantViewSet)

router_plot = routers.SimpleRouter()
router_plot.register(r'plot', PlotViewSet)

router_order = routers.SimpleRouter()
router_order.register(r'order', OrderViewSet)

router_available_plants = routers.SimpleRouter()
router_available_plants.register(r'availableplants', AvailablePlantsViewSet)

urlpatterns = [
    path('', include(router_agronomist.urls)),
    path('', include(router_supplier.urls)),
    path('', include(router_worker.urls)),
    path('', include(router_garden.urls)),
    path('', include(router_fertilizer.urls)),
    path('', include(router_user.urls)),
    path('', include(router_plant.urls)),
    path('', include(router_plot.urls)),
    path('', include(router_order.urls)),
    path('', include(router_available_plants.urls)),
    path('api/schema/', schema_view, name='schema'),  # URL для схемы
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path, include
from rest_framework import routers

from .views import *

from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

schema_view = SpectacularAPIView.as_view()

router_agronomist = routers.SimpleRouter()
router_agronomist.register(r'agronomist', AgronomistViewSet)

router_supplier = routers.SimpleRouter()
router_supplier.register(r'supplier', SupplierViewSet)

router_worker = routers.SimpleRouter()
router_worker.register(r'worker', WorkerViewSet)

router_garden = routers.SimpleRouter()
router_garden.register(r'garden', GardenBedViewSet)

router_fertilizer = routers.SimpleRouter()
router_fertilizer.register(r'fertilizer', FertilizerViewSet)

router_user = routers.SimpleRouter()
router_user.register(r'user', UserViewSet)

router_plant = routers.SimpleRouter()
router_plant.register(r'plant', PlantViewSet)

router_plot = routers.SimpleRouter()
router_plot.register(r'plot', PlotViewSet)

router_order = routers.SimpleRouter()
router_order.register(r'order', OrderViewSet)

router_available_plants = routers.SimpleRouter()
router_available_plants.register(r'availableplants', AvailablePlantsViewSet)
urlpatterns = [
    path('', include(router_agronomist.urls)),
    path('', include(router_supplier.urls)),
    path('', include(router_worker.urls)),
    path('', include(router_garden.urls)),
    path('', include(router_fertilizer.urls)),
    path('', include(router_user.urls)),
    path('', include(router_plant.urls)),
    path('', include(router_plot.urls)),
    path('', include(router_order.urls)),
    path('', include(router_available_plants.urls)),
    path('api/schema/', schema_view, name='schema'),  # URL для схемы
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # ReDoc
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
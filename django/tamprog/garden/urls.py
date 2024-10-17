from django.urls import path, include
from rest_framework import routers

from .views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="Electronic agronomist",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zarembiczkiy@mail.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
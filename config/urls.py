from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from warehouse.views import WarehouseCalculationView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Asosiy hisoblash API (ikkala qulay URL orqali ham ishlaydi)
    path('api/calculate/', WarehouseCalculationView.as_view(), name='api-calculate-direct'),
    path('api/v1/', include('warehouse.urls')),

    # Swagger va OpenAPI Hujjatlari (Talab bo'yicha)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

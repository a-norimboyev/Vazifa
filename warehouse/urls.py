from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'materials', views.MaterialViewSet, basename='material')
router.register(r'warehouse-stock', views.WarehouseViewSet, basename='warehouse')

urlpatterns = [
    path('calculate/', views.WarehouseCalculationView.as_view(), name='warehouse-calculate'),
    path('', include(router.urls)),
]

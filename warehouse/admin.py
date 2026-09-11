from django.contrib import admin
from .models import Product, Material, ProductMaterial, Warehouse


class ProductMaterialInline(admin.TabularInline):
    model = ProductMaterial
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_code']
    search_fields = ['product_name', 'product_code']
    inlines = [ProductMaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'material_name']
    search_fields = ['material_name']


@admin.register(ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'material', 'quantity']
    list_filter = ['product', 'material']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['id', 'material', 'remainder', 'price']
    list_filter = ['material']
    ordering = ['id']

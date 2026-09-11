from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse


# --- Model Serializers (CRUD / Admin ko'rish uchun) ---

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']


class ProductMaterialSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.material_name', read_only=True)

    class Meta:
        model = ProductMaterial
        fields = ['id', 'product', 'material', 'material_name', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    materials = ProductMaterialSerializer(source='product_materials', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code', 'materials']


class WarehouseSerializer(serializers.ModelSerializer):
    material_name = serializers.CharField(source='material.material_name', read_only=True)

    class Meta:
        model = Warehouse
        fields = ['id', 'material', 'material_name', 'remainder', 'price']


# --- Request & Response Serializers (Vazifadagi API uchun) ---

class ProductOrderInputSerializer(serializers.Serializer):
    product_code = serializers.CharField(
        help_text="Mahsulot kodi (masalan: 238923)"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Ishlab chiqarilishi kerak bo'lgan mahsulot miqdori (masalan: 30)"
    )


class ProductMaterialOutputSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField(
        allow_null=True,
        help_text="Ombor partiyasi ID raqami (agar yetishmasa null)"
    )
    material_name = serializers.CharField(
        help_text="Xomashyo nomi"
    )
    qty = serializers.FloatField(
        help_text="Ushbu partiyadan olinadigan miqdor"
    )
    price = serializers.FloatField(
        allow_null=True,
        help_text="Partiyadagi xomashyo narxi (agar yetishmasa null)"
    )


class ProductResultOutputSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    product_qty = serializers.IntegerField()
    product_materials = ProductMaterialOutputSerializer(many=True)


class WarehouseCalculationResponseSerializer(serializers.Serializer):
    result = ProductResultOutputSerializer(many=True)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import (
    ProductSerializer,
    MaterialSerializer,
    WarehouseSerializer,
    ProductOrderInputSerializer,
    WarehouseCalculationResponseSerializer
)
from .services import calculate_warehouse_materials


class WarehouseCalculationView(APIView):
    """
    Mahsulotlar va ularning miqdorlari bo'yicha omborxonadan xomashyolarni hisoblash API.
    """

    @extend_schema(
        request=ProductOrderInputSerializer(many=True),
        responses={200: WarehouseCalculationResponseSerializer},
        summary="Omborxonadan xomashyo hisoblash (FIFO)",
        description="Mahsulot kodi va miqdori yuborilganda, ombordagi partiyalardan qoldiqni kamaytirmasdan FIFO bo'yicha hisoblab beradi.",
        examples=[
            OpenApiExample(
                name="Misol so'rov (List formatida)",
                summary="Ikki xil mahsulot (Ko'ylak va Shim) uchun so'rov",
                value=[
                    {"product_code": "238923", "quantity": 30},
                    {"product_code": "498723", "quantity": 20}
                ],
                request_only=True
            ),
            OpenApiExample(
                name="Misol so'rov (Bitta mahsulot)",
                summary="Faqat bitta mahsulot uchun so'rov",
                value={"product_code": "238923", "quantity": 10},
                request_only=True
            ),
            OpenApiExample(
                name="Muvaffaqiyatli javob",
                summary="Kutilayotgan hisob-kitob natijasi",
                value={
                    "result": [
                        {
                            "product_name": "Koylak",
                            "product_qty": 30,
                            "product_materials": [
                                {"warehouse_id": 1, "material_name": "Mato", "qty": 12, "price": 1500},
                                {"warehouse_id": 2, "material_name": "Mato", "qty": 12, "price": 1600},
                                {"warehouse_id": 5, "material_name": "Tugma", "qty": 150, "price": 300},
                                {"warehouse_id": 3, "material_name": "Ip", "qty": 40, "price": 500},
                                {"warehouse_id": 4, "material_name": "Ip", "qty": 260, "price": 550}
                            ]
                        },
                        {
                            "product_name": "Shim",
                            "product_qty": 20,
                            "product_materials": [
                                {"warehouse_id": 2, "material_name": "Mato", "qty": 28, "price": 1600},
                                {"warehouse_id": 4, "material_name": "Ip", "qty": 40, "price": 550},
                                {"warehouse_id": None, "material_name": "Ip", "qty": 260, "price": None},
                                {"warehouse_id": 6, "material_name": "Zamok", "qty": 20, "price": 2000}
                            ]
                        }
                    ]
                },
                response_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        raw_data = request.data

        # Ma'lumotlarni ro'yxat (list) shakliga keltiramiz
        if isinstance(raw_data, dict):
            if "products" in raw_data and isinstance(raw_data["products"], list):
                orders = raw_data["products"]
            else:
                orders = [raw_data]
        elif isinstance(raw_data, list):
            orders = raw_data
        else:
            return Response(
                {"error": "Noto'g'ri so'rov formati. JSON ro'yxat yoki obyekt yuboring."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not orders:
            return Response({"result": []}, status=status.HTTP_200_OK)

        calculation_result = calculate_warehouse_materials(orders)
        return Response(calculation_result, status=status.HTTP_200_OK)


# --- Qo'shimcha CRUD ViewSetlar (Ma'lumotlarni ko'rish va boshqarish uchun) ---

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().prefetch_related('product_materials__material')
    serializer_class = ProductSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class WarehouseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Warehouse.objects.all().select_related('material')
    serializer_class = WarehouseSerializer

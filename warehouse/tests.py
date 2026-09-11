from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from warehouse.models import Product, Material, ProductMaterial, Warehouse


class WarehouseCalculationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Materiallar
        self.mato = Material.objects.create(material_name="Mato")
        self.ip = Material.objects.create(material_name="Ip")
        self.tugma = Material.objects.create(material_name="Tugma")
        self.zamok = Material.objects.create(material_name="Zamok")

        # Mahsulotlar: Koylak (238923)
        self.koylak = Product.objects.create(product_name="Koylak", product_code="238923")
        ProductMaterial.objects.create(product=self.koylak, material=self.mato, quantity=0.8)
        ProductMaterial.objects.create(product=self.koylak, material=self.tugma, quantity=5.0)
        ProductMaterial.objects.create(product=self.koylak, material=self.ip, quantity=10.0)

        # Mahsulotlar: Shim (498723)
        self.shim = Product.objects.create(product_name="Shim", product_code="498723")
        ProductMaterial.objects.create(product=self.shim, material=self.mato, quantity=1.4)
        ProductMaterial.objects.create(product=self.shim, material=self.ip, quantity=15.0)
        ProductMaterial.objects.create(product=self.shim, material=self.zamok, quantity=1.0)

        # Omborxona partiyalari (1 dan 6 gacha)
        Warehouse.objects.create(id=1, material=self.mato, remainder=12.0, price=1500.0)
        Warehouse.objects.create(id=2, material=self.mato, remainder=200.0, price=1600.0)
        Warehouse.objects.create(id=3, material=self.ip, remainder=40.0, price=500.0)
        Warehouse.objects.create(id=4, material=self.ip, remainder=300.0, price=550.0)
        Warehouse.objects.create(id=5, material=self.tugma, remainder=500.0, price=300.0)
        Warehouse.objects.create(id=6, material=self.zamok, remainder=1000.0, price=2000.0)

    def test_warehouse_calculation_exact_mock_output(self):
        """Topshiriqdagi misol so'rov natijasi bilan 100% bir xil chiqishini tekshirish"""
        request_payload = [
            {"product_code": "238923", "quantity": 30},
            {"product_code": "498723", "quantity": 20}
        ]

        response = self.client.post('/api/calculate/', data=request_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_response = {
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
        }

        self.assertEqual(response.json(), expected_response)

        # Bazadagi ombor qoldiqlari o'zgarmaganligini tekshirish
        w1 = Warehouse.objects.get(id=1)
        self.assertEqual(w1.remainder, 12.0)

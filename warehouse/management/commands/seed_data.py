from django.core.management.base import BaseCommand
from warehouse.models import Product, Material, ProductMaterial, Warehouse


class Command(BaseCommand):
    help = "Omborxona vazifasi uchun namunaviy ma'lumotlarni bazaga kiritish (Seed data)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Eski ma'lumotlar tozalanmoqda..."))
        ProductMaterial.objects.all().delete()
        Warehouse.objects.all().delete()
        Product.objects.all().delete()
        Material.objects.all().delete()

        # 1. Materiallar (Xomashyolar)
        self.stdout.write("Materiallar yaratilmoqda...")
        mato = Material.objects.create(material_name="Mato")
        ip = Material.objects.create(material_name="Ip")
        tugma = Material.objects.create(material_name="Tugma")
        zamok = Material.objects.create(material_name="Zamok")

        # 2. Mahsulotlar (Products)
        self.stdout.write("Mahsulotlar va retseptlar yaratilmoqda...")
        koylak = Product.objects.create(product_name="Koylak", product_code="238923")
        # 1 dona Ko'ylak uchun: 0.8 m² mato, 5 ta tugma, 10 m ip
        ProductMaterial.objects.create(product=koylak, material=mato, quantity=0.8)
        ProductMaterial.objects.create(product=koylak, material=tugma, quantity=5.0)
        ProductMaterial.objects.create(product=koylak, material=ip, quantity=10.0)

        shim = Product.objects.create(product_name="Shim", product_code="498723")
        # 1 dona Shim uchun: 1.4 m² mato, 15 m ip (20 dona uchun 300 m), 1 ta zamok
        ProductMaterial.objects.create(product=shim, material=mato, quantity=1.4)
        ProductMaterial.objects.create(product=shim, material=ip, quantity=15.0)
        ProductMaterial.objects.create(product=shim, material=zamok, quantity=1.0)

        # 3. Omborxona (Warehouse partiyalari)
        self.stdout.write("Omborxona partiyalari kiritilmoqda...")
        Warehouse.objects.create(id=1, material=mato, remainder=12.0, price=1500.0)
        Warehouse.objects.create(id=2, material=mato, remainder=200.0, price=1600.0)
        Warehouse.objects.create(id=3, material=ip, remainder=40.0, price=500.0)
        Warehouse.objects.create(id=4, material=ip, remainder=300.0, price=550.0)
        Warehouse.objects.create(id=5, material=tugma, remainder=500.0, price=300.0)
        Warehouse.objects.create(id=6, material=zamok, remainder=1000.0, price=2000.0)

        self.stdout.write(self.style.SUCCESS("Barcha namunaviy ma'lumotlar muvaffaqiyatli kiritildi!"))

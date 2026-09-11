from django.db import models


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    product_code = models.CharField(max_length=50, unique=True, verbose_name="Mahsulot kodi")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"

    def __str__(self):
        return f"{self.product_name} ({self.product_code})"


class Material(models.Model):
    material_name = models.CharField(max_length=255, verbose_name="Xomashyo nomi")

    class Meta:
        verbose_name = "Xomashyo"
        verbose_name_plural = "Xomashyolar"

    def __str__(self):
        return self.material_name


class ProductMaterial(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_materials",
        verbose_name="Mahsulot"
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="product_materials",
        verbose_name="Xomashyo"
    )
    quantity = models.FloatField(verbose_name="Kerakli miqdor")

    class Meta:
        verbose_name = "Mahsulot xomashyosi"
        verbose_name_plural = "Mahsulot xomashyolari"
        unique_together = ('product', 'material')

    def __str__(self):
        return f"{self.product.product_name} -> {self.material.material_name}: {self.quantity}"


class Warehouse(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="warehouses",
        verbose_name="Xomashyo"
    )
    remainder = models.FloatField(verbose_name="Qoldiq miqdori")
    price = models.FloatField(verbose_name="Kelgan narxi")

    class Meta:
        verbose_name = "Ombor partiyasi"
        verbose_name_plural = "Ombor partiyalari"
        ordering = ['id']  # FIFO bo'yicha tartiblanishi uchun id bo'yicha

    def __str__(self):
        return f"Partiya #{self.id}: {self.material.material_name} - Qoldiq: {self.remainder}, Narx: {self.price}"

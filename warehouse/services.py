from .models import Product, Warehouse


def calculate_warehouse_materials(orders):
    """
    Mahsulotlar va ularning miqdorlari ro'yxatini qabul qilib,
    ombordagi xomashyolarni FIFO (partiyalar tartibi) bo'yicha hisoblaydi.
    
    Diqqat: Bazadagi ma'lumotlar o'zgarmaydi (remainder ayirib qo'yilmaydi),
    hisoblash xotiradagi nusxa (in-memory) orqali amalga oshiriladi.
    """
    # 1. Ombordagi barcha partiyalarni xotiraga yuklab olamiz
    warehouses = list(Warehouse.objects.select_related('material').filter(remainder__gt=0).order_by('id'))
    
    # Har bir partiyaning qoldig'ini xotirada saqlaymiz: {warehouse_id: current_balance}
    warehouse_stock = {w.id: float(w.remainder) for w in warehouses}

    result = []

    for order in orders:
        product_code = str(order.get('product_code', '')).strip()
        quantity = int(order.get('quantity', 0))

        if not product_code or quantity <= 0:
            continue

        try:
            product = Product.objects.prefetch_related('product_materials__material').get(product_code=product_code)
        except Product.DoesNotExist:
            continue

        product_result = {
            "product_name": product.product_name,
            "product_qty": quantity,
            "product_materials": []
        }

        # Ushbu mahsulot uchun kerak bo'lgan xomashyolarni ko'rib chiqamiz
        for pm in product.product_materials.all().order_by('id'):
            material = pm.material
            needed_qty = float(pm.quantity) * quantity

            # Ushbu materialga tegishli ombor partiyalarini topamiz
            material_batches = [w for w in warehouses if w.material_id == material.id]

            for batch in material_batches:
                current_available = warehouse_stock.get(batch.id, 0.0)

                if current_available > 0 and needed_qty > 0:
                    take = min(needed_qty, current_available)
                    warehouse_stock[batch.id] -= take
                    needed_qty -= take

                    # Butun son bo'lsa int, aks holda float ko'rinishida formatlash
                    formatted_qty = int(take) if take.is_integer() else round(take, 2)
                    formatted_price = int(batch.price) if float(batch.price).is_integer() else round(float(batch.price), 2)

                    product_result["product_materials"].append({
                        "warehouse_id": batch.id,
                        "material_name": material.material_name,
                        "qty": formatted_qty,
                        "price": formatted_price
                    })

                if needed_qty <= 0:
                    break

            # Agar partiyalardan keyin ham yetmay qolsa
            if needed_qty > 0:
                formatted_qty = int(needed_qty) if needed_qty.is_integer() else round(needed_qty, 2)
                product_result["product_materials"].append({
                    "warehouse_id": None,
                    "material_name": material.material_name,
                    "qty": formatted_qty,
                    "price": None
                })

        result.append(product_result)

    return {"result": result}

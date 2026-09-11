# Omborxona Tizimi – Mock Task (Warehouse REST API)

Ishlab chiqarish korxonasida mahsulot ishlab chiqarish uchun kerak boʻlgan xomashyolarni omborxona partiyalaridan **FIFO (First-In, First-Out)** usulida hisoblash va yetishmayotgan xomashyolarni aniqlash uchun yaratilgan **Django Rest Framework (DRF)** REST API loyihasi.

---

## 🛠 Texnologiyalar
- **Python 3**
- **Django 5.2+**
- **Django Rest Framework (DRF)**
- **drf-spectacular (Swagger UI / OpenAPI 3.0)**
- **SQLite3**

---

## 🏗 Maʼlumotlar bazasi modellari
1. **`Product`**: Mahsulotlar (`product_name`, `product_code`).
2. **`Material`**: Xomashyolar (`material_name`).
3. **`ProductMaterial`**: 1 dona mahsulot uchun kerakli xomashyo miqdori (`product_id`, `material_id`, `quantity`).
4. **`Warehouse`**: Ombordagi partiyalar (`material_id`, `remainder`, `price`).

> ⚠️ **Muhim qoida**: Hisob-kitob jarayonida omborxona bazasidagi `remainder` qiymati oʻzgarmaydi. Barcha hisoblashlar xotiradagi nusxa (in-memory) asosida amalga oshiriladi.

---

## 🚀 Loyihani oʻrnatish va ishga tushirish

1. **Bogʻliqliklarni oʻrnatish**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Migratsiyalarni bajarish**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Namunaviy maʼlumotlarni bazaga yuklash (Seed Data)**:
   ```bash
   python manage.py seed_data
   ```

4. **Testlarni ishga tushirish**:
   ```bash
   python manage.py test
   ```

5. **Serverni ishga tushirish**:
   ```bash
   python manage.py runserver
   ```

---

## 📡 API Endpointlar

### 1. Asosiy hisoblash API (Asosiy Vazifa)
- **URL**: `POST /api/calculate/` (yoki `/api/v1/calculate/`)
- **Headers**: `Content-Type: application/json`

#### 📥 Misol soʻrov (Request Body):
```json
[
  { "product_code": 238923, "quantity": 30 },
  { "product_code": 498723, "quantity": 20 }
]
```

#### 📤 Kutilgan javob (Response Body):
```json
{
  "result": [
    {
      "product_name": "Koylak",
      "product_qty": 30,
      "product_materials": [
        {
          "warehouse_id": 1,
          "material_name": "Mato",
          "qty": 12,
          "price": 1500
        },
        {
          "warehouse_id": 2,
          "material_name": "Mato",
          "qty": 12,
          "price": 1600
        },
        {
          "warehouse_id": 5,
          "material_name": "Tugma",
          "qty": 150,
          "price": 300
        },
        {
          "warehouse_id": 3,
          "material_name": "Ip",
          "qty": 40,
          "price": 500
        },
        {
          "warehouse_id": 4,
          "material_name": "Ip",
          "qty": 260,
          "price": 550
        }
      ]
    },
    {
      "product_name": "Shim",
      "product_qty": 20,
      "product_materials": [
        {
          "warehouse_id": 2,
          "material_name": "Mato",
          "qty": 28,
          "price": 1600
        },
        {
          "warehouse_id": 4,
          "material_name": "Ip",
          "qty": 40,
          "price": 550
        },
        {
          "warehouse_id": null,
          "material_name": "Ip",
          "qty": 260,
          "price": null
        },
        {
          "warehouse_id": 6,
          "material_name": "Zamok",
          "qty": 20,
          "price": 2000
        }
      ]
    }
  ]
}
```

---

## 📖 Swagger va API Hujjatlari
Server ishga tushirilgach:
- **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## 🧪 Postman Kolleksiyasi
Loyiha ildizidagi `Omborxona_API.postman_collection.json` faylini toʻgʻridan-toʻgʻri Postman dasturiga **Import** qilib, APIʼni sinab koʻrishingiz mumkin.

# PythonCLIAndStoreProject

A command-line inventory and stock management program written in Python. Product data is stored in a JSON file, so your inventory is kept between sessions.

> The program's interface is in Turkish.

## Features

- **List all products**: shown as a table with ID, name, category, stock, price and line value (stock × price)
- **Add a new product**: IDs are assigned automatically, and inputs are validated (stock can't be negative, price must be greater than zero)
- **Search by name**: case-insensitive partial matching that handles Turkish characters correctly (`ı`, `I`, `i`, `İ`)
- **Update stock and price** of an existing product by its ID
- **Delete a product** by its ID
- **Critical stock report**: lists products with fewer than 5 items in stock
- **Total inventory value**: the sum of stock × price across all products
- **Auto-save**: every change is written to `envanter.json` immediately
- **Data protection**: if `envanter.json` is corrupted, it is backed up as `envanter_bozuk.json` instead of being overwritten

Prices can be entered with either a dot or a comma (`12.5` or `12,5`).

## Requirements

- Python **3.10 or newer** (the program uses `match` statements)
- No external libraries. Only the Python standard library is used.

## Running the program

```bash
git clone https://github.com/<your-username>/PythonCLIAndStoreProject.git
cd PythonCLIAndStoreProject
python envanter.py
```

On first run, an empty `envanter.json` file is created automatically.

## Usage

When the program starts, this menu appears:

```
========================================
     DEPO VE STOK YÖNETİM SİSTEMİ
========================================
1. Tüm Ürünleri Listele
2. Yeni Ürün Ekle
3. Ürün Ara (İsme Göre)
4. Stok ve Fiyat Güncelle
5. Ürün Sil
6. Kritik Stok Raporu (< 5)
7. Toplam Envanter Değeri
0. Kaydet ve Çıkış
========================================
```

| Option | What it does |
|---|---|
| 1 | List all products |
| 2 | Add a new product |
| 3 | Search products by name |
| 4 | Update stock and price |
| 5 | Delete a product |
| 6 | Critical stock report (stock < 5) |
| 7 | Total inventory value |
| 0 | Save and exit |

Example product list:

```
ID   Ad                   Kategori          Stok      Fiyat   Satır Değeri
--------------------------------------------------------------------------
1    Kalem                Kırtasiye            7      12.50          87.50
2    İpek kumaş           Tekstil             10      50.00         500.00
```

## Data format

Products are stored in `envanter.json` as a list:

```json
[
  {
    "id": 1,
    "ad": "Kalem",
    "kategori": "Kırtasiye",
    "stok": 7,
    "fiyat": 12.5
  }
]
```

## About

As a third-year university student, this is the first Python project I've completed.

## Author

**Aybars Alper**
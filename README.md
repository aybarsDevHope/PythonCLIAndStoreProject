# PythonCLIAndStoreProject

An inventory and stock management program written in Python. You can use it in two ways: as an interactive command-line program, or as a REST API built with Flask. Both use the same JSON file, so your inventory is kept between sessions.

> The program's interface and API messages are in Turkish.

## Features

### Command-line program

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

### REST API

- The same operations over HTTP, with JSON requests and responses
- **Input validation**: missing fields, wrong types, negative stock and non-positive prices are rejected with a `400` error and a clear message
- **Consistent errors**: every error is returned as `{"hata": "..."}` with the correct status code (`400` or `404`)

## Requirements

- Python **3.10 or newer** (the program uses `match` statements)
- [Flask](https://flask.palletsprojects.com/) for the API. The command-line program only uses the Python standard library.

## Installation

```bash
git clone https://github.com/aybarsDevHope/PythonCLIAndStoreProject.git
cd PythonCLIAndStoreProject
pip install -r requirements.txt
```

On first run, an empty `envanter.json` file is created automatically if it doesn't exist.

## Using the command-line program

```bash
python main.py
```

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

## Using the API

```bash
python api.py
```

The server runs at `http://127.0.0.1:5000`.

### Endpoints

| Method | Endpoint | What it does | Success |
|---|---|---|---|
| `GET` | `/urunler` | List all products | `200` |
| `GET` | `/urunler/<id>` | Get one product | `200` |
| `POST` | `/urunler` | Add a new product | `201` |
| `PUT` | `/urunler/<id>` | Update a product's stock and price | `200` |
| `DELETE` | `/urunler/<id>` | Delete a product | `200` |
| `GET` | `/rapor/kritik` | Products with stock below 5 | `200` |
| `GET` | `/rapor/toplam` | Total inventory value | `200` |

### Validation rules

| Field | Rule | Required for |
|---|---|---|
| `ad` | Non-empty text | `POST` |
| `kategori` | Text | `POST` |
| `stok` | Whole number, 0 or greater | `POST`, `PUT` |
| `fiyat` | Number greater than 0 | `POST`, `PUT` |

### Examples

**Add a product**

```bash
curl -X POST http://127.0.0.1:5000/urunler \
  -H "Content-Type: application/json" \
  -d '{"ad": "Silgi", "kategori": "Kırtasiye", "stok": 20, "fiyat": 7.5}'
```

```json
{"id": 2, "ad": "Silgi", "kategori": "Kırtasiye", "stok": 20, "fiyat": 7.5}
```

**Update stock and price**

```bash
curl -X PUT http://127.0.0.1:5000/urunler/2 \
  -H "Content-Type: application/json" \
  -d '{"stok": 15, "fiyat": 8}'
```

**Total inventory value**

```bash
curl http://127.0.0.1:5000/rapor/toplam
```

```json
{"toplam": 207.5, "mesaj": "Toplam envanter değeri: 207.50 TL"}
```

**Error examples**

A request with missing fields returns `400`:

```json
{"hata": "Eksik alan(lar): kategori, stok, fiyat"}
```

A product that doesn't exist returns `404`:

```json
{"hata": "999 numaralı ürün bulunamadı"}
```

> On Windows PowerShell, use `curl.exe` instead of `curl`, write each command on a single line, and escape the quotes inside the JSON (`\"ad\"`). Alternatively, use a tool like Postman or Thunder Client.

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

## Project structure

```
PythonCLIAndStoreProject/
├── main.py            # Command-line program and shared functions
├── api.py             # Flask REST API
├── envanter.json      # Product data
├── requirements.txt   # Dependencies
└── README.md
```

## About

As a third-year university student, this is the first Python project I've completed.

## Author

**Aybars Alper**
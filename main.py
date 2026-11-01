import json
import math
import os
from json import JSONDecodeError
def printMenu():
    print("""========================================
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
========================================""")

def load():
    try:
        with open("envanter.json",encoding="utf_8") as file:
            items = json.load(file)
            return items
    except FileNotFoundError:
        with open("envanter.json", "w",encoding="utf_8") as file:
            file.write("[]")
            return []
    except JSONDecodeError:
        os.replace("envanter.json", "envanter_bozuk.json")
        print("UYARI: envanter.json bozuktu, envanter_bozuk.json olarak yedeklendi.")
        return []

def yeniID(item):
    if not item:
        return 1

    return max(urun["id"] for urun in item) + 1

def tr_lower(s):
    return s.replace("I", "ı").replace("İ", "i").lower()

def tr_capitalize(s):
    if not s:
        return s
    ilk = {"i": "İ", "ı": "I"}.get(s[0], s[0].upper())
    return ilk + tr_lower(s[1:])

def printItems(item):
    if not item:
        print("Kayıtlı ürün bulunamadı")
        return

    print(f"{'ID':<4} {'Ad':<20} {'Kategori':<15} {'Stok':>6} {'Fiyat':>10} {'Satır Değeri':>14}")
    print("-" * 74)
    for urun in item:
        satir_degeri = urun["stok"] * urun["fiyat"]
        print(f"{urun['id']:<4} {urun['ad']:<20} {urun['kategori']:<15} "
              f"{urun['stok']:>6} {urun['fiyat']:>10.2f} {satir_degeri:>14.2f}")

    print("\n")

def addItem(item):
    while True:
        try:
            ad = tr_capitalize(input("Ürün adı giriniz: ").strip())
            if ad == "":
                print("Lütfen ad giriniz.")
                continue
            kategori = str(input("Kategori giriniz: "))
            stok = int(input("Stok giriniz: "))
            fiyat = float(input("Fiyat giriniz: ").replace(",", "."))

            if stok < 0:
                print("Lütfen sıfır veya sıfırdan büyük bir değer giriniz.")
                continue
            if not math.isfinite(fiyat) or fiyat <= 0:
                print("Lütfen sıfırdan büyük bir değer giriniz.")
                continue

        except ValueError:
            print("İşlemde hata meydana geldi.Lütfen geçerli değerler giriniz.")
            continue

        list = {
                "id": yeniID(item),
                "ad": ad,
                "kategori": kategori,
                "stok": stok,
                "fiyat": fiyat
            }
        item.append(list)
        print("Başarıyla Eklendi.")
        save(item)
        break

def searchItem(item):

        ad = tr_lower(input("Lütfen aradığınız ürünün adını yazınız: ").strip())
        if ad == "":
            return
        bul = False
        for list in item:
            if ad in tr_lower(list["ad"]):
                bul = True
                print(list)
                print("Ürün bulundu.")

        if not bul:
            print("Ürün bulunamadı.")

def updateStockAndPrice(item):
    tempList = None
    while True:
        try:
            id = int(input("Lütfen değiştirmek istediğiniz ürünün id numarasını giriniz: "))
            for list in item:
                if list["id"] == id:
                    tempList = list
                    print("Bulundu")
                    break

        except ValueError:
            print("Lütfen bir sayı giriniz.")
            continue

        if tempList is None:
            print("Bulunamadı.")
            return

        break

    print(tempList)
    while True:
        try:
            yeniStok = int(input("Lütfen yeni stoku giriniz: "))
            yeniFiyat = float(input("Lütfen yeni fiyat giriniz: ").replace(",", "."))

            if yeniStok >= 0 and math.isfinite(yeniFiyat) and yeniFiyat > 0:
                break
            else:
                print("Stok sıfır veya sıfırdan büyük, fiyat sıfırdan büyük olmak zorunda.")
        except ValueError:
            print("Lütfen değer giriniz.")
            continue

    tempList["stok"] = yeniStok
    tempList["fiyat"] = yeniFiyat
    print("Başarıyla güncellendi.")

    save(item)


def deleteItem(item):
    if not item:
        print("Listede herhangi bir ürün yok.")
        return
    try:
        id = int(input("Lütfen kaldırmak istediğiniz ürünün id numarasını giriniz: "))
    except ValueError:
        print("Lütfen numara değeri giriniz.")
        return
    for list in item:
        if list["id"] == id:
            item.remove(list)
            print("Başarıyla kaldırıldı")
            save(item)
            return
    print("Ürün bulunamadı.")

def criticalStockReport(item):
    report_list = []
    for list in item:
        if list["stok"] < 5:
            report_list.append(list)

    return report_list

def totalItemValue(Item):
    totalvalue = 0
    for list in Item:
        totalvalue += list["fiyat"]*list["stok"]

    return totalvalue

def save(items):
    with open("envanter.json", "w",encoding="utf-8") as file:
        json.dump(items, file,ensure_ascii=False, indent=2)

def main():
    item = load()
    while True:
            printMenu()
            try:
                secim = int(input("Seçiminiz: "))
            except ValueError:
                print("Lütfen bir sayı girin.")
                continue
            match secim:
                case 0:
                    save(item)
                    break
                case 1:
                    printItems(item)
                case 2:
                    addItem(item)
                case 3:
                    searchItem(item)
                case 4:
                    updateStockAndPrice(item)
                case 5:
                     deleteItem(item)
                case 6:
                    kritik = criticalStockReport(item)
                    if kritik:
                        printItems(kritik)
                    else:
                        print("Kritik stokta ürün yok.")
                case 7:
                    print(f"Ürünlerin toplam değeri: {totalItemValue(item):.2f}")
                case _:
                    print("Geçersiz seçim. Lütfen 0-7 arası bir sayı seçin.")

if __name__ == "__main__":
    main()
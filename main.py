import json
from enum import Flag
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

def yeniID(items):
    if not items:
        return 1

    return max(urun["id"] for urun in items) + 1

def printItems():

    try:
        file = open("envanter.json")
        items = json.load(file)
    except FileNotFoundError:
        print("Kayıtlı dosya bulunamadı")

    for item in items:
        print(item)

def addItem(items):
    while True:
        try:
            ad = str(input("Ürün adı giriniz: ")).strip().capitalize()
            if ad == "":
                print("Lütfen ad giriniz.")
                continue
            kategori = str(input("Kategori giriniz: "))
            stok = int(input("Stok giriniz: "))
            fiyat = float(input("Fiyat giriniz: "))

            if stok < 0:
                print("Lütfen sıfır veya sıfırdan büyük bir değer giriniz.")
                continue
            if fiyat<=0:
                print("Lütfen sıfırdan büyük bir değer giriniz.")
                continue

        except ValueError:
            print("İşlemde hata meydana geldi.Lütfen geçerli değerler giriniz.")
            continue

        list = {
                "id": yeniID(items),
                "ad": ad,
                "kategori": kategori,
                "stok": stok,
                "fiyat": fiyat
            }
        items.append(list)
        print("Başarıyla Eklendi.")
        break
        #print(yeniID(items)+" id numaralı ürün başarıyla eklendi.")


def searchItem(items):

        ad = str(input("Lütfen aradığınız ürünün adını yazınız: ")).strip().lower()
        if ad == "":
            return
        bul = False
        for list in items:
            if ad in list["ad"].lower():
                bul = True
                print(list)
                print("Ürün bulundu.")

        if not bul:
            print("Ürün bulunamadı.")

def updateStockAndPrice(items):
    tempList = None
    while True:
        try:
            id = int(input("Lütfen değiştirmek istediğiniz ürünün id numarasını giriniz: "))
            for list in items:
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
            yeniFiyat = float(input("Lütfen yeni fiyat giriniz: "))

            if  yeniStok >= 0 and yeniFiyat > 0:
                break
            else:
                print("Stok sıfır veya sıfırdan büyüki fiyat sıfırdan büyük olmak zorunda.")
        except ValueError:
            print("Lütfen değer giriniz.")
            continue

    tempList["stok"] = yeniStok
    tempList["fiyat"] = yeniFiyat
    print("Başarıyla güncellendi.")


def deleteItem():
    pass

def criticalStockReport():
    pass

def totalItemValue():
    pass

def save(items):
    file = open("envanter.json", "w",encoding="utf-8")
    json.dump(items, file,ensure_ascii=False, indent=2)

def main():
    try:
        file = open("envanter.json")
        item = json.load(file)
        while True:
            printMenu()
            try:
                secim = int(input("Seçiminiz: "))
            except ValueError:
                print("Lütfen bir sayı girin.")
                continue
            except:
                print("Hata!")
            match secim:
                case 0:
                    save(item)
                    break
                case 1:
                    printItems()
                case 2:
                    addItem(item)
                    save(item)
                case 3:
                    searchItem(item)
                case 4:
                    updateStockAndPrice(item)
                    save(item)
                case 5:
                     deleteItem()
                case 6:
                    criticalStockReport()
                case 7:
                    totalItemValue()
                case _:
                    print("Geçersiz seçim. Lütfen 0-7 arası bir sayı seçin.")

    except FileNotFoundError:
        print("Error.")

    except JSONDecodeError:
        print("Error.")

if __name__ == "__main__":
    main()
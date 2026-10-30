import json
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

    global items
    try:
        file = open("envanter.json")
        items = json.load(file)
    except FileNotFoundError:
        print("Kayıtlı dosya bulunamadı")

    print(items)

def addItem(items):
        try:
            ad = str(input("Kullanıcı adı giriniz: "))
        except ValueError:

            kategori = str(input("Kategori giriniz: "))
        while True:
            try:
                stok = int(input("Stok giriniz: "))
                if stok<0:
                    print("Lütfen sıfır veya sıfırdan büyük bir değer giriniz.")
                else:
                    break
            except ValueError:
                print("Lütfen bir değer giriniz.")
        while True:
            try:
                fiyat = float(input("Fiyat giriniz: "))
                if fiyat<=0:
                    print("Lütfen sıfırdan büyük bir değer giriniz.")
                else:
                    break
            except ValueError:
                print("Lütfen bir değer giriniz.")

        list = {
            "id": yeniID(items),
            "ad": ad,
            "kategori": kategori,
            "stok": stok,
            "fiyat": fiyat
        }
        items.append(list)
        #print(yeniID(items)+" id numaralı ürün başarıyla eklendi.")


def searchItem():
    pass

def updateStockAndPrice():
    pass

def deleteItem():
    pass

def criticalStockReport():
    pass

def totalItemValue():
    pass

def saveAndExit():
    pass


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
                    saveAndExit()
                    break
                case 1:
                    printItems()
                case 2:
                    addItem(item)
                case 3:
                    searchItem()
                case 4:
                    updateStockAndPrice()
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
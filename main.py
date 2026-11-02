import json
import math
import os
from json import JSONDecodeError


def print_menu():
    cizgi = "=" * 40
    print(f"""{cizgi}
     DEPO VE STOK YÖNETİM SİSTEMİ
{cizgi}
1. Tüm Ürünleri Listele
2. Yeni Ürün Ekle
3. Ürün Ara (İsme Göre)
4. Stok ve Fiyat Güncelle
5. Ürün Sil
6. Kritik Stok Raporu (< 5)
7. Toplam Envanter Değeri
0. Kaydet ve Çıkış
{cizgi}""")


def load():
    try:
        with open("envanter.json", encoding="utf_8") as file:
            items = json.load(file)
            return items
    except FileNotFoundError:
        with open("envanter.json", "w", encoding="utf_8") as file:
            file.write("[]")
            return []
    except JSONDecodeError:
        os.replace("envanter.json", "envanter_bozuk.json")
        print("UYARI: envanter.json bozuktu, "
              "envanter_bozuk.json olarak yedeklendi.")
        with open("envanter.json", "w", encoding="utf_8") as file:
            file.write("[]")
        return []


def yeni_id(item):
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


def print_items(item):
    if not item:
        print("Kayıtlı ürün bulunamadı")
        return

    print(f"{'ID':<4} {'Ad':<20} "
          f"{'Kategori':<15} {'Stok':>6} "
          f"{'Fiyat':>10} {'Satır Değeri':>14}")
    print("-" * 74)
    for urun in item:
        satir_degeri = urun["stok"] * urun["fiyat"]
        print(f"{urun['id']:<4} {urun['ad']:<20} "
              f"{urun['kategori']:<15} "
              f"{urun['stok']:>6} {urun['fiyat']:>10.2f} "
              f"{satir_degeri:>14.2f}")

    print("\n")


def add_item(item):
    while True:
        try:
            ad = tr_capitalize(input("Ürün adı giriniz: ").strip())
            if ad == "":
                print("Lütfen ad giriniz.")
                continue
            kategori = input("Kategori giriniz: ").strip()
            stok = int(input("Stok giriniz: "))
            fiyat = float(input("Fiyat giriniz: ").replace(",", "."))

            if stok < 0:
                print("Lütfen sıfır veya sıfırdan büyük bir değer giriniz.")
                continue
            if not math.isfinite(fiyat) or fiyat <= 0:
                print("Lütfen sıfırdan "
                      "büyük bir değer giriniz.")
                continue

        except ValueError:
            print("İşlemde hata meydana geldi."
                  " Lütfen geçerli değerler giriniz.")
            continue

        yeni_urun = {
                "id": yeni_id(item),
                "ad": ad,
                "kategori": kategori,
                "stok": stok,
                "fiyat": fiyat
            }
        item.append(yeni_urun)
        print("Başarıyla Eklendi.")
        save(item)
        break


def search_item(item):
    ad = tr_lower(input("Lütfen aradığınız ürünün adını yazınız: ").strip())
    if ad == "":
        return
    bulunanlar = [urun for urun in item if ad in tr_lower(urun["ad"])]
    if bulunanlar:
        print_items(bulunanlar)
    else:
        print("Ürün bulunamadı.")


def update_stock_and_price(item):
    secilen_urun = None
    while True:
        try:
            urun_id = int(input("Lütfen değiştirmek istediğiniz "
                                "ürünün id numarasını giriniz: "))
            for urun in item:
                if urun["id"] == urun_id:
                    secilen_urun = urun
                    print("Bulundu")
                    break

        except ValueError:
            print("Lütfen bir sayı giriniz.")
            continue

        if secilen_urun is None:
            print("Bulunamadı.")
            return

        break

    print_items([secilen_urun])
    while True:
        try:
            yeni_stok = int(input("Lütfen yeni stoku giriniz: "))
            yeni_fiyat = float(input("Lütfen yeni "
                                     "fiyat giriniz: ").replace(",", "."))

            if (yeni_stok >= 0 and math.isfinite(yeni_fiyat)
                    and yeni_fiyat > 0):
                break
            else:
                print("Stok sıfır veya sıfırdan büyük, "
                      "fiyat sıfırdan büyük olmak zorunda.")
        except ValueError:
            print("Lütfen değer giriniz.")
            continue

    secilen_urun["stok"] = yeni_stok
    secilen_urun["fiyat"] = yeni_fiyat
    print("Başarıyla güncellendi.")

    save(item)


def delete_item(item):
    if not item:
        print("Listede herhangi "
              "bir ürün yok.")
        return
    try:
        urun_id = int(input("Lütfen kaldırmak istediğiniz ürünün "
                            "id numarasını giriniz: "))
    except ValueError:
        print("Lütfen numara değeri giriniz.")
        return
    for urun in item:
        if urun["id"] == urun_id:
            item.remove(urun)
            print("Başarıyla kaldırıldı")
            save(item)
            return
    print("Ürün bulunamadı.")


def critical_stock_report(item):
    return [urun for urun in item if urun["stok"] < 5]


def total_item_value(items):
    total_value = 0
    for urun in items:
        total_value += urun["fiyat"]*urun["stok"]

    return total_value


def save(items):
    with open("envanter.json", "w", encoding="utf-8") as file:
        json.dump(items, file, ensure_ascii=False, indent=2)


def main():
    item = load()
    while True:
        print_menu()
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
                print_items(item)
            case 2:
                add_item(item)
            case 3:
                search_item(item)
            case 4:
                update_stock_and_price(item)
            case 5:
                delete_item(item)
            case 6:
                kritik = (
                    critical_stock_report(item))
                if kritik:
                    print_items(kritik)
                else:
                    print("Kritik stokta ürün yok.")
            case 7:
                print(f"Ürünlerin toplam değeri: {total_item_value(item):.2f}")
            case _:
                print("Geçersiz seçim. Lütfen 0-7 arası bir sayı seçin.")


if __name__ == "__main__":
    main()

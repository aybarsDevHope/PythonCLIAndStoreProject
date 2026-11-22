import math, logging


from flask import Flask, jsonify, request
from main import load, yeni_id, save, critical_stock_report, total_item_value, tr_lower
from models import tablolari_olustur

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log", encoding="utf-8")],
)

app = Flask(__name__)
app.json.ensure_ascii = False


def urun_bul(items, urun_id):
    return next((urun for urun in items if urun["id"] == urun_id), None)


def dogrula(data, alanlar):
    """Hata varsa mesajını, yoksa None döndürüyor"""
    if not isinstance(data, dict):
        return "Geçerli bir JSON gönderilmedi"

    eksik = [alan for alan in alanlar if alan not in data]
    if eksik:
        return f"Eksik alan(lar): {', '.join(eksik)}"

    if "ad" in alanlar:
        if not isinstance(data["ad"], str) or not data["ad"].strip():
            return "ad boş olmayan bir metin olmalı"

    if "kategori" in alanlar:
        if not isinstance(data["kategori"], str) or not data["kategori"].strip():
            return "kategori boş olmayan bir metin olmalı"

    if "stok" in alanlar:
        if not isinstance(data["stok"], int) or isinstance(data["stok"], bool) or data["stok"] < 0:
            return "stok 0 veya daha büyük bir tam sayı olmalı"

    if "fiyat" in alanlar:
        if not isinstance(data["fiyat"], (int, float)) or isinstance(data["fiyat"], bool) or data[
            "fiyat"] <= 0 or not math.isfinite(data["fiyat"]):
            return "fiyat 0'dan büyük bir sayı olmalı"

    return None

@app.route("/urunler", methods=["GET"])
def listele():
    liste = load()
    aranan = request.args.get("q")

    if aranan is None:
        return jsonify(liste)
    aranan = tr_lower(aranan)
    bulunanlar = [urun for urun in liste if aranan in tr_lower(urun["ad"])]

    return jsonify(bulunanlar)


@app.route("/urunler/<int:urun_id>", methods=["GET"])
def belirli_urun_getir(urun_id):
    liste = load()
    temp = urun_bul(liste, urun_id)
    if temp is not None:
        return jsonify(temp)
    else:
        return jsonify(hata="ürün bulunamadı"), 404


@app.route("/urunler", methods=["POST"])
def urun_ekle():
    data = request.get_json(silent=True)
    hata = dogrula(data, ["ad", "kategori", "stok", "fiyat"])
    if hata:
        return jsonify(hata=hata), 400
    items = load()
    yeni_urun = {
        "id": yeni_id(items),
        "ad": data["ad"],
        "kategori": data["kategori"],
        "stok": data["stok"],
        "fiyat": data["fiyat"]
    }
    items.append(yeni_urun)
    save(items)
    return jsonify(yeni_urun), 201


@app.route("/urunler/<int:urun_id>", methods=["PUT"])
def urun_guncelle(urun_id):
    data = request.get_json(silent=True)
    hata = dogrula(data, ["stok", "fiyat"])
    if hata:
        return jsonify(hata=hata), 400
    items = load()
    temp = urun_bul(items, urun_id)
    if temp is None:
        return jsonify(hata=f"{urun_id} numaralı ürün bulunamadı"), 404
    temp["stok"] = data["stok"]
    temp["fiyat"] = data["fiyat"]
    save(items)
    return jsonify(temp)


@app.route("/urunler/<int:urun_id>", methods=["DELETE"])
def urun_sil(urun_id):
    liste = load()
    urun = urun_bul(liste, urun_id)
    if urun is None:
        return jsonify(hata=f"{urun_id} numaralı ürün bulunamadı"), 404
    liste.remove(urun)
    save(liste)
    return jsonify(mesaj=f"{urun_id} numaralı ürün silindi")


@app.route("/rapor/kritik", methods=["GET"])
def kritik_rapor():
    liste = load()
    return jsonify(critical_stock_report(liste))


@app.route("/rapor/toplam", methods=["GET"])
def total_rapor():
    liste = load()
    toplam = total_item_value(liste)
    return jsonify(toplam=toplam, mesaj=f"Toplam envanter değeri: {toplam:.2f} TL")


if __name__ == "__main__":
    tablolari_olustur()
    app.run(debug=True)

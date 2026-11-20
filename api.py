
from flask import Flask, jsonify, request
from main import load, yeni_id, save, critical_stock_report, total_item_value

app = Flask(__name__)
app.json.ensure_ascii = False

def urun_bul(items,urun_id):
    for temp in items:
        if temp["id"] == urun_id:
            return temp
    return None


@app.route("/urunler", methods=["GET"])
def listele():
    return jsonify(load())


@app.route("/urunler/<int:urun_id>", methods=["GET"])
def urun_getir(urun_id):
    liste = load()
    temp = urun_bul(liste,urun_id)
    if temp is not None:
        return jsonify(temp)
    else:
        return jsonify(hata = "ürün bulunamadı"), 404


@app.route("/urunler", methods=["POST"])
def urun_ekle():
    data = request.json
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
    data = request.json
    items = load()
    temp = urun_bul(items,urun_id)
    if temp is None:
        return temp
    temp["stok"] = data["stok"]
    temp["fiyat"] = data["fiyat"]
    save(items)
    return jsonify(temp)


@app.route("/urunler/<int:urun_id>", methods=["DELETE"])
def urun_sil(urun_id):
    liste = load()
    urun = urun_bul(liste,urun_id)
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
    app.run(debug=True)





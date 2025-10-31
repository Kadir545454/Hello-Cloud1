from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app) # CORS ayarı doğru

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://kadir:yWNXnRVYLNuQfsgYhyfeIboWDFXPMhiY@dpg-d3tjgf9r0fns73ahsth0-a.oregon-postgres.render.com/hello_cloud2_db_ryty"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# --- Ziyaretçiler (İsimler) Rotası ---
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    
    # 1. Tablonun var olup olmadığını kontrol et VE HEMEN KAYDET
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")
    conn.commit() # DİKKAT: Tablo oluşturma işlemini kaydetmek için eklendi.
    
    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit() # Sadece ekleme işlemini kaydet

    # Her iki istek türünde de (GET veya POST) son 10 ismi döndür
    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return jsonify(isimler)

# --- YENİ EKLENEN: Şehirler Rotası ---
@app.route("/sehirler", methods=["GET", "POST"])
def sehirler():
    conn = connect_db()
    cur = conn.cursor()
    
    # 1. 'sehirler' tablosunu oluştur VE HEMEN KAYDET
    cur.execute("CREATE TABLE IF NOT EXISTS sehirler (id SERIAL PRIMARY KEY, sehir TEXT)")
    conn.commit() # DİKKAT: Tablo oluşturma işlemini kaydetmek için eklendi.
    
    if request.method == "POST":
        sehir = request.json.get("sehir") # Gelen JSON'da 'sehir' anahtarını ara
        if sehir:
            # 'sehirler' tablosuna ekle
            cur.execute("INSERT INTO sehirler (sehir) VALUES (%s)", (sehir,))
            conn.commit() # Sadece ekleme işlemini kaydet

    # Son 10 şehri getir
    cur.execute("SELECT sehir FROM sehirler ORDER BY id DESC LIMIT 10")
    sehirler_listesi = [row[0] for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    # Şehir listesini JSON olarak döndür
    return jsonify(sehirler_listesi)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

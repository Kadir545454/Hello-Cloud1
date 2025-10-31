from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Bu, app.py dosyanızın çalıştığı adres (Render.com)
API_URL = "https://hello-cloud1-eksl.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam! (Tek Panel)</title>
<style>
    body { 
        font-family: Arial, sans-serif; 
        padding: 40px; 
        background: #eef2f3; 
        color: #333;
    }
    h1 {
        text-align: center;
        color: #2c3e50;
    }
    
    /* TEK ANA PANELİN STİLİ */
    .main-panel {
        max-width: 600px; /* Panelin maksimum genişliği */
        margin: 20px auto; /* Paneli yatayda ortalar */
        background: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    input[type="text"] { 
        width: 90%; /* Panelin içine sığsın */
        padding: 12px; 
        font-size: 16px; 
        margin-bottom: 20px; /* Girişler arası boşluk */
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    
    /* Ana Gönder Butonu Stili */
    .submit-button-container {
        text-align: center;
        margin-top: 15px;
        margin-bottom: 30px; /* Buton ile listeler arası boşluk */
    }
    .submit-button-container button { 
        padding: 12px 30px; 
        background: #007BFF; 
        color: white; 
        border: none; 
        border-radius: 8px; 
        cursor: pointer; 
        font-size: 18px;
        font-weight: bold;
    }
    .submit-button-container button:hover {
        background: #0056b3;
    }
    
    ul {
        list-style-type: none;
        padding: 0;
    }
    li { 
        background: #f9f9f9; 
        margin: 5px 0; 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px solid #eee;
    }
    
    /* Listeler arasına ayırıcı çizgi ekle */
    .list-divider {
        border-top: 1px solid #eee;
        margin: 30px 0;
    }

</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>

<div class="main-panel">
    <form method="POST">
        
        <h2>İsim Ekle</h2>
        <p>Adını yaz</p>
        <input type="text" name="isim" placeholder="Adını yaz">
        
        <h2>Şehir Ekle</h2>
        <p>Şehrini yaz</p>
        <input type="text" name="sehir" placeholder="Şehrini yaz">
        
        <div class="submit-button-container">
            <button type="submit">Gönder</button>
        </div>

        <div class="list-divider"></div>

        <h3>Ziyaretçiler:</h3>
        <ul>
            {% for ad in isimler %}
                <li>{{ ad }}</li>
            {% endfor %}
        </ul>
        
        <h3>Eklenen Şehirler:</h3>
        <ul>
            {% for sehir in sehirler %}
                <li>{{ sehir }}</li>
            {% endfor %}
        </ul>
        
    </form>
</div>

</body>
</html>
"""

# --- PYTHON (FLASK) KODU ---
# Bu kısımda hiçbir değişiklik yapmaya gerek yok,
# bir önceki "tek gönder tuşu" ile aynı mantıkta çalışıyor.

@app.route("/", methods=["GET", "POST"])
def index():
    # --- POST Metodu: Tek form gönderildiğinde ---
    if request.method == "POST":
        
        # 1. İsim alanını kontrol et
        isim = request.form.get("isim")
        if isim: 
            try:
                requests.post(API_URL + "/ziyaretçiler", json={"isim": isim})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /ziyaretciler): {e}")
                
        # 2. Şehir alanını kontrol et
        sehir = request.form.get("sehir")
        if sehir: 
            try:
                requests.post(API_URL + "/sehirler", json={"sehir": sehir})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /sehirler): {e}")
        
        return redirect("/")

    # --- GET Metodu: Sayfa Yüklendiğinde ---
    
    # 1. İsim listesini al
    isimler = []
    try:
        resp_isimler = requests.get(API_URL + "/ziyaretciler")
        if resp_isimler.status_code == 200:
            isimler = resp_isimler.json()
    except requests.exceptions.RequestException as e:
        print(f"Hata (GET /ziyaretciler): {e}")

    # 2. Şehir listesini al
    sehirler = []
    try:
        resp_sehirler = requests.get(API_URL + "/sehirler")
        if resp_sehirler.status_code == 200:
            sehirler = resp_sehirler.json()
    except requests.exceptions.RequestException as e:
        print(f"Hata (GET /sehirler): {e}")
    
    # 3. HTML'i ve her iki listeyi render et
    return render_template_string(HTML, isimler=isimler, sehirler=sehirler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

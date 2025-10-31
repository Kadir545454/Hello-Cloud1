from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Bu, app.py dosyanızın çalıştığı adres (Render.com)
API_URL = "https://hello-cloud1-eksl.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam! (İsim & Şehir)</title>
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
    /* Ana Taşıyıcı: Kutuları yan yana dizer */
    .container {
        display: flex;
        justify-content: space-around; /* Kutular arasına eşit boşluk bırakır */
        flex-wrap: wrap; /* Küçük ekranlarda alt alta inmeyi sağlar */
        gap: 20px; /* Kutular arasında boşluk bırakır */
    }
    
    /* Her bir kutunun stili */
    .box {
        flex: 1; /* Her kutu eşit yer kaplar */
        min-width: 300px; /* Minimum genişlik */
        background: #ffffff;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    input[type="text"] { 
        width: 80%;
        padding: 10px; 
        font-size: 16px; 
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    button { 
        padding: 10px 18px; 
        background: #4CAF50; 
        color: white; 
        border: none; 
        border-radius: 6px; 
        cursor: pointer; 
        font-size: 16px;
    }
    button:hover {
        background: #45a049;
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
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>
<div class="container">
    
    <div class="box">
        <h2>İsim Ekle</h2>
        <p>Adını yaz</p>
        <form method="POST">
            <input type="text" name="isim" placeholder="Adını yaz" required>
            <button type="submit">Gönder</button>
        </form>
        <h3>Ziyaretçiler:</h3>
        <ul>
            {% for ad in isimler %}
                <li>{{ ad }}</li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="box">
        <h2>Şehir Ekle</h2>
        <p>Şehrini yaz</p>
        <form method="POST">
            <input type="text" name="sehir" placeholder="Şehrini yaz" required>
            <button type="submit">Gönder</button>
        </form>
        <h3>Eklenen Şehirler:</h3>
        <ul>
            {% for sehir in sehirler %}
                <li>{{ sehir }}</li>
            {% endfor %}
        </ul>
    </div>
    
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # --- POST Metodu: Formlardan Biri Gönderildiğinde ---
    if request.method == "POST":
        # Hangi formun gönderildiğini kontrol et
        if "isim" in request.form:
            isim = request.form.get("isim")
            try:
                requests.post(API_URL + "/ziyaretciler", json={"isim": isim})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /ziyaretciler): {e}")
                
        elif "sehir" in request.form:
            sehir = request.form.get("sehir")
            try:
                requests.post(API_URL + "/sehirler", json={"sehir": sehir})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /sehirler): {e}")
        
        # Her iki durumda da işlem sonrası ana sayfaya yönlendir
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

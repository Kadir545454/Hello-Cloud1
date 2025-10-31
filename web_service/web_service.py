from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Bu, app.py dosyanızın çalıştığı adres (Render.com)
API_URL = "https://hello-cloud1-eksl.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam! (Tek Buton)</title>
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
    .container {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 20px;
    }
    .box {
        flex: 1;
        min-width: 300px;
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
    
    /* Ana Gönder Butonu Stili */
    .submit-button-container {
        text-align: center;
        margin-top: 25px;
    }
    .submit-button-container button { 
        padding: 12px 30px; /* Daha büyük buton */
        background: #007BFF; /* Farklı bir renk */
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
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>

<form method="POST">
    <div class="container">
        
        <div class="box">
            <h2>İsim Ekle</h2>
            <p>Adını yaz</p>
            <input type="text" name="isim" placeholder="Adını yaz">
            
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
            <input type="text" name="sehir" placeholder="Şehrini yaz">
            
            <h3>Eklenen Şehirler:</h3>
            <ul>
                {% for sehir in sehirler %}
                    <li>{{ sehir }}</li>
                {% endfor %}
            </ul>
        </div>
        
    </div>
    
    <div class="submit-button-container">
        <button type="submit">Gönder</button>
    </div>

</form> </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    # --- POST Metodu: Tek form gönderildiğinde ---
    if request.method == "POST":
        
        # 1. İsim alanını kontrol et
        isim = request.form.get("isim")
        # Eğer 'isim' alanı boş değilse API'ye gönder
        if isim: 
            try:
                requests.post(API_URL + "/ziyaretciler", json={"isim": isim})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /ziyaretciler): {e}")
                
        # 2. Şehir alanını kontrol et (Burada 'elif' KULLANILMAMALI)
        sehir = request.form.get("sehir")
        # Eğer 'sehir' alanı boş değilse API'ye gönder
        if sehir: 
            try:
                requests.post(API_URL + "/sehirler", json={"sehir": sehir})
            except requests.exceptions.RequestException as e:
                print(f"Hata (POST /sehirler): {e}")
        
        # Her iki kontrol bittikten sonra sayfayı yenile
        return redirect("/")

    # --- GET Metodu: Sayfa Yüklendiğinde (Bu kısım aynı kaldı) ---
    
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

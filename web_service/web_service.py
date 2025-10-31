from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Bu, app.py dosyanızın çalıştığı adres (Render.com)
API_URL = "https://hello-cloud1-eksl.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam!</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
input { padding: 10px; font-size: 16px; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>
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
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        isim = request.form.get("isim")
        # Arka plan API'sine (app.py) veriyi gönder
        requests.post(API_URL + "/ziyaretciler", json={"isim": isim})
        return redirect("/")

    # Sayfa yüklendiğinde (GET) veya isim eklendikten sonra (redirect)
    # Arka plan API'sinden (app.py) isim listesini al
    resp = requests.get(API_URL + "/ziyaretciler")
    isimler = resp.json() if resp.status_code == 200 else []
    
    # HTML'i ve isim listesini render et
    return render_template_string(HTML, isimler=isimler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template_string, request, redirect
import requests

app = Flask(__name__)

# Bu, app.py dosyanızın çalıştığı adres (Render.com)
API_URL = "https://hello-cloud1-eksl.onrender.com"

HTML = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam! (Şehir Versiyonu)</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
input { padding: 10px; font-size: 16px; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; }
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>
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
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sehir = request.form.get("sehir")
        # Arka plan API'sine (app.py) şehir verisini gönder
        # API'nizin /sehirler endpoint'ine sahip olduğunu varsayıyoruz
        try:
            requests.post(API_URL + "/sehirler", json={"sehir": sehir})
        except requests.exceptions.RequestException as e:
            print(f"Hata (POST): {e}") # Sunucuya bağlanamazsa logla
        return redirect("/")

    # Sayfa yüklendiğinde (GET) veya şehir eklendikten sonra (redirect)
    # Arka plan API'sinden (app.py) şehir listesini al
    # API'nizin /sehirler endpoint'ine sahip olduğunu varsayıyoruz
    sehirler = []
    try:
        resp = requests.get(API_URL + "/sehirler")
        if resp.status_code == 200:
            sehirler = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Hata (GET): {e}") # Sunucuya bağlanamazsa logla
    
    # HTML'i ve şehir listesini render et
    return render_template_string(HTML, sehirler=sehirler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

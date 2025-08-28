# Flask API CSRF Token ile cURL Komutları

## CSRF Token Alma ve Login

### 1. CSRF token'i al (Login sayfasını GET ile çek)
HTML içinde csrf_token input'u bulunur:

```bash
curl -c cookies.txt http://127.0.0.1:5000/login
```

### 2. Login POST isteğini CSRF ile gönder
Hem cookie dosyasını (-b cookies.txt) gönder hem de csrf token parametresini login formuna ekle:

```bash
curl -c cookies.txt -b cookies.txt -X POST http://127.0.0.1:5000/login \
-d "username=gokhan&password=1234&csrf_token=<buraya_csrf_token>"
```

## API İşlemleri

### 1️⃣ Notları listeleme (GET)

```bash
curl -b cookies.txt http://127.0.0.1:5000/api/notes
```

### 2️⃣ Not ekleme (POST)

```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/notes \
-H "Content-Type: application/json" \
-H "X-CSRFToken: <buraya_csrf_token>" \
-d '{"note": "Curl test"}'
```

### 3️⃣ Not güncelleme (PUT veya PATCH)

```bash
curl -b cookies.txt -X PUT http://127.0.0.1:5000/api/notes/<buraya_id> \
-H "Content-Type: application/json" \
-H "X-CSRFToken: <buraya_csrf_token>" \
-d '{"note": "Updated via curl"}'
```

### 4️⃣ Not silme (DELETE)

```bash
curl -b cookies.txt -X DELETE http://127.0.0.1:5000/api/notes/<buraya_id> \
-H "X-CSRFToken: <buraya_csrf_token>"
```

## Notlar

- `cookies.txt` dosyası session bilgilerini saklar
- CSRF token her form gönderiminde gereklidir
- API isteklerinde `X-CSRFToken` header'ı kullanılır
- Login formunda `csrf_token` field'ı kullanılır
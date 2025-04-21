# Customer Review Scraper

Bu uygulama, HTML dosyalarından veya URL'lerden müşteri yorumlarını çeker.

## Kullanım

### Temel Kullanım

```
python main.py
```
Bu komut varsayılan olarak `feedback.html` dosyasını okur ve sonuçları `reviews.json` dosyasına kaydeder.

### URL'den Yorum Çekme

```
python main.py --url "https://www.trendyol.com/teenage-millionaire/kadin-lacivert-bisiklet-yaka-likrali-kisa-kol-body-crop-bluz-p-807250024"
```

### Farklı Çıktı Formatları

```
python main.py --format csv
python main.py --format excel
python main.py --format all
```

### Tüm Parametreler

- `--input`, `-i`: Yorumları içeren HTML dosyası (varsayılan: feedback.html)
- `--url`, `-u`: Yorumları çekmek için URL
- `--output`, `-o`: Çıktı dosyası adı, uzantısız (varsayılan: reviews)
- `--format`, `-f`: Çıktı formatı (json, csv, excel, all) (varsayılan: json)

### Örnekler

URL'den çekip Excel formatında kaydetme:
```
python main.py --url "https://www.trendyol.com/teenage-millionaire/kadin-lacivert-bisiklet-yaka-likrali-kisa-kol-body-crop-bluz-p-807250024" --format excel
```

Yerel dosyadan okuyup tüm formatlarda kaydetme:
```
python main.py --input "my_reviews.html" --output "product_reviews" --format all
```

# Görev Hatırlatıcı

Python ödevi için yaptığım planlama ve hatırlatıcı bot.

Terminal üzerinden çalışan, Python ile yazılmış basit bir görev hatırlatıcı uygulaması. Görevlerini gün ve saat belirterek kaydedersin, saati geldiğinde ekranda bildirim penceresi çıkar.

## Özellikler

- Gün/dönem, saat ve açıklama ile görev ekleme
- Görevler `gorev_listesi.json` dosyasına kaydedilir, program kapanınca kaybolmaz
- Kayıtlı tüm görevleri listeleme
- Hatırlatıcı arka planda çalışır, açıkken menüyü kullanmaya ve yeni görev eklemeye devam edebilirsin
- Gün adı yazılan görevler sadece o gün çalar (örn. `Pazartesi`, `Pazartesi, Çarşamba`)
- Aynı görev aynı gün içinde tekrar bildirilmez
- Saat girerken `21.45` yazarsan otomatik olarak `21:45` olarak kaydedilir

## Gereksinimler

- Python 3.8 veya üzeri
- `tkinter`

Ek bir kütüphane kurulumu gerekmez, sadece Python'un kendi modülleri kullanılıyor.

## Kurulum ve Çalıştırma

```bash
git clone https://github.com/Mcataseven/Odev_Pyhton.git
cd Odev_Pyhton
python gorev_hatirlatici.py
```

## Kullanım

Program açılınca şu menü gelir:

```
1- Görev Ekle
2- Tüm Görevleri Göster
3- Hatırlatıcıyı Başlat
4- Çıkış
```

1. **Görev Ekle:** Gün (veya dönem), saat ve görev açıklamasını gir.
2. **Tüm Görevleri Göster:** Kayıtlı görevleri numaralı liste olarak gösterir.
3. **Hatırlatıcıyı Başlat:** Hatırlatıcıyı arka planda başlatır. Her 5 saniyede bir saati kontrol eder, görevin saati gelince bildirim penceresi açar.
4. **Çıkış:** Programı kapatır. Hatırlatıcı da program ile birlikte durur.

### Örnek

```
Gün veya dönem (Örn: Pazartesi, Aylık): Pazartesi
Saat (Örn: 21:45): 21.45
Görev açıklaması: Haftalık raporu hazırla
Görev kaydedildi.
```

## Görev Formatı

Görevler `gorev_listesi.json` dosyasında şu şekilde tutulur:

```json
[
    {
        "gun": "Pazartesi",
        "saat": "21:45",
        "aciklama": "Haftalık raporu hazırla"
    }
]
```

## Gün Alanı Nasıl Çalışır?

- Gün adı yazarsan (`Pazartesi`, `Salı`, `Çarşamba`, `Perşembe`, `Cuma`, `Cumartesi`, `Pazar`) görev sadece o gün çalar. Birden fazla gün de yazabilirsin: `Pazartesi, Cuma`.
- Gün adı içermeyen bir şey yazarsan (`Aylık`, `Her gün` gibi) görev her gün o saatte çalar.

## Bilinen Sınırlamalar

- Hatırlatıcı sadece program açıkken çalışır. Program kapalıyken bildirim gelmez.
- Ayın belirli bir günü için (örn. "her ayın 15'i") özel bir kontrol yok.
- Görev silme veya düzenleme özelliği henüz yok, şimdilik `gorev_listesi.json` dosyasını elle düzenleyebilirsin.

## Yapılabilecek Geliştirmeler

- [ ] Görev silme ve düzenleme
- [ ] Ayın belirli günü için tekrar desteği
- [ ] Hatırlatıcıyı durdurma seçeneği
- [ ] Bilgisayar açılışında otomatik başlatma

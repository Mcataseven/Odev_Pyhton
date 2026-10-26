import json
import os
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

dosya_adi = "gorev_listesi.json"

# Gün adlarını hafta günü numarasına çeviriyorum (Pazartesi = 0, Pazar = 6)
gun_numaralari = {
    "pazartesi": 0,
    "salı": 1, "sali": 1,
    "çarşamba": 2, "carsamba": 2,
    "perşembe": 3, "persembe": 3,
    "cuma": 4,
    "cumartesi": 5,
    "pazar": 6
}

hatirlatici_thread = None  # Hatırlatıcı arka planda çalıştığından threadi burada tutuyorum

# Kayıtlı görevleri dosyadan okuma fonksiyonu
def gorevleri_getir():
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as f:
            return json.load(f)
    return []  # Dosya yoksa boş liste döndürecek

# Görevleri json dosyasına kaydetme fonksiyonu
def gorevleri_kaydet(liste):
    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=4)

# Havuza yeni görev ekleme kısmı
def gorev_ekle(liste):
    gun = input("Gün veya dönem (Örn: Pazartesi, Aylık): ")
    saat = input("Saat (Örn: 21:45): ").replace(".", ":")  # Nokta girilirse iki noktaya çevirir
    aciklama = input("Görev açıklaması: ")

    yeni_gorev = {
        "gun": gun,
        "saat": saat,
        "aciklama": aciklama
    }
    liste.append(yeni_gorev)
    gorevleri_kaydet(liste)
    print("Görev kaydedildi.")

# Bütün görevleri tek seferde ekrana yazdırmamı sağlayor
def gorevleri_listele(liste):
    print("\n--- Kayıtlı Görevler ---")
    if len(liste) == 0:
        print("Henüz eklenmiş bir görev yok.")
    else:
        for i in range(len(liste)):
            g = liste[i]
            print(f"{i+1}) {g['gun']} - Saat {g['saat']} : {g['aciklama']}")

# Görevin bugün çalışıp çalışmayacağını kontrol eder
# Gün adı yazılmışsa (Pazartesi, Cuma gibi) sadece o gün çalar, başka bir şey yazılmışsa (Aylık, Her gün) her gün çalar
def gorev_bugun_mu(gun_yazisi, bugun_no):
    kelimeler = gun_yazisi.lower().replace(",", " ").split()
    secilen_gunler = [gun_numaralari[k] for k in kelimeler if k in gun_numaralari]
    if len(secilen_gunler) == 0:
        return True
    return bugun_no in secilen_gunler

# Görevin saati gelince bildirim atan döngü, arka planda ayrı thread olarak çalışıyor
def hatirlatici_dongusu(liste):
    # tkinterı sadece bu thread içinde kullanıyorum, boş pencere çıkmasın diye gizliyorum
    root = tk.Tk()
    root.withdraw()

    bildirilenler = set()  # (açıklama, saat, tarih) tutuyor, aynı görev aynı gün tekrar bildirilmesin diye

    while True:
        simdi = datetime.now()
        su_an = simdi.strftime("%H:%M")
        bugun = simdi.strftime("%Y-%m-%d")

        for g in list(liste):
            gorev_saati = g["saat"].replace(".", ":")
            anahtar = (g["aciklama"], gorev_saati, bugun)
            if gorev_saati == su_an and anahtar not in bildirilenler and gorev_bugun_mu(g["gun"], simdi.weekday()):
                print(f"\nHatırlatma zamanı geldi: {g['aciklama']} ({g['saat']})")
                bildirilenler.add(anahtar)
                messagebox.showinfo("Görev Hatırlatıcı", f"Görev: {g['aciklama']}\nSaat: {g['saat']}")

        time.sleep(5)
        #5 saniyede bir saati kontrol eder, bu kısımda daha uzun tutabilirdim ama
        #çok görev eklediğim için ve görevlerde hemen hemen aynı saatlere çok biriktiği için böyle yapmam daha doğru

# Hatırlatıcıyı arka planda başlatır, böylece menü kullanmaya devam edebilirim, iş aksamaz
def hatirlaticiyi_baslat(liste):
    global hatirlatici_thread
    if hatirlatici_thread is not None and hatirlatici_thread.is_alive():
        print("Hatırlatıcı zaten çalışıyor.")
        return
    hatirlatici_thread = threading.Thread(target=hatirlatici_dongusu, args=(liste,), daemon=True)
    hatirlatici_thread.start()
    print("Hatırlatıcı arka planda başlatıldı, menüyü kullanmaya devam edebilirsin.")

# Ana menünün döngüsü, sayılarla seçim yapmamı sağlıyor
gorev_listesi = gorevleri_getir()

while True:
    print("\n1- Görev Ekle")
    print("2- Tüm Görevleri Göster")
    print("3- Hatırlatıcıyı Başlat")
    print("4- Çıkış")

    secim = input("Seçiminiz: ")

    if secim == "1":
        gorev_ekle(gorev_listesi)
    elif secim == "2":
        gorevleri_listele(gorev_listesi)
    elif secim == "3":
        hatirlaticiyi_baslat(gorev_listesi)
    elif secim == "4":
        print("Program kapatıldı.")
        break
    else:
        print("Hatalı seçim yaptınız.")
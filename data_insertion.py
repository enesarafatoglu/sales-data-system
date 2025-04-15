import pandas as pd
from datetime import datetime
import re

def validate_input(urun, fiyat, miktar, satis_tarihi):
    """
    Kullanıcı girişlerini doğrular.
    Hatalı giriş varsa hata mesajı döndürür, yoksa None.
    """
    # Ürün adı: Boş olamaz, sadece harf ve boşluk (özel karakter veya sayı yok)
    if not urun or not urun.strip():
        return "Ürün adı boş olamaz."
    if not re.match(r'^[a-zA-Z\s]+$', urun.strip()):
        return "Ürün adı sadece harf ve boşluk içerebilir."

    # Fiyat: Pozitif bir sayı olmalı
    try:
        fiyat = float(fiyat)
        if fiyat <= 0:
            return "Fiyat sıfır veya negatif olamaz."
    except (ValueError, TypeError):
        return "Fiyat geçerli bir sayı olmalı (örn: 5000.0)."

    # Miktar: Pozitif bir tam sayı olmalı
    try:
        miktar = int(miktar)
        if miktar <= 0:
            return "Miktar sıfır veya negatif olamaz."
    except (ValueError, TypeError):
        return "Miktar geçerli bir tam sayı olmalı (örn: 10)."

    # Satış tarihi: YYYY-MM-DD formatında, 2025 ve sonrası
    try:
        tarih = datetime.strptime(satis_tarihi, "%Y-%m-%d")
        if tarih.year < 2025:
            return "Satış tarihi 2025 veya sonrası olmalı."
    except ValueError:
        return "Satış tarihi YYYY-MM-DD formatında olmalı (örn: 2025-04-10)."

    return None  # Hata yoksa None dön

def insert_user_data(conn, cursor):
    """Kullanıcıdan veri alır ve satislar tablosuna ekler (terminal için)."""
    print("\nYeni Satış Kaydı Ekle")
    urun = input("Ürün Adı: ")
    fiyat = input("Fiyat (örn: 5000.0): ")
    miktar = input("Miktar (örn: 10): ")
    satis_tarihi = input("Satış tarihi (YYYY-MM-DD, örn: 2025-04-10): ")

    # Girişleri doğrula
    error = validate_input(urun, fiyat, miktar, satis_tarihi)
    if error:
        print(f"Giriş hatası: {error}")
        return

    try:
        # Veritabanına ekle
        cursor.execute(
            "INSERT INTO satislar (urun, fiyat, miktar, satis_tarihi) VALUES (%s, %s, %s, %s)",
            (urun, float(fiyat), int(miktar), satis_tarihi)
        )
        conn.commit()
        print(f"{urun} başarıyla eklendi!")
    except Exception as e:
        print(f"Ekleme hatası: {e}")
        conn.rollback()

def insert_csv_data(conn, cursor, csv_file="yeni_satislar.csv"):
    """CSV dosyasından verileri okur ve satislar tablosuna ekler."""
    try:
        df_csv = pd.read_csv(csv_file)
        print("\nCSV Verileri:")
        print(df_csv)

        # CSV verilerini doğrula
        for _, row in df_csv.iterrows():
            error = validate_input(
                row["urun"], row["fiyat"], row["miktar"], row["satis_tarihi"]
            )
            if error:
                print(f"CSV satırı geçersiz: {error}")
                continue
            cursor.execute(
                "INSERT INTO satislar (urun, fiyat, miktar, satis_tarihi) VALUES (%s, %s, %s, %s)",
                (row["urun"], row["fiyat"], row["miktar"], row["satis_tarihi"])
            )
        conn.commit()
        print("CSV verileri veritabanına eklendi!")
        return df_csv
    except FileNotFoundError:
        print(f"Hata: {csv_file} dosyası bulunamadı!")
        return None
    except Exception as e:
        print(f"CSV ekleme hatası: {e}")
        conn.rollback()
        return None
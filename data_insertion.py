import pandas as pd
from datetime import datetime

def insert_user_data(conn, cursor):
    """Kullanıcıdan veri alır ve satislar tablosuna ekler."""
    print("\nYeni Satış Kaydı Ekle")
    try:
        urun = input("Ürün Adı: ")
        fiyat = float(input("Fiyat (örn: 5000.0): "))  # Float dönüşümü
        miktar = int(input("Miktar (örn: 10): "))      # Int dönüşümü
        satis_tarihi = input("Satış tarihi (YYYY-MM-DD, örn: 2025-04-10): ")

        # Tarihi doğrulama
        datetime.strptime(satis_tarihi, "%Y-%m-%d")

        # Veritabanına ekle
        cursor.execute(
            "INSERT INTO satislar (urun, fiyat, miktar, satis_tarihi) VALUES (%s, %s, %s, %s)",
            (urun, fiyat, miktar, satis_tarihi)
        )
        conn.commit()
        print(f"{urun} başarıyla eklendi!")
    except ValueError as e:
        print(f"Giriş hatası: {e}. Lütfen doğru formatta veri girin.")
        conn.rollback()
    except Exception as e:
        print(f"Ekleme hatası: {e}")
        conn.rollback()

def insert_csv_data(conn, cursor, csv_file="yeni_satislar.csv"):
    """CSV dosyasından verileri okur ve satislar tablosuna ekler."""
    try:
        df_csv = pd.read_csv(csv_file)
        print("\nCSV Verileri:")
        print(df_csv)

        # Verileri veritabanına ekle
        for _, row in df_csv.iterrows():
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
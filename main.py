import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from db_config import get_db_connection

import warnings
warnings.filterwarnings("ignore")

# Veritabanı bağlantısını al
conn = get_db_connection()
if conn is None:
    print("Bağlantı sağlanamadı, program sonlandırılıyor.")
    exit()

cursor = conn.cursor()

# Kullanıcıdan veri girişi
print("\nYeni Satış Kaydı Ekle")
try:
    urun = input("Ürün Adı: ")
    fiyat = input("Fiyat (örn: 5000.0): ")
    miktar = input("Miktar (örn: 10): ")
    satis_tarihi = input("Satış tarihi (YYYY-MM-DD, örn: 2025-04-10): ")

    # Tarihi doğrulama
    datetime.strptime(satis_tarihi, "%Y-%m-%d")

    # Veritabanına ekle 
    cursor.execute(
        "INSERT INTO satislar (urun,fiyat,miktar,satis_tarihi) VALUES (%s,%s,%s,%s)",
        (urun,fiyat,miktar,satis_tarihi)
    )
    conn.commit()
    print(f"{urun} başarıyla eklendi!")
except ValueError as e:
    print(f"Giriş hatası: {e}. Lütfen doğru formatta veri girin.")
except Exception as e:
    print(f"Ekleme hatası: {e}")
    conn.rollback()

# CSV'yi oku
try:
    df_csv = pd.read_csv("yeni_satislar.csv")
    print("CSV Verileri:")
    print(df_csv)
except FileNotFoundError:
    print("Hata: yeni_satislar.csv dosyası bulunamadı!")
    conn.close()
    exit()

# Verileri veritabanına ekle
for _, row in df_csv.iterrows():
    cursor.execute(
        "INSERT INTO satislar (urun, fiyat, miktar, satis_tarihi) VALUES (%s, %s, %s, %s)",
        (row["urun"], row["fiyat"], row["miktar"], row["satis_tarihi"])
    )
conn.commit()
print("CSV verileri veritabanına eklendi!")

# Yeni verileri kontrol et
df_son = pd.read_sql_query("SELECT * FROM satislar", conn)
print("\nGüncel Veriler:")
print(df_son)

# Görselleştirme 1: Ürün bazında toplam gelir (pasta grafiği)
query_pie = """
    SELECT urun, SUM(fiyat * miktar) AS toplam_gelir
    FROM satislar
    GROUP BY urun
"""
df_pie = pd.read_sql_query(query_pie, conn)
print("\nPasta Grafiği Verileri (Ürün Bazında Toplam Gelir): ")
print(df_pie)

# Pasta grafiği çiz
plt.figure(figsize=(7,7))
plt.pie(df_pie["toplam_gelir"], labels=df_pie["urun"], autopct="%1.1f%%", startangle=90)
plt.title("Ürün Bazında Gelir Dağılımı")
plt.axis("equal")
plt.show()

# Görselleştirme 2: Tarihe göre toplam miktar (alan grafiği)
query_area = """
    SELECT satis_tarihi, SUM(miktar) AS toplam_miktar
    FROM satislar
    GROUP BY satis_tarihi
    ORDER BY satis_tarihi
"""
df_area = pd.read_sql_query(query_area, conn)
print("\nAlan Grafiği Verileri (Tarihe Göre Toplam Miktar): ")
print(df_area)

# Alan grafiği çiz
plt.figure(figsize=(12,6))
plt.fill_between(df_area["satis_tarihi"], df_area["toplam_miktar"], color="skyblue", alpha=0.4)
plt.plot(df_area["satis_tarihi"], df_area["toplam_miktar"], color="slateblue", alpha=0.6)
plt.title("Tarihe Göre Toplam Satış Miktarı")
plt.xlabel("Tarih")
plt.ylabel("Toplam Miktar")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Görselleştirme 3: Tarihe göre toplam miktar (Plotly ile interaktif çizgi grafiği)
query_area = """
    SELECT satis_tarihi, SUM(miktar) AS toplam_miktar
    FROM satislar
    GROUP BY satis_tarihi
    ORDER BY satis_tarihi
"""
df_area = pd.read_sql_query(query_area, conn)
print("\nÇizgi Grafiği Verileri (Tarihe Göre Toplam Miktar):")
print(df_area)

# Plotly ile interaktif çizgi grafiği
fig = px.line(
    df_area,
    x="satis_tarihi",
    y="toplam_miktar",
    title="Tarihe Göre Toplam Satış Miktarı (İnteraktif)",
    labels={"satis_tarihi": "Tarih", "toplam_miktar": "Toplam Miktar"},
    markers=True
)
fig.update_layout(
    xaxis_title="Tarih",
    yaxis_title="Toplam Miktar",
    xaxis_tickangle=45,
    showlegend=True
)
fig.show()

# Güncelleme: Telefon miktarını 5 arttır
print("\nGüncelleme öncesi veriler: ")
df_ilk = pd.read_sql_query("SELECT * FROM satislar", conn)
print(df_ilk)

cursor.execute("UPDATE satislar SET miktar = miktar + 5 WHERE urun = 'Telefon'")
conn.commit()
print("\nTelefon miktarı güncellendi.")

# Güncellenmiş verileri göster
print("\nGüncelleme sonrası veriler: ")
df_guncel = pd.read_sql_query("SELECT * FROM satislar", conn)
print(df_guncel)

# Silme: 2025-03-01'den eski kayıtları sil
cursor.execute("DELETE FROM satislar WHERE satis_tarihi < '2025-03-01'")
conn.commit()
print("\n2025-03-01'den eski kayıtları silindi.")

# Son durumu göster
print("\nSilme sonrası veriler: ")
df_son = pd.read_sql_query("SELECT * FROM satislar", conn)
print(df_son)

# Bağlantıyı kapat
cursor.close()
conn.close()
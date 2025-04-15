import pandas as pd
from db_config import get_db_connection

import warnings
warnings.filterwarnings("ignore")

# Veritabanı bağlantısını al
conn = get_db_connection()
if conn is None:
    print("Bağlantı sağlanamadı, program sonlandırılıyor.")
    exit()

cursor = conn.cursor()

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

# Bağlantıyı kapat
cursor.close()
conn.close()
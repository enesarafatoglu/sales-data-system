import pandas as pd

# Örnek CSV verisi
yeni_veriler = pd.DataFrame({
    "urun": ["Mouse", "Klavye", "Monitör", "Telefon"],
    "fiyat": [200.0, 300.0, 4000.0, 6000.0],
    "miktar": [100, 80, 20, 15],
    "satis_tarihi": ["2025-04-10", "2025-04-12", "2025-04-15", "2025-04-20"]
})

# CSV'ye kaydet
yeni_veriler.to_csv("yeni_satislar.csv", index=False)
print("yeni_satislar.csv oluşturuldu!")
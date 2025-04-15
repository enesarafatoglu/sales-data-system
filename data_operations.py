import pandas as pd

def update_phone_quantity(conn, cursor):
    """Telefon ürününün miktarını 5 artırır."""
    print("\nGüncelleme öncesi veriler:")
    df_ilk = pd.read_sql_query("SELECT * FROM satislar", conn)
    print(df_ilk)

    cursor.execute("UPDATE satislar SET miktar = miktar + 5 WHERE urun = 'Telefon'")
    conn.commit()
    print("\nTelefon miktarı güncellendi.")

    print("\nGüncelleme sonrası veriler:")
    df_guncel = pd.read_sql_query("SELECT * FROM satislar", conn)
    print(df_guncel)

def delete_old_records(conn, cursor, date_threshold="2025-03-01"):
    """Belirtilen tarihten eski kayıtları siler."""
    cursor.execute("DELETE FROM satislar WHERE satis_tarihi < %s", (date_threshold,))
    conn.commit()
    print(f"\n{date_threshold}'den eski kayıtlar silindi.")

    print("\nSilme sonrası veriler:")
    df_son = pd.read_sql_query("SELECT * FROM satislar", conn)
    print(df_son)

def print_current_data(conn):
    """Mevcut verileri ekrana yazdırır."""
    df_son = pd.read_sql_query("SELECT * FROM satislar", conn)
    print("\nGüncel Veriler:")
    print(df_son)
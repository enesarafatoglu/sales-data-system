import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from data_insertion import validate_input

def create_gui(conn, cursor):
    """Satış verisi eklemek ve görüntülemek için GUI oluşturur."""
    window = tk.Tk()
    window.title("Satış Veri Girişi")
    window.geometry("600x400")

    # Giriş formu
    tk.Label(window, text="Ürün Adı:").grid(row=0, column=0, padx=10, pady=5)
    entry_urun = tk.Entry(window)
    entry_urun.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Fiyat (örn: 5000.0):").grid(row=1, column=0, padx=10, pady=5)
    entry_fiyat = tk.Entry(window)
    entry_fiyat.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Miktar (örn: 10):").grid(row=2, column=0, padx=10, pady=5)
    entry_miktar = tk.Entry(window)
    entry_miktar.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="Satış Tarihi (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    entry_tarih = tk.Entry(window)
    entry_tarih.grid(row=3, column=1, padx=10, pady=5)

    # Mesaj alanı
    mesaj_label = tk.Label(window, text="", wraplength=500)
    mesaj_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def ekle_buton_aksiyon():
        """Ekle butonuna basıldığında veri ekler."""
        urun = entry_urun.get()
        fiyat = entry_fiyat.get()
        miktar = entry_miktar.get()
        tarih = entry_tarih.get()

        # Girişleri doğrula
        error = validate_input(urun, fiyat, miktar, tarih)
        if error:
            mesaj_label.config(text=f"Hata: {error}", fg="red")
            return

        try:
            cursor.execute(
                "INSERT INTO satislar (urun, fiyat, miktar, satis_tarihi) VALUES (%s, %s, %s, %s)",
                (urun, float(fiyat), int(miktar), tarih)
            )
            conn.commit()
            mesaj_label.config(text=f"{urun} başarıyla eklendi!", fg="green")
            # Giriş alanlarını temizle
            entry_urun.delete(0, tk.END)
            entry_fiyat.delete(0, tk.END)
            entry_miktar.delete(0, tk.END)
            entry_tarih.delete(0, tk.END)
        except Exception as e:
            mesaj_label.config(text=f"Ekleme hatası: {e}", fg="red")
            conn.rollback()

    def goster_buton_aksiyon():
        """Verileri tablo olarak gösterir."""
        try:
            df = pd.read_sql_query("SELECT * FROM satislar", conn)
            # Yeni pencere aç
            table_window = tk.Toplevel(window)
            table_window.title("Satış Verileri")
            table_window.geometry("600x400")

            # Tablo oluştur
            tree = ttk.Treeview(table_window, columns=("ID", "Ürün", "Fiyat", "Miktar", "Tarih"), show="headings")
            tree.heading("ID", text="ID")
            tree.heading("Ürün", text="Ürün")
            tree.heading("Fiyat", text="Fiyat")
            tree.heading("Miktar", text="Miktar")
            tree.heading("Tarih", text="Tarih")
            tree.pack(fill="both", expand=True)

            # Verileri tabloya ekle
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=(
                    row["id"], row["urun"], row["fiyat"], row["miktar"], row["satis_tarihi"]
                ))
        except Exception as e:
            messagebox.showerror("Hata", f"Veri çekme hatası: {e}")

    # Butonlar
    tk.Button(window, text="Ekle", command=ekle_buton_aksiyon).grid(row=5, column=0, padx=10, pady=10)
    tk.Button(window, text="Verileri Göster", command=goster_buton_aksiyon).grid(row=5, column=1, padx=10, pady=10)

    window.mainloop()

    # Pencere kapandığında bağlantıyı kapat
    cursor.close()
    conn.close()
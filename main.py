from db_config import get_db_connection
from data_insertion import insert_csv_data
from visualization import plot_pie_chart, plot_area_chart, plot_interactive_line_chart
from data_operations import update_phone_quantity, delete_old_records, print_current_data
from gui import create_gui

import warnings
warnings.filterwarnings("ignore")

# Veritabanı bağlantısını al
conn = get_db_connection()
if conn is None:
    print("Bağlantı sağlanamadı, program sonlandırılıyor...")
    exit()

cursor = conn.cursor()

# GUI ile veri girişi
create_gui(conn, cursor) # GUI çalışır, kapandığında bağlantı kapanır

# Yeni bağlantı aç (GUI bağlantıyı kapattığı için)
conn = get_db_connection()
if conn is None:
    print("Bağlantı sağlanamadı, program sonlandırılıyor...")
    exit()
cursor = conn.cursor()

# Diğer işlemler
insert_csv_data(conn, cursor)           # CSV'den veri ekle
print_current_data(conn)                # Güncel verileri göster
plot_pie_chart(conn)                    # Pasta grafiği
plot_area_chart(conn)                   # Alan grafiği
plot_interactive_line_chart(conn)       # Plotly interaktif grafik
update_phone_quantity(conn, cursor)     # Telefon miktarını güncelle
delete_old_records(conn, cursor)        # Eski kayıtları sil

# Bağlantıyı kapat
cursor.close()
conn.close()
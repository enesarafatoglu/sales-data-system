import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def plot_pie_chart(conn):
    """Ürün bazında toplam gelir için pasta grafiği çizer."""
    query_pie = """
        SELECT urun, SUM(fiyat * miktar) AS toplam_gelir
        FROM satislar
        GROUP BY urun
    """
    df_pie = pd.read_sql_query(query_pie, conn)
    print("\nPasta Grafiği Verileri (Ürün Bazında Toplam Gelir):")
    print(df_pie)

    plt.figure(figsize=(7, 7))
    plt.pie(df_pie["toplam_gelir"], labels=df_pie["urun"], autopct="%1.1f%%", startangle=90)
    plt.title("Ürün Bazında Gelir Dağılımı")
    plt.axis("equal")
    plt.show()

def plot_area_chart(conn):
    """Tarihe göre toplam miktar için alan grafiği çizer."""
    query_area = """
        SELECT satis_tarihi, SUM(miktar) AS toplam_miktar
        FROM satislar
        GROUP BY satis_tarihi
        ORDER BY satis_tarihi
    """
    df_area = pd.read_sql_query(query_area, conn)
    print("\nAlan Grafiği Verileri (Tarihe Göre Toplam Miktar):")
    print(df_area)

    plt.figure(figsize=(12, 6))
    plt.fill_between(df_area["satis_tarihi"], df_area["toplam_miktar"], color="skyblue", alpha=0.4)
    plt.plot(df_area["satis_tarihi"], df_area["toplam_miktar"], color="slateblue", alpha=0.6)
    plt.title("Tarihe Göre Toplam Satış Miktarı")
    plt.xlabel("Tarih")
    plt.ylabel("Toplam Miktar")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_interactive_line_chart(conn):
    """Tarihe göre toplam miktar için Plotly interaktif çizgi grafiği çizer."""
    query_area = """
        SELECT satis_tarihi, SUM(miktar) AS toplam_miktar
        FROM satislar
        GROUP BY satis_tarihi
        ORDER BY satis_tarihi
    """
    df_area = pd.read_sql_query(query_area, conn)
    print("\nÇizgi Grafiği Verileri (Tarihe Göre Toplam Miktar):")
    print(df_area)

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
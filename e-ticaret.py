import os
import pandas as pd
import pyodbc
import seaborn as sns
import matplotlib.pyplot as plt

# Genel ayarlar 
OUTPUT_DIR = "outputs/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False
sns.set(style="whitegrid")

#  1) SQL bağlantısı 
try:
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=DESKTOP-6BGTUJ7;"   # kendi server adınla değiştir
        "Database=EcommerceDB;"     # veritabanı adınla değiştir
        "Trusted_Connection=yes;"
    )
    print(" SQL bağlantısı başarılı.")
except Exception as e:
    print(" Bağlantı hatası:", e)
    raise SystemExit(1)

#  2) Veriyi çekme işlemi
query = "SELECT InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country FROM dbo.data;"
df = pd.read_sql(query, conn)  # uyarı çıktıysa SQLAlchemy ile de yapılabilir
conn.close()

print("\nVeri ilk 5 satır:")
print(df.head())

#  3) Temizleme & tip dönüşümleri 
# Tarih dönüşümü
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# Sayısal dönüşümler (hatalı/boş -> NaN)
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')

# Toplam tutar kolonu
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Eksik veya anlamsız satırları temizleyelim (ör: Quantity/UnitPrice NaN veya negatif işlemler isteğe bağlı)
initial_count = len(df)
df = df.dropna(subset=['Quantity', 'UnitPrice', 'InvoiceDate'])
# Opsiyonel: negatif Quantity (iptaller) kalabilir; isterseniz filtreleyin
# df = df[df['Quantity'] > 0]

cleaned_count = len(df)
print(f"\nVeri temizlendi: {initial_count} -> {cleaned_count} gözlem")

# 4) Temel istatistikler 
print("\n--- Temel İstatistikler (TotalPrice) ---")
print(df['TotalPrice'].describe().to_string())

#  5) En çok gelir getiren 10 ürün (Description) 
top_products = (
    df.groupby("Description")["TotalPrice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\nEn çok gelir getiren 10 ürün:")
print(top_products)

plt.figure(figsize=(10,6))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("En Çok Gelir Getiren 10 Ürün")
plt.xlabel("Toplam Gelir")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_10_products.png", dpi=300)
plt.close()

#  6) Kategori bazlı toplam satış (eğer ProductCategory yoksa Country bazlı göster) 
if 'ProductCategory' in df.columns:
    cat_sales = df.groupby('ProductCategory')['TotalPrice'].sum().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(x=cat_sales.values, y=cat_sales.index, palette="coolwarm")
    plt.title("Kategoriye Göre Toplam Satış")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/category_sales.png", dpi=300)
    plt.close()
else:
    country_sales = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(15)
    plt.figure(figsize=(10,6))
    sns.barplot(x=country_sales.values, y=country_sales.index, palette="mako")
    plt.title("Ülkelere Göre Toplam Satış (Top 15)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/country_sales_top15.png", dpi=300)
    plt.close()

#  7) Zaman serisi: aylık satış trendi 
df['Month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
monthly = df.groupby('Month')['TotalPrice'].sum().reset_index()

plt.figure(figsize=(12,5))
sns.lineplot(data=monthly, x='Month', y='TotalPrice', marker='o')
plt.xticks(rotation=45)
plt.title("Aylık Satış Hacmi")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/monthly_sales.png", dpi=300)
plt.close()

#  8) En çok harcayan müşteriler 
top_customers = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print("\nEn çok harcayan 10 müşteri:")
print(top_customers)

plt.figure(figsize=(10,6))
sns.barplot(x=top_customers.values, y=top_customers.index.astype(str), palette="viridis")
plt.title("En Çok Harcayan 10 Müşteri")
plt.xlabel("Toplam Harcama")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_customers.png", dpi=300)
plt.close()

# 9) Korelasyon analizi 
num_cols = ['Quantity', 'UnitPrice', 'TotalPrice']
corr = df[num_cols].corr()

plt.figure(figsize=(5,4))
sns.heatmap(corr, annot=True, cmap="mako", fmt=".2f")
plt.title("Sayısal Değişkenler Korelasyonu")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/correlation_matrix.png", dpi=300)
plt.close()

print("\n Analiz tamamlandı. Grafikler kaydedildi:", OUTPUT_DIR)

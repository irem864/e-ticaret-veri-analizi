# E-Ticaret Veri Analizi Projesi | E-Commerce Data Analysis Project

#  Proje Açıklaması | Project Description

Bu proje, bir **e-ticaret satış verisi** üzerinden **veri analizi** yaparak satış trendlerini, ürün performansını ve müşteri davranışlarını incelemeyi amaçlamaktadır.  
Veriler SQL veritabanından **PyODBC** kütüphanesiyle çekilmiş ve **Pandas**, **Matplotlib** ve **Seaborn** kullanılarak analiz edilmiştir.

This project analyzes **e-commerce sales data** to explore sales trends, product performance, and customer behavior.  
The dataset is fetched from an SQL database using **PyODBC**, and analyzed using **Pandas**, **Matplotlib**, and **Seaborn**.

---

##  Kullanılan Teknolojiler | Technologies Used

| Kategori | Araçlar / Kütüphaneler |
|-----------|------------------------|
| Veri Kaynağı (Database) | SQL Server, PyODBC |
| Veri Analizi | Python, Pandas, Numpy |
| Görselleştirme | Matplotlib, Seaborn |
| Ortam | Visual Studio Code, Jupyter Notebook |

---

##  Proje Yapısı | Project Structure

 e-ticaret-veri-analizi
 
│

├── e-ticaret.py # Ana Python dosyası / Main analysis file

├──data.csv # Örnek veri seti / Sample dataset

---

###Nasıl Çalıştırılır | How to Run

###  1. Gerekli Kütüphaneleri Kurunuz
```bash
pip install pandas pyodbc matplotlib seaborn


 ###2. Veritabanı Bağlantısını Ayarlayın

e-ticaret.py içinde aşağıdaki bağlantıyı kendi sisteminize göre düzenleyin:

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=YOUR_SERVER_NAME;"
    "Database=EcommerceDB;"
    "Trusted_Connection=yes;"
)

 ###3. Çalıştırın : python e-ticaret.py


 Öne Çıkan Analizler | Key Insights

 En çok gelir getiren ürün kategorileri

 En aktif müşteriler

 Satışların zamana göre değişimi

 Ülkelere göre satış dağılımı

These analyses include:

 Top revenue-generating product categories

Most active customers

 Time-based sales trends

 Country-based sales distribution


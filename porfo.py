import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Judul Portofolio
st.title("Portofolio Analisis Data")

# Informasi Pribadi
st.header("Informasi Pribadi")
st.write("Nama: Annas As Sidik")
st.write("Email: annas.assidiq10@gmail.com")
st.write("[LinkedIn](https://www.linkedin.com/in/...) | [GitHub](https://github.com/...)")

# Proyek 1
st.header("Data-Driven Inventory Management Optimization for Retail Efficiency and Profitability")
st.write("""
*Gaols*: 
- Mengoptimalkan manajemen inventaris untuk mengurangi biaya penyimpanan dan mencegah kekurangan stok.
- Meningkatkan efisiensi pengadaan dengan menggunakan analisis cost-benefit berbasis data.
""")

st.write("*Tools*: Python, Pandas, Matplotlib")

# Load Dataset
data = pd.read_csv("./retail_store_inventory_final.csv")  # Ganti dengan dataset Anda
st.write("*Dataset*:")
st.write(data.head())

# Kolom numerik untuk analisis
numeric_cols = [
    'Inventory Level', 'Safety Stock', 'Units Sold', 'Units Ordered', 'Demand Forecast',
    'Price', 'Order Cost', 'Daily Unit Holding Cost', 'Estimated Lead Time', 'Discount',
    'Competitor Pricing'
]

# Kolom kategori
category_cols = [
    'Store ID', 'Product ID', 'Category', 'Region', 'Weather Condition', 
    'Holiday/Promotion', 'Seasonality'
]

# Kolom waktu
times_cols = ['Date']

# Fungsi EOQ, ROP, dan Safety Stock
def ordering_cost(data, month=None, category=None, store_id=None):
    # Memfilter data berdasarkan bulan jika diberikan
    if month:
        data = data[data['Month'].isin(month)]
    if store_id:
        data = data[data['Store ID'].isin(store_id)]
    if category:
        data = data[data['Category'].isin(category)]
    
    # Mengelompokkan data dan menghitung total
    result = (
        data.groupby('Store ID')[['Total Ordering Cost', 'Total Ordering Cost EOQ', 'Total Ordering Cost JIT']]
        .sum()
        .reset_index()
    )
    return result    

# Fungsi Holding Cost
def Holding_cost(data, month=None, category=None, store_id=None):
    if month:
        data = data[data['Month'].isin(month)]
    if store_id:
        data = data[data['Store ID'].isin(store_id)]
    if category:
        data = data[data['Category'].isin(category)]
    
    result = (
        data.groupby('Store ID')[['Total Holding Cost', 'Total Holding Cost EOQ', 'Total Holding Cost JIT']]
        .sum()
        .reset_index()
    )
    return result

# Fungsi Total Cost
def Total_cost(data, month=None, category=None, store_id=None):
    if month:
        data = data[data['Month'].isin(month)]
    if store_id:
        data = data[data['Store ID'].isin(store_id)]
    if category:
        data = data[data['Category'].isin(category)]
    
    result = (
        data.groupby('Store ID')[['Total Cost', 'Total Cost EOQ', 'Total Cost JIT']]
        .sum()
        .reset_index()
    )
    return result

# Fungsi Inventory Turnover
def InventoryTurnover(data, month=None, category=None, store_id=None):
    if month:
        data = data[data['Month'].isin(month)]
    if store_id:
        data = data[data['Store ID'].isin(store_id)]
    if category:
        data = data[data['Category'].isin(category)]
    
    result = (
        data.groupby('Store ID')[['Inventory Turnover', 'Inventory Turnover EOQ', 'Inventory Turnover JIT']]
        .sum()
        .reset_index()
    )
    return result

# Fungsi Profit
def Profit(data, month=None, category=None, store_id=None):
    if month:
        data = data[data['Month'].isin(month)]
    if store_id:
        data = data[data['Store ID'].isin(store_id)]
    if category:
        data = data[data['Category'].isin(category)]
    
    result = (
        data.groupby('Store ID')[['Profit', 'Profit EOQ', 'Profit JIT']]
        .sum()
        .reset_index()
    )
    return result

# Fungsi untuk memformat angka besar (K untuk ribuan, M untuk jutaan)
def humanize_number(num):
    if num >= 1_000_000:
        return f'{num/1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num/1_000:.1f}K'
    else:
        return f'{num:.0f}'

# Streamlit UI
st.title("Analisis Perhitungan Ordering Cost per Store")

# Pilihan filter bulan, kategori, dan store ID
month_selected = st.multiselect("Pilih Bulan:", list(range(1, 13)), default=list(range(1, 13)))
category_selected = st.multiselect("Pilih Kategori:", data["Category"].unique(), default=data["Category"].unique())
store_selected = st.multiselect("Pilih Store ID:", data["Store ID"].unique(), default=data["Store ID"].unique())

# Filter data dengan fungsi
ordingCost = ordering_cost(data, month_selected, category_selected, store_selected)
holdingCost = Holding_cost(data, month_selected, category_selected, store_selected)
totalCost = Total_cost(data, month_selected, category_selected, store_selected)
inventoryTurnover = InventoryTurnover(data, month_selected, category_selected, store_selected)
profit = Profit(data, month_selected, category_selected, store_selected)

# Visualisasi Data
# Plot Heatmap Korelasi
st.subheader("Heatmap Korelasi")
fig, ax = plt.subplots(figsize=(8,6))
correlation = data[numeric_cols].corr()
sns.heatmap(correlation, annot=True, fmt='.2f', cmap='Blues', ax=ax)
st.pyplot(fig)

# Plot Bar Chart untuk setiap cost dan metrik lainnya
def plot_comparison(data, title, x_col, y_cols, ylabel, custom_palette):
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind='bar', x=x_col, y=y_cols, ax=ax, color=custom_palette)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(humanize_number(height), (p.get_x() + p.get_width() / 2., height), ha='center', va='center', fontsize=7, color='black', xytext=(0, 8), textcoords='offset points')
    
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("Store ID", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticklabels(data[x_col], rotation=45)
    ax.legend(title="Jenis Cost", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

# Panggil fungsi untuk setiap visualisasi
if ordingCost is not None and not ordingCost.empty:
    plot_comparison(ordingCost, "Perbandingan Ordering Cost per Store ID", 'Store ID', ['Total Ordering Cost', 'Total Ordering Cost EOQ', 'Total Ordering Cost JIT'], "Total Ordering Cost", ['#003366', '#0055A4', '#ADD8E6'])

if holdingCost is not None and not holdingCost.empty:
    plot_comparison(holdingCost, "Perbandingan Holding Cost per Store ID", 'Store ID', ['Total Holding Cost', 'Total Holding Cost EOQ', 'Total Holding Cost JIT'], "Total Holding Cost", ['#003366', '#0055A4', '#ADD8E6'])

if totalCost is not None and not totalCost.empty:
    plot_comparison(totalCost, "Perbandingan Total Cost per Store ID", 'Store ID', ['Total Cost', 'Total Cost EOQ', 'Total Cost JIT'], "Total Cost", ['#003366', '#0055A4', '#ADD8E6'])

if inventoryTurnover is not None and not inventoryTurnover.empty:
    plot_comparison(inventoryTurnover, "Perbandingan Inventory Turnover per Store ID", 'Store ID', ['Inventory Turnover', 'Inventory Turnover EOQ', 'Inventory Turnover JIT'], "Inventory Turnover", ['#003366', '#0055A4', '#ADD8E6'])

if profit is not None and not profit.empty:
    plot_comparison(profit, "Perbandingan Profit per Store ID", 'Store ID', ['Profit', 'Profit EOQ', 'Profit JIT'], "Profit", ['#003366', '#0055A4', '#ADD8E6'])


# Kesimpulan
# st.write("*Kesimpulan*: Jelaskan temuan utama dari analisis.")
# Filter relevant columns for the cost analysis
# Fungsi untuk menampilkan Ringkasan Analisis
st.title("Ringkasan Analisis & Rekomendasi Bisnis")

st.header("📊 **Ringkasan Analisis**")

st.markdown("""
- **Pengelolaan Inventaris dengan EOQ**: Mengurangi biaya penyimpanan hingga **31-32%** dan meningkatkan **Inventory Turnover** sebesar **59.2%**.
- **Mitigasi Stockout dan Biaya Penyimpanan dengan JIT**: Mengurangi biaya penyimpanan hingga **66-67%** dan mengurangi biaya total hingga **43.9%**. **Stockout rate** juga berkurang signifikan.
- **Kombinasi EOQ dan JIT**: Efektif untuk produk dengan permintaan campuran, dengan EOQ menjaga stok stabil dan JIT mengelola lonjakan permintaan musiman.
""")

st.header("💡 **Business Recommendations**")

st.subheader("1. Optimalkan Pengelolaan Inventaris dengan EOQ")
st.markdown("""
**Implementasi**: Gunakan EOQ untuk produk dengan permintaan stabil seperti **Clothing** dan **Groceries**.  
**Tujuan**: Mengurangi biaya penyimpanan dan menghindari **overstocking**.  
**Business Metrics**:
- **Cost Savings**: Pengurangan biaya penyimpanan yang lebih efisien.
- **Inventory Turnover**: Peningkatan perputaran stok sebesar **59.2%**.
  
**Analisis**: Penghematan biaya penyimpanan rata-rata **31-32%** dengan **EOQ**.
""")

st.subheader("2. Mitigasi Stockout dan Biaya Penyimpanan dengan JIT")
st.markdown("""
**Implementasi**: Terapkan JIT untuk produk dengan permintaan fluktuatif seperti **Electronics** dan **Furniture**.  
**Tujuan**: Menurunkan **stockout rate** dan biaya penyimpanan.  
**Business Metrics**:
- **Cost Savings**: Penghematan biaya penyimpanan hingga **66-67%**.
- **Stockout Rate**: Mengurangi frekuensi kekurangan stok.
  
**Analisis**: Pengurangan biaya total hingga **43.9%**, meningkatkan likuiditas dan profitabilitas.
""")

st.subheader("3. Kombinasikan EOQ dan JIT untuk Produk dengan Pola Permintaan Campuran")
st.markdown("""
**Implementasi**: Gabungkan **EOQ** untuk menjaga stok stabil pada produk dengan permintaan stabil, dan **JIT** untuk menangani lonjakan permintaan musiman.  
**Tujuan**: Mengoptimalkan **biaya penyimpanan** dan memastikan ketersediaan stok yang tepat waktu.  
**Business Metrics**:
- **Cost Savings**: Mengurangi biaya pengadaan yang tidak perlu.
- **Inventory Turnover**: Meningkatkan perputaran stok untuk kategori produk musiman.

**Analisis**: Kombinasi **EOQ** dan **JIT** memungkinkan efisiensi biaya dan menjaga ketersediaan stok yang optimal.
""")

st.markdown("""
Dengan pendekatan ini, perusahaan dapat mengoptimalkan biaya penyimpanan, mengurangi risiko stockout, dan meningkatkan **Inventory Turnover**, yang pada akhirnya berkontribusi pada peningkatan **cash flow** dan **profitabilitas** perusahaan.
""")


# Kontak
st.header("Hubungi Saya")
st.write("Silakan hubungi saya melalui email di annas.assidiq10@gamil.com.")
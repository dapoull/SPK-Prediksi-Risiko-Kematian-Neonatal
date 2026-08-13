import streamlit as st
import joblib
import pandas as pd
import numpy as np
# Import yang diperlukan untuk file upload (excel)
from io import BytesIO 

# ==============================================================================
# 1. MUAT MODEL DAN FITUR
# ==============================================================================
try:
    model = joblib.load('model_neonatal_dt.joblib')
    feature_columns = joblib.load('feature_columns.joblib')
    le = joblib.load('label_encoder.joblib') 
except FileNotFoundError:
    st.error("Error: Pastikan file model, fitur, dan encoder berada di folder yang sama.")
    st.stop()


# ==============================================================================
# 2. KONFIGURASI TAMPILAN
# ==============================================================================
st.set_page_config(page_title="Sistem Pendukung Keputusan Risiko Neonatal", layout="wide")

st.title("Sistem Pendukung Keputusan Prediksi Risiko Kematian Neonatal")
st.markdown("---")


# ==============================================================================
# 3. INPUT DATA (Dipisahkan menjadi Single dan Bulk)
# ==============================================================================
st.header("Mode Prediksi")
mode = st.radio(
    "Pilih Mode Input Data:",
    ('Input Satu Data (Manual)', 'Input Banyak Data (Upload File Excel)'),
    horizontal=True
)

st.markdown("---")

#MODE 1: SINGLE PREDICTION
if mode == 'Input Satu Data (Manual)':
    st.subheader("Input Data Bayi Baru Lahir (Manual)")
    # Input manual
    col1, col2 = st.columns(2)

    with col1:
        birth_weight = st.number_input("1. Berat Badan Lahir (kg)", min_value=0.5, max_value=5.5, value=2.8, step=0.01, key='bw_single')
        gestational_age = st.number_input("2. Usia Kehamilan (minggu)", min_value=20, max_value=45, value=34, step=1, key='ga_single')
        antenatal_visits = st.number_input("3. Kunjungan Antenatal (kali)", min_value=0, max_value=10, value=4, step=1, key='av_single')

    with col2:
        maternal_age = st.number_input("4. Usia Ibu (tahun)", min_value=15, max_value=50, value=25, step=1, key='ma_single')
        breastfeeding_init = st.number_input("5. Inisiasi ASI (jam setelah lahir)", min_value=0, max_value=24, value=8, step=1, key='bi_single')
        delivery_complication = st.selectbox("6. Komplikasi Persalinan Utama", ['None', 'Asphyxia', 'Sepsis', 'Preeclampsia'], key='dc_single')
        place_of_delivery = st.selectbox("7. Tempat Persalinan", ['Hospital', 'Clinic', 'Home'], key='pd_single')
    
    # LOGIKA PREDIKSI SATU DATA
    if st.button("PREDIKSI RISIKO KEMATIAN"):
        # 1. BUAT DATAFRAME KOSONG DENGAN URUTAN KOLOM YANG TEPAT
        input_data = pd.DataFrame(0, index=[0], columns=feature_columns)
        
        # 2. MASUKKAN INPUT NUMERIK
        input_data['Birth_Weight_kg'] = birth_weight
        input_data['Gestational_Age_weeks'] = gestational_age
        input_data['Maternal_Age_years'] = maternal_age
        input_data['Antenatal_Visits'] = antenatal_visits
        input_data['Breastfeeding_Initiation_hrs'] = breastfeeding_init
        
        # 3. MASUKKAN INPUT KATEGORI (ONE-HOT ENCODING)
        
        # Komplikasi
        komplikasi_kolom = f'Delivery_Complications_{delivery_complication}'
        if komplikasi_kolom in input_data.columns:
            input_data[komplikasi_kolom] = 1
        
        # Tempat Lahir
        place_kolom = f'Place_of_Delivery_{place_of_delivery}'
        if place_kolom in input_data.columns:
            input_data[place_kolom] = 1
        
        input_df = input_data[feature_columns] # Pastikan urutan kolom
    
        # 4. PREDIKSI MENGGUNAKAN MODEL
        prediction_numeric = model.predict(input_df)
        result_label = le.inverse_transform(prediction_numeric)[0]
        
        # 5. Tampilkan Hasil
        st.markdown("---")
        st.header("HASIL PREDIKSI RISIKO")
        
        if result_label == 'Died':
            st.error(f"⚠️ **PREDIKSI: BAYI MATI (RISIKO TINGGI)**")
            st.write("Rekomendasi: Intervensi dan perawatan intensif harus segera dipertimbangkan.")
        else:
            st.success(f"✅ **PREDIKSI: BAYI HIDUP (RISIKO RENDAH)**")
            st.write("Rekomendasi: Lanjutkan dengan protokol pengawasan standar.")
        
        st.subheader("Detail Input Data:")
        st.dataframe(input_df)

# --- MODE 2: BULK PREDICTION (Fitur Baru) ---
elif mode == 'Input Banyak Data (Upload File Excel)':
    st.subheader("Upload File Dataset (Excel atau CSV)")
    
    uploaded_file = st.file_uploader(
        "Pilih file Excel (.xlsx) atau CSV (.csv)",
        type=['xlsx', 'csv']
    )

    if uploaded_file is not None:
        try:
            # Baca file ke DataFrame
            if uploaded_file.name.endswith('.csv'):
                data_bulk = pd.read_csv(uploaded_file)
            else:
                data_bulk = pd.read_excel(uploaded_file)
            
            st.write("Preview Data yang Diunggah:")
            st.dataframe(data_bulk.head())

            # PREPROCESSING UNTUK BULK DATA
            
            # 1. Melakukan One-Hot Encoding pada data yang diunggah
            data_encoded = pd.get_dummies(data_bulk)
            
            # 2. Reindexing/Aligning Kolom
            # Buat DataFrame kosong dengan semua feature_columns yang dibutuhkan model
            final_data = pd.DataFrame(0, index=data_encoded.index, columns=feature_columns)
            
            # Isi kolom yang ada dari data_encoded ke final_data
            # Ini sangat penting agar data_input memiliki urutan dan kolom yang sama
            for col in final_data.columns:
                if col in data_encoded.columns:
                    final_data[col] = data_encoded[col]
            
            # PREDIKSI BATCH
            st.markdown("---")
            st.subheader(f"Hasil Prediksi untuk {len(final_data)} Baris Data")
            
            # 3. Prediksi pada seluruh DataFrame
            with st.spinner('Model sedang memprediksi risiko untuk semua data...'):
                predictions_numeric = model.predict(final_data)
                
                # 4. Terjemahkan hasil numerik (0/1) ke label teks
                predictions_labels = le.inverse_transform(predictions_numeric)
            
            # 5. Tambahkan hasil prediksi ke DataFrame asli
            data_bulk['Prediksi_Outcome'] = predictions_labels
            
            # 6. Tampilkan dan Sediakan Opsi Download
            st.success("Prediksi Selesai!")
            
            # Tampilkan 10 baris teratas hasil
            st.dataframe(data_bulk.head(10)) 
            
            # Tombol Download Hasil
            @st.cache_data
            def convert_df(df):
                # Fungsi untuk mengkonversi DataFrame ke CSV untuk di-download
                return df.to_csv(index=False).encode('utf-8')

            csv = convert_df(data_bulk)

            st.download_button(
                label="📥 Download Hasil Prediksi (.csv)",
                data=csv,
                file_name='hasil_prediksi_neonatal.csv',
                mime='text/csv',
            )
            
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memproses file. Pastikan nama kolom sudah benar. Error: {e}")
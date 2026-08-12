# SPK Prediksi Risiko Kematian Neonatal

Sistem Pendukung Keputusan (SPK) berbasis Machine Learning menggunakan algoritma **Decision Tree** untuk memprediksi risiko kematian neonatal (28 hari pertama) berdasarkan data klinis awal ibu dan bayi 

---

## Latar Belakang & Masalah Utama

* **Kematian Neonatal:** Merupakan indikator krusial kualitas layanan kesehatan di suatu negara
* **Risiko Tinggi:** Kondisi seperti Berat Badan Lahir Rendah (BBLR), Asfiksia, dan kelahiran prematur membutuhkan penanganan cepat dan akurat
* **Tantangan Data:** Pengolahan data klinis yang memiliki *missing values* serta ketidakseimbangan kelas (*imbalanced data*)

---

## Poin Utama Proyek & Metodologi

1. **Pengolahan Data**
   * Mengoptimalkan dataset 500 baris dengan menangani 307 *missing values*
   * Menerapkan **SMOTE** (*Synthetic Minority Over-sampling Technique*) untuk mengatasi *imbalanced data*, sehingga meningkatkan nilai *Recall* pada kelas minoritas (*Died*)

2. **Pemodelan Machine Learning**
   * Membangun algoritma **Decision Tree** dengan rasio *data split* 70:30
   * Berhasil mencapai **Akurasi 86.00%**

3. **Faktor Dominan (*Feature Importance*)**
   Mengidentifikasi 3 faktor risiko paling dominan terhadap kematian neonatal:
   * **Berat Badan Lahir (BBLR)**
   * **Kondisi Asfiksia**
   * **Usia Kehamilan (Prematuritas)**

4. **Implementasi**
   * Menyediakan *prototype* Sistem Pendukung Keputusan interaktif berbasis Streamlit
   * Menyederhanakan aturan keputusan menggunakan *if-then rules* dari *tree* untuk membantu pengambilan keputusan klinis secara cepat

---

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

1. **Clone repositori ini:**
   ```bash
   git clone [https://github.com/dapoull/SPK-Prediksi-Risiko-Kematian-Neonatal.git](https://github.com/dapoull/SPK-Prediksi-Risiko-Kematian-Neonatal.git)

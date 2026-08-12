# SPK-Prediksi-Risiko-Kematian-Neonatal
Latar Belakang & Masalah Utama

Kematian neonatal merupakan indikator krusial kualitas layanan kesehatan.

Tingginya risiko seperti Berat Badan Lahir Rendah (BBLR), Asfiksia, dan kelahiran prematur membutuhkan penanganan cepat dan akurat.

Adanya tantangan pengolahan data klinis yang memiliki missing values serta ketidakseimbangan kelas (imbalanced data).

Poin Utama Proyek & Metodologi

Pengolahan Data: Mengoptimalkan dataset 500 baris dengan menangani 307 missing values serta menerapkan SMOTE (Synthetic Minority Over-sampling Technique) untuk mengatasi imbalanced data, sehingga meningkatkan nilai Recall pada kelas minoritas (Died).

Pemodelan Machine Learning: Membangun algoritma Decision Tree dengan rasio data split 70:30 yang berhasil mencapai Akurasi 86.00%.

Faktor Dominan (Feature Importance): Mengidentifikasi 3 faktor risiko paling dominan terhadap kematian neonatal, yaitu:

Berat Badan Lahir (BBLR)

Kondisi Asfiksia

Usia Kehamilan (Prematuritas)

Implementasi: Menyediakan prototype Sistem Pendukung Keputusan interaktif berbasis Streamlit dan menyederhanakan aturan keputusan (if-then rules) dari tree untuk membantu pengambilan keputusan klinis dengan cepat.

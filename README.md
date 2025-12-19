# 🎮 Batu Gunting Kertas - 2 Pemain

Permainan Rock-Paper-Scissors untuk 2 pemain menggunakan Streamlit dan TensorFlow.

## 🌟 Fitur

- **2 Pemain**: Gameplay bergantian untuk Pemain 1 dan Pemain 2
- **Input Fleksibel**: Pilih antara kamera live atau upload foto
- **Model AI**: Menggunakan model Teachable Machine untuk mendeteksi gesture
- **Mode Demo**: Jika model tidak dapat dimuat, permainan tetap berfungsi dengan pemilihan manual
- **Skor Otomatis**: Pelacakan skor dan pengumuman pemenang otomatis
- **Antarmuka Indonesia**: Menggunakan bahasa Indonesia untuk label dan instruksi

## 📋 Persyaratan

- Python 3.8+
- Virtual environment yang sudah disiapkan

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
# Jika menggunakan venv yang sudah ada
python -m pip install -r requirements.txt

# Atau install ulang dependencies
python -m pip install streamlit tensorflow opencv-python numpy Pillow
```

### 2. Jalankan Aplikasi
```bash
streamlit run app.py
```

Atau menggunakan path Python spesifik:
```bash
/Users/usermac/Downloads/Rock-Paper-Scissors-Game-with-Teachable-Machine-streamlit/.venv/bin/python -m streamlit run app.py
```

### 3. Buka di Browser
Aplikasi akan otomatis terbuka di browser Anda pada `http://localhost:8501`

## 🎮 Cara Bermain

### Normal Mode (dengan AI)
1. **Pemain 1**:
   - Pilih metode input (Kamera atau Upload Foto)
   - Ambil foto atau upload gambar tangan Anda dengan gesture batu/gunting/kertas
   - Tunggu proses analisis AI
   - Konfirmasi pilihan

2. **Pemain 2**:
   - Lakukan hal yang sama seperti Pemain 1
   - Sistem akan secara otomatis menentukan pemenang

### Demo Mode (tanpa AI)
Jika model tidak dapat dimuat karena masalah kompatibilitas:
1. Pemain 1 memilih gesture secara manual (🗿 Batu, ✌️ Gunting, atau ✋ Kertas)
2. Pemain 2 memilih gesture secara manual
3. Sistem akan menentukan pemenang berdasarkan aturan standar

## 📜 Aturan Permainan

- 🗿 **Batu** menghancurkan Gunting ✌️
- ✌️ **Gunting** memotong Kertas ✋
- ✋ **Kertas** membungkus Batu 🗿

## 🛠️ Struktur File

```
/
├── app.py                 # Aplikasi Streamlit utama
├── utils.py               # Fungsi helper untuk model dan image processing
├── requirements.txt       # Dependencies Python
├── keras_model.h5        # Model TensorFlow yang sudah dilatih
├── labels.txt            # Label untuk gesture (Indonesia)
└── README.md             # File ini
```

## 🔧 Pemecahan Masalah

### Model tidak dapat dimuat
Jika muncul peringatan "Model tidak dapat dimuat", aplikasi akan otomatis beralih ke mode demo di mana Anda dapat memilih gesture secara manual.

### Kamera tidak berfungsi
- Pastikan browser Anda memiliki izin untuk mengakses kamera
- Coba gunakan browser yang berbeda (Chrome, Firefox, atau Safari)
- Atau gunakan opsi "Upload Foto" sebagai alternatif

### Hasil prediksi tidak akurat
- Pastikan pencahayaan cukup baik
- Tangan harus terlihat jelas dalam frame
- Latar belakang yang sederhana membantu proses deteksi
- Pastikan gesture dibuat dengan jelas (batu = kepal tangan, gunting = 2 jari, kertas = tangan terbuka)

## 📝 Catatan Teknis

- Aplikasi menggunakan TensorFlow/Keras untuk model machine learning
- Model dilatih dengan Teachable Machine dan labels dalam bahasa Indonesia
- Image processing menggunakan OpenCV dan Pillow
- Streamlit digunakan untuk interface web interaktif

## 🤝 Kontribusi

Ini adalah projek pembelajaran yang menggabungkan machine learning dengan game development. Silakan modifikasi dan sesuaikan sesuai kebutuhan Anda!

## 📄 Lisensi

Projek ini untuk tujuan pembelajaran dan pengembangan pribadi.
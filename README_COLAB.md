# 🎮 Batu Gunting Kertas - Google Colab Version

## 🌟 **Cara Mudah Main di Google Colab**

Ini adalah versi alternatif dari game Batu Gunting Kertas yang bisa dimainkan langsung di Google Colab tanpa instalasi apapun!

### 🚀 **Opsi 1: Jupyter Notebook (.ipynb)**
- Download file `batu_gunting_kertas_colab.ipynb`
- Upload ke Google Colab
- Klik "Runtime → Run all"

### 🚀 **Opsi 2: Python Script (.py) - Cara Termudah**
- Copy semua isi dari file `colab_version.py`
- Paste ke Google Colab cell
- Run cell tersebut
- Ketik `play_round()` untuk mulai bermain

---

## 📖 **Panduan Cepat Bermain**

### **Cara Memulai:**
1. Buka [Google Colab](https://colab.research.google.com/)
2. Buat notebook baru
3. Copy script dari `colab_version.py`
4. Paste dan Run
5. Ketik `play_round()` untuk mulai

### **Step-by-Step:**
```python
# 1. Paste script dan run (semua dependencies akan otomatis diinstall)

# 2. Mulai permainan
play_round()

# 3. Upload foto Pemain 1
# - Klik "Choose Files"
# - Pilih foto gesture (batu/gunting/kertas)

# 4. Upload foto Pemain 2
# - Lakukan hal yang sama untuk Pemain 2

# 5. Lihat hasil
# - AI akan otomatis mendeteksi gesture
# - Pemenang akan diumumkan

# 6. Main lagi?
# - Ketik play_round() lagi untuk ronde baru
```

---

## 🎯 **Petunjuk Gesture**

### **📸 Cara Pengambilan Foto:**
- **🗿 Batu**: Kepal tangan seperti tinju
- **✌️ Gunting**: 2 jari membentuk huruf V
- **✋ Kertas**: Tangan terbuka rata

### **💡 Tips untuk Hasil Terbaik:**
- ✅ Pencahayaan cukup terang
- ✅ Tangan terlihat jelas, tidak blur
- ✅ Background sederhana (tidak terlalu ramai)
- ✅ Gesture dibuat dengan jelas
- ✅ Jarak foto tidak terlalu jauh/dekat

---

## 🏆 **Aturan Permainan**

### **Classic Rock-Paper-Scissors:**
- 🗿 **Batu** menghancurkan ✌️ **Gunting**
- ✌️ **Gunting** memotong ✋ **Kertas**
- ✋ **Kertas** membungkus 🗿 **Batu**

### **Skoring:**
- ✅ Pemain yang menang dapat 1 poin
- 🤝 Seri tidak ada poin
- 📊 Skor terakumulasi untuk setiap ronde

---

## 🤖 **Teknologi AI**

### **Cara Kerja Detection:**
1. **Image Processing**: Foto di-preprocess dengan OpenCV
2. **Feature Extraction**: Analisis kontur dan bentuk
3. **Classification**: Klasifikasi berdasarkan fitur visual
4. **Confidence Score**: AI memberikan confidence percentage

### **AI Features:**
- ✅ **Automatic gesture detection**
- ✅ **Confidence scoring** (0-100%)
- ✅ **Error handling** dan fallback
- ✅ **Fast processing** (detik)

---

## 📱 **Keuntungan Google Colab Version**

### **🎯 No Installation Required:**
- Tidak perlu install Python, TensorFlow, dll
- Buka browser langsung bisa main

### **🌍 Any Device:**
- Bisa di HP, tablet, laptop
- Tidak perlu download file besar
- Google storage untuk upload foto

### **🔄 Easy to Share:**
- Share link ke audience
- Collaborative playing
- Real-time demonstration

### **💡 Educational:**
- Perfect untuk workshop/presentasi
- Live coding demo
- Interactive learning

---

## 📋 **Kode untuk Presentasi**

### **Quick Copy-Paste:**
```python
# Copy ini ke Google Colab cell:
!pip install tensorflow opencv-python numpy pillow matplotlib -q
# (Paste sisa kode dari colab_version.py)
```

### **Cara Presentasi:**
1. Buka Google Colab
2. Copy paste script
3. Run sekali untuk install dependencies
4. Jalankan `play_round()` untuk demo
5. Upload contoh foto gesture
6. Tunjukkan hasil AI detection

---

## 🔧 **Troubleshooting**

### **Common Issues:**
- **Upload gagal**: Refresh browser, coba lagi
- **AI salah deteksi**: Coba foto dengan pencahayaan lebih baik
- **Error**: Run ulang cell dari awal
- **Loading lama**: Tunggu proses install dependencies

### **Performance Tips:**
- Gunakan GPU di Colab (Runtime → Change runtime type → GPU)
- Foto size tidak terlalu besar (< 5MB)
- Pastikan koneksi internet stabil

---

## 🎮 **Summary**

### **📁 Files yang Dibutuhkan:**
- ✅ `batu_gunting_kertas_colab.ipynb` - Full notebook version
- ✅ `colab_version.py` - Simple copy-paste script
- ✅ `README_COLAB.md` - This documentation

### **🚀 Cara Paling Mudah:**
1. Buka Google Colab
2. Copy script dari `colab_version.py`
3. Paste dan Run
4. Ketik `play_round()` → Start playing!

### **🎯 Perfect Untuk:**
- **Presentasi & Workshop**
- **Demo AI/ML**
- **Interactive Learning**
- **Quick Testing**
- **Mobile Gaming**

---

## 🏆 **Get Started Now!**

### **🔗 Langsung Main:**
1. [Buka Google Colab](https://colab.research.google.com/)
2. Copy script dari `colab_version.py`
3. Run → `play_round()` → Start!

### **🎮 Selamat Bermain di Google Colab!**

**Created with ❤️ for easy AI Gaming!**

**Framework**: TensorFlow + OpenCV + Google Colab
**Perfect for**: Workshops, Demos, Quick Testing
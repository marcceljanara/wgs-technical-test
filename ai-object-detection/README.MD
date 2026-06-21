# 🍎 YOLO Fruit Detection (AI Object Classification)

Proyek ini adalah implementasi end-to-end dari sistem Kecerdasan Buatan (AI) berbasis **YOLOv8** untuk mengklasifikasikan 9 jenis buah secara otomatis. 

Pipeline proyek ini mencakup keseluruhan proses machine learning: mulai dari pembersihan dan restrukturisasi data, pelatihan model (training), hingga inferensi (prediksi) dengan antarmuka visual menggunakan OpenCV.

## 📁 Struktur Direktori

```text
ai-object-detection/
├── datasets/                 # Folder dataset utama
│   ├── train/                # Data latih (dibagi per subfolder kelas)
│   ├── val/                  # Data validasi
│   └── test/                 # Data uji untuk inferensi
├── runs/                     # Direktori otomatis tempat Ultralytics menyimpan log & metrik
├── best.pt                   # Model terbaik hasil training (muncul setelah train.py)
├── prepare_dataset.py        # Script Tahap 1: Restrukturisasi dataset
├── train.py                  # Script Tahap 2: Training & Evaluasi model
├── inference.py              # Script Tahap 3: Prediksi gambar dengan UI Pop-up
├── requirements.txt          # Daftar dependensi Python
└── AI-OBJECT-DETECTION.MD    # Dokumentasi ini
```

## ⚙️ Prasyarat & Instalasi

Sebelum menjalankan pipeline, pastikan Anda telah menginstal dependensi yang dibutuhkan. Proyek ini membutuhkan Python 3.8+ (disarankan Python 3.11).

1. Buka terminal/Command Prompt dan arahkan ke folder proyek ini:
   ```bash
   cd path/to/ai-object-detection
   ```
2. Instal semua pustaka yang diperlukan melalui `pip`:
   ```bash
   pip install -r requirements.txt
   ```
   > **Catatan:** Secara default, ini akan menginstal PyTorch versi CPU. Jika Anda memiliki GPU NVIDIA dan ingin mempercepat proses training, disarankan menginstal PyTorch versi CUDA (misal: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121` atau sesuai versi CUDA perangkat Anda).

---

## 🚀 Pipeline Penggunaan (Cara Menjalankan)

Proyek ini dirancang agar dapat dijalankan secara berurutan. Ikuti langkah 1 hingga 3 di bawah ini:

### Tahap 1: Persiapan Dataset (`prepare_dataset.py`)
Dataset mentah (gambar gabungan yang didasarkan pada file CSV anotasi) perlu direstrukturisasi agar sesuai dengan standar format direktori klasifikasi Ultralytics YOLO (yaitu gambar dipisah ke dalam subfolder berdasarkan nama kelas/labelnya).

**Perintah:**
```bash
python prepare_dataset.py
```
**Yang dilakukan script ini:**
- Membaca file `_classes.csv` untuk mencocokkan setiap gambar dengan label buahnya.
- Membuat struktur folder `datasets/train/<NamaBuah>`, `datasets/val/<NamaBuah>`, dan `datasets/test/<NamaBuah>`.
- Memindahkan/menyalin gambar ke folder yang sesuai secara otomatis dan membersihkan nama file dari spasi (sanitisasi).

---

### Tahap 2: Pelatihan Model (`train.py`)
Setelah dataset tersusun rapi, tahap selanjutnya adalah melatih model AI agar dapat mempelajari dan mengenali pola visual dari masing-masing buah.

**Perintah:**
```bash
python train.py
```
**Yang dilakukan script ini:**
- Memvalidasi integritas struktur dataset.
- Mengunduh model arsitektur dasar `yolov8n-cls.pt` (jika belum ada).
- Melatih model selama beberapa epoch (default: 10 epoch).
- Mengevaluasi akurasi model (Top-1 dan Top-5 accuracy) pada test set.
- **Menyimpan model terbaik** sebagai `best.pt` di root direktori agar siap dipakai.
- Metrik tambahan seperti grafik *confusion matrix*, kurva *loss*, dan *accuracy* akan tersimpan secara otomatis di dalam folder `runs/classify/fruits-cls/`.

---

### Tahap 3: Inferensi & Visualisasi (`inference.py`)
Gunakan model yang telah dilatih (`best.pt`) untuk memprediksi gambar-gambar buah (dari folder `test/` atau file eksternal).

**Perintah:**
```bash
python inference.py
```
**Yang dilakukan script ini:**
- Membaca file model `best.pt`.
- Memuat gambar-gambar secara berurutan dari folder `datasets/test`.
- Melakukan inferensi menggunakan YOLOv8.
- Membuka **pop-up window UI (menggunakan OpenCV)** yang menampilkan:
  - Header: Nama buah prediksi utama dan skor keyakinan (*confidence score*) tertinggi.
  - Border warna khusus yang berbeda untuk setiap jenis buah.
  - Footer: Daftar *Top-3 predictions* beserta progress bar persentase tebakannya.
- **Kontrol UI Navigasi:**
  - Tekan **Sembarang Tombol (Any Key)** di keyboard untuk beralih ke gambar selanjutnya.
  - Tekan **'Q'** atau tombol **ESC** untuk keluar dari program.

---

## 💡 Troubleshooting / Masalah Umum

1. **Error: Model tidak ditemukan saat menjalankan inference.py**
   - Pastikan Anda telah menjalankan `python train.py` sampai selesai.
   - Pastikan file `best.pt` sudah terbentuk dan berada di root folder proyek ini.

2. **Error: Out of Memory (OOM) saat training**
   - Buka file `train.py`, cari variabel `BATCH_SIZE = 16`, lalu turunkan nilainya menjadi `8` atau `4`.

3. **Proses Training Terasa Sangat Lambat**
   - Ini wajar terjadi jika training berjalan menggunakan CPU. Untuk performa yang jauh lebih cepat (bisa 10-20x lipat), jalankan proses ini menggunakan GPU dengan cara menginstal driver CUDA dan PyTorch versi CUDA.

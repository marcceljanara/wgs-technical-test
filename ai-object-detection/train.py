"""
============================================================
train.py — YOLO Fruit Classification Training Script
============================================================
Fruit Detection Project | Fruits by YOLO (Roboflow)

DESKRIPSI:
    Script pelatihan model deteksi/klasifikasi buah menggunakan
    Ultralytics YOLOv8. Model akan dilatih menggunakan dataset
    yang telah direstrukturisasi oleh prepare_dataset.py.

PRASYARAT:
    1. Jalankan prepare_dataset.py terlebih dahulu
    2. Pastikan folder datasets/ sudah berisi gambar per-kelas
    3. Install requirements: pip install -r requirements.txt

CARA MENJALANKAN:
    python train.py

OUTPUT:
    - runs/classify/fruits-cls/weights/best.pt  ← Model terbaik
    - runs/classify/fruits-cls/weights/last.pt  ← Model terakhir
    - runs/classify/fruits-cls/results.csv       ← Metrik training

ARSITEKTUR:
    - Base model : YOLOv8n-cls (Nano Classification)
    - Framework  : Ultralytics (PyTorch backend)
    - Task       : Image Classification (9 kelas buah)
"""

import os
import sys
import shutil
import logging
from pathlib import Path

# ── Dependency imports dengan graceful error handling ──────────
try:
    import torch
    _TORCH_AVAILABLE = True
except ImportError:
    _TORCH_AVAILABLE = False

try:
    from ultralytics import YOLO
    _ULTRALYTICS_AVAILABLE = True
except Exception as _e:
    _ULTRALYTICS_AVAILABLE = False
    _ULTRALYTICS_ERROR = str(_e)

# ============================================================
# KONFIGURASI TRAINING — Edit sesuai kebutuhan Anda
# ============================================================

# Path ke dataset yang sudah direstrukturisasi (output dari prepare_dataset.py)
DATASET_PATH = "./datasets"

# Pretrained model base (akan didownload otomatis jika belum ada)
# Pilihan: yolov8n-cls.pt (nano/cepat), yolov8s-cls.pt, yolov8m-cls.pt
BASE_MODEL = "yolov8n-cls.pt"

# Hyperparameter Training
EPOCHS       = 50      # Jumlah epoch maksimum
IMAGE_SIZE   = 224     # Ukuran input gambar (standar untuk klasifikasi)
BATCH_SIZE   = 16      # Batch size (turunkan ke 8 jika GPU VRAM < 4GB)
PATIENCE     = 15      # Epoch tanpa peningkatan sebelum early stop
LEARNING_RATE = 0.01   # Learning rate awal
SAVE_PERIOD  = 10      # Simpan checkpoint setiap N epoch
PROJECT_NAME = "runs/classify"
RUN_NAME     = "fruits-cls"

# Gunakan GPU jika tersedia, fallback ke CPU
DEVICE = "0" if (_TORCH_AVAILABLE and torch.cuda.is_available()) else "cpu"

# Path output best.pt yang akan disalin ke root project
BEST_PT_SOURCE = Path(f"{PROJECT_NAME}/{RUN_NAME}/weights/best.pt")
BEST_PT_DEST   = Path("./best.pt")

# ============================================================
# SETUP LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("training.log", encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)


# ============================================================
# VALIDASI PRE-TRAINING
# ============================================================

def validate_environment() -> bool:
    """
    Validasi bahwa semua prasyarat terpenuhi sebelum training dimulai.

    Returns:
        True jika semua OK, False jika ada masalah
    """
    log.info("Memvalidasi environment training...")

    # Cek dataset
    dataset_path = Path(DATASET_PATH)
    if not dataset_path.exists():
        log.error(
            f"Dataset tidak ditemukan di: {dataset_path.resolve()}\n"
            "Jalankan 'python prepare_dataset.py' terlebih dahulu!"
        )
        return False

    # Cek subfolder train, val, test
    for split in ["train", "val", "test"]:
        split_path = dataset_path / split
        if not split_path.exists():
            log.error(f"Folder split tidak ditemukan: {split_path}")
            return False

        # Pastikan ada minimal 1 subfolder kelas
        subfolders = [d for d in split_path.iterdir() if d.is_dir()]
        if not subfolders:
            log.error(f"Tidak ada subfolder kelas di: {split_path}")
            return False

    log.info(f"✅ Dataset valid: {dataset_path.resolve()}")
    log.info(f"✅ Device      : {DEVICE} ({'GPU' if DEVICE != 'cpu' else 'CPU'})")
    log.info(f"✅ Base model  : {BASE_MODEL}")
    log.info(f"✅ Epochs      : {EPOCHS} (max), patience={PATIENCE}")
    log.info(f"✅ Batch size  : {BATCH_SIZE}")
    return True


# ============================================================
# TRAINING
# ============================================================

def run_training():
    """
    Jalankan proses training YOLOv8 Classification.
    """
    if not _ULTRALYTICS_AVAILABLE:
        log.error(
            f"Ultralytics tidak dapat diload: {_ULTRALYTICS_ERROR}\n"
            "Coba: pip install 'numpy<2.0' && pip install --upgrade matplotlib ultralytics"
        )
        sys.exit(1)

    log.info("\n" + "="*60)
    log.info("MEMULAI TRAINING — YOLOv8 Fruit Classification")
    log.info("="*60)

    # Load pretrained model
    # yolov8n-cls.pt akan didownload otomatis dari Ultralytics jika belum ada
    log.info(f"Loading pretrained model: {BASE_MODEL}")
    model = YOLO(BASE_MODEL)

    # Mulai training
    log.info("Training dimulai...\n")
    try:
        results = model.train(
            data=DATASET_PATH,          # Path ke folder dataset
            epochs=EPOCHS,              # Jumlah epoch maksimum
            imgsz=IMAGE_SIZE,           # Ukuran gambar input
            batch=BATCH_SIZE,           # Batch size
            patience=PATIENCE,          # Early stopping patience
            lr0=LEARNING_RATE,          # Learning rate awal
            save=True,                  # Simpan checkpoint
            save_period=SAVE_PERIOD,    # Simpan setiap N epoch
            project=PROJECT_NAME,       # Folder output utama
            name=RUN_NAME,              # Nama subfolder run
            device=DEVICE,              # GPU (0) atau CPU
            verbose=True,               # Tampilkan log detail
            exist_ok=True,              # Overwrite run yang ada
            pretrained=True,            # Gunakan pretrained weights
            optimizer="auto",           # Pilih optimizer otomatis
            seed=42,                    # Reproducibility
            workers=4,                  # Jumlah worker DataLoader
        )

        log.info("\n" + "="*60)
        log.info("✅ TRAINING SELESAI!")
        log.info("="*60)
        return results

    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            log.error(
                f"GPU kehabisan VRAM!\n"
                f"Coba turunkan BATCH_SIZE dari {BATCH_SIZE} ke {BATCH_SIZE // 2}\n"
                f"Error: {e}"
            )
        else:
            log.error(f"Runtime error saat training: {e}")
        sys.exit(1)


# ============================================================
# EVALUASI POST-TRAINING
# ============================================================

def run_evaluation():
    """
    Evaluasi model hasil training pada test set dan cetak metrik.
    """
    if not _ULTRALYTICS_AVAILABLE:
        return

    if not BEST_PT_SOURCE.exists():
        log.warning(f"best.pt tidak ditemukan di: {BEST_PT_SOURCE}")
        return

    log.info("\n" + "="*60)
    log.info("EVALUASI MODEL PADA TEST SET")
    log.info("="*60)

    model = YOLO(str(BEST_PT_SOURCE))

    try:
        metrics = model.val(
            data=DATASET_PATH,
            split="test",
            imgsz=IMAGE_SIZE,
            batch=BATCH_SIZE,
            device=DEVICE,
        )

        log.info("\n📊 HASIL EVALUASI TEST SET:")
        log.info(f"   Top-1 Accuracy : {metrics.top1:.4f} ({metrics.top1 * 100:.2f}%)")
        log.info(f"   Top-5 Accuracy : {metrics.top5:.4f} ({metrics.top5 * 100:.2f}%)")

        # Target threshold
        if metrics.top1 >= 0.85:
            log.info("   ✅ Target Top-1 ≥ 85% TERCAPAI!")
        else:
            log.warning(
                f"   ⚠️ Top-1 {metrics.top1 * 100:.2f}% belum mencapai target 85%.\n"
                "   Pertimbangkan menambah epoch atau menggunakan model yang lebih besar."
            )

    except Exception as e:
        log.error(f"Error saat evaluasi: {e}")


# ============================================================
# SALIN BEST.PT KE ROOT PROJECT
# ============================================================

def copy_best_weights():
    """
    Salin best.pt dari folder runs/ ke root direktori project
    agar mudah ditemukan sebagai deliverable.
    """
    if BEST_PT_SOURCE.exists():
        shutil.copy2(BEST_PT_SOURCE, BEST_PT_DEST)
        size_mb = BEST_PT_DEST.stat().st_size / (1024 * 1024)
        log.info(f"\n✅ best.pt disalin ke: {BEST_PT_DEST.resolve()}")
        log.info(f"   Ukuran file: {size_mb:.2f} MB")
    else:
        log.warning(f"best.pt tidak ditemukan di: {BEST_PT_SOURCE}")


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    log.info("=" * 60)
    log.info("YOLO Fruit Detection — Training Script")
    log.info("=" * 60)

    # Validasi environment
    if not validate_environment():
        sys.exit(1)

    # Jalankan training
    run_training()

    # Evaluasi pada test set
    run_evaluation()

    # Salin best.pt ke root project
    copy_best_weights()

    log.info("\n" + "="*60)
    log.info("🎉 PIPELINE TRAINING SELESAI!")
    log.info("="*60)
    log.info(f"   Model terbaik : {BEST_PT_DEST.resolve()}")
    log.info(f"   Training log  : {Path('training.log').resolve()}")
    log.info(f"   Hasil run     : {Path(PROJECT_NAME, RUN_NAME).resolve()}")
    log.info("\nLangkah berikutnya: jalankan python inference.py")


if __name__ == "__main__":
    main()

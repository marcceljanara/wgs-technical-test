"""
============================================================
prepare_dataset.py — Dataset Preparation for YOLO Classification
============================================================
Fruit Detection Project | Fruits by YOLO (Roboflow)

DESKRIPSI:
    Script ini merestrukturisasi dataset dari format Roboflow classification
    export (flat images + _classes.csv) ke format subfolder per-kelas yang
    dibutuhkan oleh Ultralytics YOLO Classification.

STRUKTUR INPUT (dari Roboflow):
    Fruits-by-YOLO/Fruits by YOLO/
    ├── train/  → *.jpg + _classes.csv
    ├── valid/  → *.jpg + _classes.csv
    └── test/   → *.jpg + _classes.csv

STRUKTUR OUTPUT (untuk YOLO Classification):
    datasets/
    ├── train/
    │   ├── Apple/   ├── Banana/   ├── Grapes/   ├── Kiwi/
    │   ├── Mango/   ├── Orange/   ├── Pineapple/
    │   ├── Sugerapple/            └── Watermelon/
    ├── val/    (sama seperti train)
    └── test/   (sama seperti train)

CARA MENJALANKAN:
    python prepare_dataset.py

CATATAN:
    - Gambar dengan multiple labels → kelas pertama yang ditemukan dipilih
    - Gambar corrupt atau tidak valid akan di-skip dan di-log
    - Script ini aman dijalankan berulang kali (overwrite-safe)
"""

import os
import csv
import shutil
import logging
from pathlib import Path

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("[WARN] Pillow tidak tersedia. Validasi gambar dinonaktifkan.")

# ============================================================
# KONFIGURASI PATH — Edit sesuai lokasi dataset Anda
# ============================================================

# Path ke folder raw dataset Roboflow
DATASET_ROOT = Path("./Fruits-by-YOLO/Fruits by YOLO")

# Path output dataset yang sudah direstrukturisasi
OUTPUT_ROOT = Path("./datasets")

# Nama split (key = nama folder input, value = nama folder output)
SPLITS = {
    "train": "train",
    "valid": "val",   # YOLO convention menggunakan 'val' bukan 'valid'
    "test":  "test",
}

# 9 kelas buah sesuai data.yaml
FRUIT_CLASSES = [
    "Apple", "Banana", "Grapes", "Kiwi", "Mango",
    "Orange", "Pineapple", "Sugerapple", "Watermelon"
]

# ============================================================
# SETUP LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("prepare_dataset.log", encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)


# ============================================================
# FUNGSI UTAMA
# ============================================================

def validate_image(image_path: Path) -> bool:
    """
    Validasi apakah file gambar dapat dibaca dengan benar.

    Args:
        image_path: Path ke file gambar

    Returns:
        True jika gambar valid, False jika corrupt
    """
    if not PIL_AVAILABLE:
        return True  # Skip validation jika Pillow tidak tersedia

    try:
        with Image.open(image_path) as img:
            img.verify()  # Cek apakah file tidak corrupt
        return True
    except Exception as e:
        log.warning(f"Gambar corrupt, skip: {image_path.name} — {e}")
        return False


def parse_classes_csv(csv_path: Path) -> dict:
    """
    Parse file _classes.csv dan kembalikan mapping filename → nama kelas.

    Format CSV:
        filename, Apple, Banana, Grapes, Kiwi, Mango, Orange, Pineapple, Sugerapple, Watermelon
        image.jpg, 0, 0, 0, 1, 0, 0, 0, 0, 0

    Args:
        csv_path: Path ke file _classes.csv

    Returns:
        dict: { "image.jpg": "Kiwi", ... }
    """
    label_map = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # Bersihkan nama kolom dari spasi ekstra
        reader.fieldnames = [col.strip() for col in reader.fieldnames]

        for row in reader:
            filename = row["filename"].strip()

            # Temukan kelas dengan nilai '1' (single-label)
            # Jika multi-label, ambil kelas pertama yang ditemukan
            assigned_class = None
            for fruit_class in FRUIT_CLASSES:
                if fruit_class in row and row[fruit_class].strip() == "1":
                    assigned_class = fruit_class
                    break  # Ambil label pertama untuk multi-label images

            if assigned_class:
                label_map[filename] = assigned_class
            else:
                log.warning(f"Tidak ada label ditemukan untuk: {filename}")

    return label_map


def create_output_structure() -> None:
    """Buat semua folder output yang diperlukan."""
    for split_out in SPLITS.values():
        for fruit_class in FRUIT_CLASSES:
            folder = OUTPUT_ROOT / split_out / fruit_class
            folder.mkdir(parents=True, exist_ok=True)
    log.info(f"Struktur folder output berhasil dibuat di: {OUTPUT_ROOT.resolve()}")


def copy_images_to_class_folders(
    split_in: str,
    split_out: str
) -> tuple[int, int, int]:
    """
    Salin gambar dari folder split mentah ke folder kelas output.

    Args:
        split_in:  Nama folder input  (misal: 'train', 'valid', 'test')
        split_out: Nama folder output (misal: 'train', 'val',   'test')

    Returns:
        tuple: (total_processed, total_copied, total_skipped)
    """
    source_dir = DATASET_ROOT / split_in
    csv_path   = source_dir / "_classes.csv"

    if not source_dir.exists():
        log.error(f"Folder split tidak ditemukan: {source_dir}")
        return 0, 0, 0

    if not csv_path.exists():
        log.error(f"File _classes.csv tidak ditemukan: {csv_path}")
        return 0, 0, 0

    log.info(f"\n{'='*50}")
    log.info(f"Memproses split: '{split_in}' → '{split_out}'")
    log.info(f"{'='*50}")

    # Parse label dari CSV
    label_map = parse_classes_csv(csv_path)
    log.info(f"Total gambar terlabeli di CSV: {len(label_map)}")

    copied  = 0
    skipped = 0

    for img_filename, fruit_class in label_map.items():
        src_path = source_dir / img_filename

        # Pastikan file gambar ada
        if not src_path.exists():
            log.warning(f"File tidak ditemukan, skip: {img_filename}")
            skipped += 1
            continue

        # Validasi integritas gambar
        if not validate_image(src_path):
            skipped += 1
            continue

        # Tentukan path tujuan
        dst_path = OUTPUT_ROOT / split_out / fruit_class / img_filename

        # Salin gambar ke folder kelas
        shutil.copy2(src_path, dst_path)
        copied += 1

    log.info(f"Selesai '{split_in}': {copied} disalin, {skipped} di-skip")
    return len(label_map), copied, skipped


def print_distribution_report() -> None:
    """Cetak laporan distribusi gambar per kelas di setiap split."""
    log.info("\n" + "="*60)
    log.info("LAPORAN DISTRIBUSI DATASET")
    log.info("="*60)

    total_all = 0
    for split_out in SPLITS.values():
        log.info(f"\n  Split: {split_out}/")
        split_total = 0
        for fruit_class in FRUIT_CLASSES:
            folder = OUTPUT_ROOT / split_out / fruit_class
            count = len(list(folder.glob("*.jpg")))
            split_total += count
            log.info(f"    {fruit_class:<15}: {count:>5} gambar")
        log.info(f"    {'TOTAL':<15}: {split_total:>5} gambar")
        total_all += split_total

    log.info(f"\n  GRAND TOTAL: {total_all} gambar")
    log.info("="*60)


def update_data_yaml() -> None:
    """Update data.yaml dengan path yang sesuai untuk YOLO Classification."""
    yaml_content = f"""# ============================================================
# data.yaml — Konfigurasi Dataset YOLO Classification
# ============================================================
# Dataset: Fruits by YOLO (Roboflow)
# Format : YOLO Classification (subfolder per kelas)

path: ./datasets   # Root directory dataset (relatif terhadap ai-object-detection/)
train: train       # Subfolder training
val: val           # Subfolder validasi
test: test         # Subfolder testing

# Jumlah kelas
nc: {len(FRUIT_CLASSES)}

# Nama kelas (urutan harus sesuai dengan index)
names: {FRUIT_CLASSES}

# Metadata Roboflow
roboflow:
  workspace: fruitsdetection
  project: fruits-by-yolo
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/fruitsdetection/fruits-by-yolo/dataset/1
"""

    yaml_path = Path("./data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)
    log.info(f"\ndata.yaml berhasil diperbarui: {yaml_path.resolve()}")


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    log.info("=" * 60)
    log.info("YOLO Fruit Detection — Dataset Preparation Script")
    log.info("=" * 60)

    # Validasi keberadaan dataset sumber
    if not DATASET_ROOT.exists():
        log.error(
            f"Dataset sumber tidak ditemukan: {DATASET_ROOT.resolve()}\n"
            "Pastikan folder 'Fruits-by-YOLO' ada di direktori yang sama "
            "dengan script ini (ai-object-detection/)."
        )
        return

    # Buat struktur folder output
    create_output_structure()

    # Proses setiap split
    grand_total   = 0
    grand_copied  = 0
    grand_skipped = 0

    for split_in, split_out in SPLITS.items():
        total, copied, skipped = copy_images_to_class_folders(split_in, split_out)
        grand_total   += total
        grand_copied  += copied
        grand_skipped += skipped

    # Laporan distribusi
    print_distribution_report()

    # Update data.yaml
    update_data_yaml()

    log.info("\n✅ Persiapan dataset selesai!")
    log.info(f"   Total diproses : {grand_total}")
    log.info(f"   Total disalin  : {grand_copied}")
    log.info(f"   Total di-skip  : {grand_skipped}")
    log.info(f"\nDataset siap di: {OUTPUT_ROOT.resolve()}")
    log.info("Langkah berikutnya: jalankan python train.py")


if __name__ == "__main__":
    main()

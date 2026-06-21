"""
============================================================
inference.py — YOLO Fruit Detection Inference Script
============================================================
Fruit Detection Project | Fruits by YOLO (Roboflow)

DESKRIPSI:
    Script inference untuk mendeteksi dan mengklasifikasikan gambar buah
    menggunakan model hasil training. Menampilkan hasil deteksi dalam
    pop-up window OpenCV dengan anotasi visual lengkap.

FITUR:
    ✅ Path gambar ditentukan langsung di script (TIDAK perlu input terminal)
    ✅ Pop-up window otomatis saat dijalankan (OpenCV cv2.imshow)
    ✅ Anotasi visual: label kelas + confidence score + color coding
    ✅ Top-3 predictions ditampilkan sebagai overlay
    ✅ Navigasi gambar: any key = lanjut, 'q'/'ESC' = keluar

PRASYARAT:
    1. Jalankan prepare_dataset.py → datasets/
    2. Jalankan train.py → best.pt (atau gunakan best.pt yang sudah ada)
    3. Install requirements: pip install -r requirements.txt

CARA MENJALANKAN:
    python inference.py

KONTROL WINDOW:
    - Tekan sembarang tombol → gambar berikutnya
    - Tekan 'q' atau ESC     → keluar dari program
"""

import os
import sys
import glob
import logging
from pathlib import Path

import cv2
import numpy as np

# ── Ultralytics YOLO ─────────────────────────────────────────
try:
    from ultralytics import YOLO
    _ULTRALYTICS_AVAILABLE = True
except Exception as _e:
    _ULTRALYTICS_AVAILABLE = False
    _ULTRALYTICS_ERROR = str(_e)

# ============================================================
# KONFIGURASI — PATH DITENTUKAN DI SINI (TIDAK DARI TERMINAL)
# ============================================================

# ⚠️ ATURAN WAJIB: Path gambar HARUS hardcoded di dalam script ini
# Ganti dengan path folder atau file gambar yang ingin dideteksi

# Opsi 1: Deteksi semua gambar di folder test set
IMAGE_SOURCE = "./datasets/test"

# Opsi 2: Deteksi satu gambar spesifik (uncomment untuk menggunakan)
# IMAGE_SOURCE = "./datasets/test/Apple/Image_1_jpg.rf.64c9a3a9b8ce63a44eb223c4d82302f0.jpg"

# Path model yang sudah dilatih
MODEL_PATH = "./best.pt"

# Fallback jika best.pt belum ada di root (cari di folder runs/)
MODEL_PATH_FALLBACK = "./runs/classify/fruits-cls/weights/best.pt"

# Ukuran gambar untuk inferensi (harus sama dengan saat training)
IMAGE_SIZE = 224

# Tampilkan gambar dengan ukuran window yang ditentukan
DISPLAY_WIDTH  = 800   # Lebar window tampilan (pixel)
DISPLAY_HEIGHT = 650   # Tinggi window tampilan (pixel)

# Jumlah top-N predictions yang ditampilkan
TOP_N = 3

# Waktu delay antar gambar jika dijalankan dalam mode slideshow
# 0 = tunggu tombol ditekan, >0 = auto-advance setelah N ms
WAIT_MS = 0

# ============================================================
# KONFIGURASI WARNA PER KELAS (Format BGR untuk OpenCV)
# ============================================================

CLASS_COLORS = {
    "Apple":      (0,   0,   220),   # Merah
    "Banana":     (0,   215, 255),   # Kuning
    "Grapes":     (180, 30,  120),   # Ungu
    "Kiwi":       (0,   180, 30),    # Hijau
    "Mango":      (0,   145, 255),   # Oranye
    "Orange":     (0,   165, 255),   # Oranye terang
    "Pineapple":  (0,   230, 230),   # Kuning muda
    "Sugerapple": (80,  200, 80),    # Hijau muda
    "Watermelon": (30,  120, 10),    # Hijau tua
}

# Warna default jika kelas tidak dikenali
DEFAULT_COLOR = (200, 200, 200)

# ============================================================
# SETUP LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger(__name__)


# ============================================================
# FUNGSI UTILITAS
# ============================================================

def find_model() -> str:
    """
    Cari file model best.pt. Coba path utama, lalu fallback.

    Returns:
        Path ke model yang ditemukan.

    Raises:
        FileNotFoundError: Jika model tidak ditemukan di keduanya.
    """
    if Path(MODEL_PATH).exists():
        log.info(f"Model ditemukan: {Path(MODEL_PATH).resolve()}")
        return MODEL_PATH

    if Path(MODEL_PATH_FALLBACK).exists():
        log.info(f"Model ditemukan (fallback): {Path(MODEL_PATH_FALLBACK).resolve()}")
        return MODEL_PATH_FALLBACK

    raise FileNotFoundError(
        f"Model tidak ditemukan!\n"
        f"Coba cari di:\n"
        f"  1. {Path(MODEL_PATH).resolve()}\n"
        f"  2. {Path(MODEL_PATH_FALLBACK).resolve()}\n"
        f"Jalankan 'python train.py' terlebih dahulu."
    )


def collect_image_paths(source: str) -> list[Path]:
    """
    Kumpulkan daftar path gambar dari folder atau file tunggal.

    Args:
        source: Path ke folder atau file gambar

    Returns:
        List of Path objects untuk setiap gambar
    """
    source_path = Path(source)

    if source_path.is_file():
        # Mode file tunggal
        if source_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp"]:
            return [source_path]
        else:
            log.error(f"File bukan gambar yang didukung: {source_path}")
            return []

    elif source_path.is_dir():
        # Mode folder — kumpulkan semua gambar secara rekursif
        extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.JPG", "*.JPEG"]
        image_files = []
        for ext in extensions:
            image_files.extend(source_path.rglob(ext))

        image_files.sort()
        log.info(f"Ditemukan {len(image_files)} gambar di: {source_path.resolve()}")
        return image_files

    else:
        log.error(f"Path tidak valid: {source_path}")
        return []


def get_class_color(class_name: str) -> tuple:
    """Kembalikan warna BGR untuk kelas tertentu."""
    return CLASS_COLORS.get(class_name, DEFAULT_COLOR)


# ============================================================
# FUNGSI ANOTASI VISUAL
# ============================================================

def create_annotated_frame(
    original_image: np.ndarray,
    predictions: list[tuple[str, float]],
    image_path: Path,
    current_idx: int,
    total_images: int,
) -> np.ndarray:
    """
    Buat frame gambar dengan anotasi visual lengkap.

    Layout:
    ┌──────────────────────────────────────────────────────┐
    │  HEADER: Nama kelas + confidence terbaik             │
    ├──────────────────────────────────────────────────────┤
    │                                                      │
    │                  [Gambar Buah]                       │
    │                                                      │
    ├──────────────────────────────────────────────────────┤
    │  FOOTER: Top-3 predictions + navigasi info           │
    └──────────────────────────────────────────────────────┘

    Args:
        original_image: Gambar asli (numpy array BGR)
        predictions:    List of (class_name, confidence) tuples, sorted desc
        image_path:     Path file gambar
        current_idx:    Indeks gambar saat ini (1-based)
        total_images:   Total gambar yang diproses

    Returns:
        Frame yang sudah dianotasi
    """
    # --- Resize gambar untuk tampilan ---
    img_h, img_w = original_image.shape[:2]
    available_h = DISPLAY_HEIGHT - 100 - (TOP_N + 1) * 30  # dikurangi header & footer
    scale = min(DISPLAY_WIDTH / img_w, available_h / img_h, 1.0)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    resized = cv2.resize(original_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # --- Buat canvas hitam sebagai background ---
    canvas = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH, 3), dtype=np.uint8)
    canvas[:] = (20, 20, 30)  # Warna latar gelap (dark navy)

    # --- Ambil prediksi terbaik ---
    top_class, top_conf = predictions[0] if predictions else ("Unknown", 0.0)
    top_color = get_class_color(top_class)

    # ═══════════════════════════════════════════════════════
    # HEADER BAR
    # ═══════════════════════════════════════════════════════
    header_h = 70
    cv2.rectangle(canvas, (0, 0), (DISPLAY_WIDTH, header_h), (40, 40, 55), -1)
    cv2.rectangle(canvas, (0, 0), (DISPLAY_WIDTH, header_h), top_color, 2)

    # Label kelas utama (besar)
    label_text = f"{top_class}"
    conf_text  = f"{top_conf * 100:.1f}%"

    cv2.putText(
        canvas, label_text,
        (15, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.2, top_color, 2, cv2.LINE_AA
    )
    # Confidence di sebelah kanan
    (conf_w, _), _ = cv2.getTextSize(conf_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
    cv2.putText(
        canvas, conf_text,
        (DISPLAY_WIDTH - conf_w - 15, 45),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA
    )

    # Sub-teks: nama file + counter
    file_info = f"[{current_idx}/{total_images}]  {image_path.name}"
    cv2.putText(
        canvas, file_info,
        (15, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1, cv2.LINE_AA
    )

    # ═══════════════════════════════════════════════════════
    # GAMBAR UTAMA (ditengah canvas)
    # ═══════════════════════════════════════════════════════
    img_y = header_h + 10
    img_x = (DISPLAY_WIDTH - new_w) // 2
    canvas[img_y: img_y + new_h, img_x: img_x + new_w] = resized

    # Border warna kelas di sekitar gambar
    cv2.rectangle(
        canvas,
        (img_x - 3, img_y - 3),
        (img_x + new_w + 3, img_y + new_h + 3),
        top_color, 2
    )

    # ═══════════════════════════════════════════════════════
    # FOOTER — TOP-N PREDICTIONS
    # ═══════════════════════════════════════════════════════
    footer_y_start = img_y + new_h + 15
    cv2.rectangle(
        canvas,
        (0, footer_y_start - 5),
        (DISPLAY_WIDTH, DISPLAY_HEIGHT),
        (35, 35, 50), -1
    )
    cv2.line(canvas, (0, footer_y_start - 5), (DISPLAY_WIDTH, footer_y_start - 5), (80, 80, 100), 1)

    # Header footer
    cv2.putText(
        canvas, f"Top-{min(TOP_N, len(predictions))} Predictions:",
        (15, footer_y_start + 15),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA
    )

    # Setiap prediksi
    for i, (cls_name, conf) in enumerate(predictions[:TOP_N]):
        y_pos = footer_y_start + 35 + i * 28
        color = get_class_color(cls_name)

        # Rank number
        rank_text = f"#{i + 1}"
        cv2.putText(
            canvas, rank_text,
            (15, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (120, 120, 120), 1, cv2.LINE_AA
        )

        # Class name
        cv2.putText(
            canvas, cls_name,
            (45, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
            color, 2, cv2.LINE_AA
        )

        # Progress bar
        bar_x_start = 190
        bar_width   = int((DISPLAY_WIDTH - bar_x_start - 80) * conf)
        bar_h       = 14
        bar_y       = y_pos - bar_h + 3

        # Background bar
        cv2.rectangle(
            canvas,
            (bar_x_start, bar_y),
            (DISPLAY_WIDTH - 75, bar_y + bar_h),
            (60, 60, 70), -1
        )
        # Filled bar
        if bar_width > 0:
            cv2.rectangle(
                canvas,
                (bar_x_start, bar_y),
                (bar_x_start + bar_width, bar_y + bar_h),
                color, -1
            )

        # Confidence percent text
        pct_text = f"{conf * 100:.1f}%"
        cv2.putText(
            canvas, pct_text,
            (DISPLAY_WIDTH - 70, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 220, 220), 1, cv2.LINE_AA
        )

    # Instruksi kontrol
    ctrl_text = "Any key: next  |  Q/ESC: quit"
    (ctrl_w, _), _ = cv2.getTextSize(ctrl_text, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
    cv2.putText(
        canvas, ctrl_text,
        (DISPLAY_WIDTH - ctrl_w - 10, DISPLAY_HEIGHT - 8),
        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (80, 80, 100), 1, cv2.LINE_AA
    )

    return canvas


# ============================================================
# FUNGSI INFERENCE UTAMA
# ============================================================

def run_inference(model, image_paths: list[Path]) -> None:
    """
    Jalankan inferensi pada semua gambar dan tampilkan pop-up window.

    Args:
        model:       YOLO model yang sudah diload
        image_paths: List of Path objects untuk setiap gambar
    """
    total = len(image_paths)
    log.info(f"\nMemulai inferensi pada {total} gambar...")
    log.info("Kontrol: any key = lanjut | 'q' atau ESC = keluar\n")

    # Nama window pop-up
    WINDOW_NAME = "Fruit Detection — YOLO"
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, DISPLAY_WIDTH, DISPLAY_HEIGHT)

    for idx, img_path in enumerate(image_paths, start=1):
        # Baca gambar
        frame = cv2.imread(str(img_path))
        if frame is None:
            log.warning(f"[{idx}/{total}] Tidak bisa membaca: {img_path.name}, skip.")
            continue

        # ── Jalankan prediksi YOLO ──────────────────────────────
        results = model.predict(
            source=str(img_path),
            imgsz=IMAGE_SIZE,
            verbose=False,   # Matikan log verbose per gambar
        )

        # ── Ekstrak top-N predictions ───────────────────────────
        predictions = []
        if results and len(results) > 0:
            result = results[0]
            if hasattr(result, "probs") and result.probs is not None:
                probs = result.probs.data.cpu().numpy()         # Array confidence semua kelas
                class_names = result.names                       # Dict {idx: class_name}

                # Urutkan dari confidence tertinggi
                sorted_indices = np.argsort(probs)[::-1]
                for i in sorted_indices[:TOP_N]:
                    predictions.append((class_names[i], float(probs[i])))

        if not predictions:
            log.warning(f"[{idx}/{total}] Tidak ada prediksi untuk: {img_path.name}")
            predictions = [("Unknown", 0.0)]

        # Log hasil ke console
        top_cls, top_conf = predictions[0]
        log.info(
            f"[{idx}/{total}] {img_path.name}\n"
            f"         → {top_cls} ({top_conf * 100:.1f}%)"
        )

        # ── Buat frame dengan anotasi visual ───────────────────
        annotated_frame = create_annotated_frame(
            original_image=frame,
            predictions=predictions,
            image_path=img_path,
            current_idx=idx,
            total_images=total,
        )

        # ── Tampilkan di pop-up window ──────────────────────────
        # ⚠️ ATURAN WAJIB: cv2.imshow() HARUS ada di script ini
        cv2.imshow(WINDOW_NAME, annotated_frame)

        # Tunggu input keyboard
        key = cv2.waitKey(WAIT_MS) & 0xFF

        # 'q' (ASCII 113) atau ESC (ASCII 27) untuk keluar
        if key in (ord("q"), 27):
            log.info("Pengguna menekan 'q' / ESC — keluar dari program.")
            break

    # ⚠️ ATURAN WAJIB: Tutup semua window dengan aman
    cv2.destroyAllWindows()
    log.info("\nSemua window ditutup. Program selesai.")


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    log.info("=" * 60)
    log.info("YOLO Fruit Detection — Inference Script")
    log.info("=" * 60)
    log.info(f"Sumber gambar : {Path(IMAGE_SOURCE).resolve()}")
    log.info(f"Model         : {MODEL_PATH}")

    # ── 1. Temukan model ────────────────────────────────────────
    try:
        model_path = find_model()
    except FileNotFoundError as e:
        log.error(str(e))
        sys.exit(1)

    # ── 2. Load model YOLO ──────────────────────────────────
    if not _ULTRALYTICS_AVAILABLE:
        log.error(
            f"Ultralytics tidak dapat diload: {_ULTRALYTICS_ERROR}\n"
            "Coba: pip install 'numpy<2.0' && pip install --upgrade matplotlib ultralytics"
        )
        sys.exit(1)

    log.info(f"Memuat model dari: {model_path}")
    model = YOLO(model_path)

    # ── 3. Kumpulkan gambar ─────────────────────────────────────
    image_paths = collect_image_paths(IMAGE_SOURCE)

    if not image_paths:
        log.error(
            f"Tidak ada gambar ditemukan di: {Path(IMAGE_SOURCE).resolve()}\n"
            "Pastikan folder datasets/ sudah berisi gambar (jalankan prepare_dataset.py)."
        )
        sys.exit(1)

    # ── 4. Jalankan inferensi + pop-up window ───────────────────
    run_inference(model, image_paths)

    log.info("✅ Inferensi selesai!")


if __name__ == "__main__":
    main()

# Implementation Plan: Content Management System (CMS) & Simulasi Pembelian

Rencana implementasi ini dirancang pada tingkat *high-level* agar mudah diikuti dan dieksekusi oleh *junior programmer* atau model AI. Menggunakan **CodeIgniter 4** sebagai framework utama.

---

## Tahap 1: Persiapan Lingkungan & Instalasi (Setup & Installation)
1. **Instalasi Framework:**
   - Install CodeIgniter 4 menggunakan Composer:
     ```bash
     composer create-project codeigniter4/appstarter ci4-cms
     ```
2. **Konfigurasi Environment:**
   - Ubah nama file `env` menjadi `.env`.
   - Ubah `CI_ENVIRONMENT` menjadi `development`.
   - Konfigurasikan koneksi database MySQL/PostgreSQL pada bagian `database.default.*` (hostname, database, username, password).
3. **Konfigurasi UUID:**
   - Karena primary key akan menggunakan UUIDv4, pastikan library atau helper untuk men-generate UUID sudah siap (bisa menggunakan package Ramsey UUID atau helper bawaan PHP/CI4).

---

## Tahap 2: Database Migrations
Gunakan fitur migration bawaan CodeIgniter (`php spark`). Pastikan urutan pembuatan migration tepat untuk menghindari masalah Foreign Key.

1. **Migration Kategori (`categories`):**
   - Kolom: `id` (VARCHAR 36, PK), `name` (VARCHAR 100), `slug` (VARCHAR 100, UNIQUE).
2. **Migration Produk (`products`):**
   - Kolom: `id` (VARCHAR 36, PK), `category_id` (VARCHAR 36, FK ke categories.id), `title`, `description`, `price` (DECIMAL), `stock` (INT), `created_at`, `updated_at`.
3. **Migration Pesanan (`orders`):**
   - Kolom: `id` (VARCHAR 36, PK), `customer_name`, `customer_email`, `total_amount`, `status` (PENDING, PAID, CANCELLED), `created_at`.
4. **Migration Item Pesanan (`order_items`):**
   - Kolom: `id` (VARCHAR 36, PK), `order_id` (VARCHAR 36, FK), `product_id` (VARCHAR 36, FK), `quantity`, `price_at_purchase`.
   
*Tugas: Jalankan `php spark migrate` setelah semua file migration selesai dibuat.*

---

## Tahap 3: Pembuatan Model (Models)
Buat representasi model untuk setiap tabel database.

1. **CategoryModel, ProductModel, OrderModel, OrderItemModel:**
   - Gunakan `php spark make:model [NamaModel]`.
   - Atur konfigurasi wajib di setiap model:
     - `$table` sesuai nama tabel.
     - `$primaryKey = 'id'`.
     - `$useAutoIncrement = false` (Karena menggunakan UUID).
     - `$returnType = 'object'` atau `'array'`.
     - Daftarkan semua kolom yang dapat diisi pada `$allowedFields`.
2. **Implementasi UUID Otomatis:**
   - Gunakan fitur event callback `$beforeInsert` pada model. Buat fungsi untuk otomatis men-generate dan mengisi field `id` dengan UUIDv4 sebelum data disimpan ke database.

---

## Tahap 4: Pembuatan Controller & Routing
Membagi logic backend (Manajemen CMS) dan logic frontend (Simulasi Toko).

1. **Backend / Admin CMS Controllers (CRUD):**
   - `CategoryController`: Menangani list kategori, form tambah, proses simpan, form edit, update, dan hapus.
   - `ProductController`: Menangani list produk, form tambah (dengan pilihan kategori dropdown), proses simpan, edit, update, dan hapus.
   - `OrderController`: Menangani list transaksi/order, melihat detail order (termasuk itemnya), dan update status (PENDING -> PAID/CANCELLED).
2. **Frontend / Shop Controllers:**
   - `ShopController`: Menampilkan list produk ke pengunjung.
   - `CheckoutController`: Menangani form simulasi pembelian produk. Menerima input nama pembeli, email, produk yang dibeli, dan quantity.
3. **Routing (`app/Config/Routes.php`):**
   - Atur route groups agar URL terstruktur, misal: `/admin/products`, `/admin/categories`, dan `/shop`.

---

## Tahap 5: Desain Layout UI Sederhana (Views)
Gunakan library CSS standar seperti **Bootstrap 5** via CDN agar UI terlihat rapi dan cepat dibuat.

1. **Layout Utama (Template):**
   - Buat `app/Views/layouts/admin.php` untuk menu CMS (Sidebar/Navbar).
   - Buat `app/Views/layouts/shop.php` untuk tampilan pembeli.
2. **Halaman Admin:**
   - Views untuk Category (Index, Create, Edit).
   - Views untuk Product (Index, Create, Edit).
   - Views untuk Order (Index, Detail).
3. **Halaman Shop:**
   - View daftar produk (Grid/Cards).
   - View formulir checkout / simulasi order.

---

## Tahap 6: Integrasi Logic Pembelian (Simulasi Transaksi)
Ini adalah *core logic* dari sistem simulasi pembelian (tanpa login):

1. **Validasi Form Checkout:** Pastikan nama, email, dan item terisi valid.
2. **Simpan Tabel `orders`:** 
   - Generate `orders.id` (UUID).
   - Hitung total harga, simpan nama & email. Status default `PENDING`.
3. **Simpan Tabel `order_items`:**
   - Looping produk yang dibeli, ambil harga *saat ini* dari tabel `products`, simpan ke `price_at_purchase`.
   - Simpan `order_id`, `product_id`, dan `quantity`.
4. **Pengurangan Stok (Opsional):** Jika diperlukan, kurangi nilai kolom `stock` di tabel `products` sebanyak `quantity` yang dibeli.

---

## Tahap 7: Testing & Finalisasi
- Jalankan server menggunakan `php spark serve`.
- **Skenario Testing Junior Programmer:**
  - [x] Bisa menambahkan, mengubah, menghapus kategori.
  - [x] Bisa menambahkan produk dan menghubungkannya dengan kategori yang ada.
  - [x] Bisa melakukan simulasi pesanan melalui halaman Shop (seolah-olah sebagai pembeli).
  - [x] Database terisi dengan benar (terutama relasi UUID dan `price_at_purchase`).
  - [x] Bisa merubah status pesanan dari dashboard admin.

# ► Ohyul-Street-Arcade // COFFEE_OPTIMIZER ◄

Proyek ini merupakan **Aplikasi Desktop Interaktif berbasis GUI (Graphical User Interface)** yang dirancang khusus untuk menyelesaikan masalah optimasi kombinasi produk pada bisnis kedai kopi. Program ini dibangun menggunakan bahasa pemrograman Python sebagai bentuk pemenuhan luaran **Tugas Akhir / Ujian Akhir Semester (UAS) mata kuliah Teknik Riset Operasi**.

Aplikasi ini mengusung estetika **Retro Boyish, Streetwear, & Hip-Hop Arcade Interface** dengan menampilkan *cutscene* penjelasan mekanis *step-by-step* oleh rangkaian aset foto karakter **Ohyul**.

---

👥 Tim Pengembang & Identitas Project 

**Mata Kuliah:** Teknik Riset Operasi (TRO) 

| Player | Nama Anggota | NIM | Peran Utama |
| --- | --- | --- | --- |
| 🕹️ **PLAYER_01** | **Hafsah Hamidah** | `2311474` | Core Developer & UI/UX Designer |
| 🕹️ **PLAYER_02** | **Alifa Salsabila** | `2308138` | Algorithm Engineer & Data Modeler |

---

📑 1. Deskripsi Studi Kasus 

Proyek ini menyelesaikan permasalahan operasional riil yang dihadapi oleh sebuah kedai kopi skala UMKM. Manajemen kedai ingin mencari **keuntungan bersih maksimum harian** dari kombinasi penjualan dua jenis menu unggulan mereka: **Kopi Susu ($X_1$)** dan **Matcha Latte ($X_2$)**.

Dalam menjalankan operasionalnya, manajemen menghadapi keterbatasan daya dukung sumber daya (*resource scarcity*) sebagai berikut:

1. **Keterbatasan Pasokan Bahan Baku:** Kedua menu menggunakan susu sebagai komponen dasar utama, namun total pasokan susu segar harian dibatasi maksimal **10.000 ml**.
2. **Keterbatasan Waktu Kerja Barista:** Proses pembuatan, penyajian, hingga penjaminan mutu memerlukan waktu operasional di mana total jam kerja efektif barista dibatasi maksimal **400 menit**.

**Tujuan Penyelesaian:** Menentukan kuantitas kombinasi produksi harian paling optimal ($X_1$ dan $X_2$) agar seluruh kapasitas bahan baku terserap efisien tanpa ada sumber daya yang terbuang sia-sia (*zero slack*) demi menghasilkan profit tertinggi.

---

🧮 2. Metode yang Digunakan (Metode Grafis) 

Metode Riset Operasi yang dipilih dalam proyek ini adalah **Metode Grafis (Linear Programming)**.

Alasan Pemilihan Metode:

* **Kesesuaian Dimensi Variabel:** Masalah ini hanya melibatkan 2 variabel keputusan ($X_1$ dan $X_2$), sehingga sangat ideal dan valid untuk dipetakan ke dalam koordinat kartesius dua dimensi (Sumbu X dan Sumbu Y).
* **Kemudahan Interpretasi Visual:** Sifat Metode Grafis yang mengandalkan grafik memudahkan pemilik kedai dalam memahami daerah kelayakan (*Feasible Region*) secara intuitif ketimbang melihat deretan matriks angka yang kaku.

Formulasi Model Matematika:

* **Variabel Keputusan:**
* $X_1$ = Jumlah cup Kopi Susu yang diproduksi per hari.
* $X_2$ = Jumlah cup Matcha Latte yang diproduksi per hari.


* **Fungsi Tujuan (Maximize Profit $Z$):**

$$\text{Maximize } Z = 15.000X_1 + 20.000X_2$$



*(Asumsi keuntungan bersih per cup: Kopi Susu = Rp15.000, Matcha Latte = Rp20.000)*
* **Fungsi Kendala (Constraints):**
1. **Kendala Kapasitas Susu:** $100X_1 + 200X_2 \le 10.000 \text{ ml}$
2. **Kendala Waktu Barista:** $5X_1 + 5X_2 \le 400 \text{ menit}$
3. **Syarat Non-Negatif:** $X_1 \ge 0, X_2 \ge 0$



---

📊 3. Proses dan Hasil Penyelesaian 

Aplikasi `OhyulStreetArcadeApp` secara otomatis mengalkulasi langkah komputasi matematis yang sinkron dengan perhitungan manual teoritis berikut:

1. **Titik Potong Garis Kendala 1 (Susu): $100X_1 + 200X_2 = 10.000$**
* Jika $X_1 = 0 \rightarrow X_2 = 50 \rightarrow \text{Titik A }(0, 50)$
* Jika $X_2 = 0 \rightarrow X_1 = 100 \rightarrow \text{Titik B }(100, 0)$


2. **Titik Potong Garis Kendala 2 (Waktu): $5X_1 + 5X_2 = 400$**
* Jika $X_1 = 0 \rightarrow X_2 = 80 \rightarrow \text{Titik C }(0, 80)$
* Jika $X_2 = 0 \rightarrow X_1 = 80 \rightarrow \text{Titik D }(80, 0)$


3. **Titik Potong Hasil Eliminasi & Substitusi Sumbu (Titik Temu Optimal):**
* $X_1 + 2X_2 = 100$ (Persamaan Susu disederhanakan)
* $X_1 + X_2 = 80$ (Persamaan Waktu disederhanakan)
* Hasil Eliminasi: $X_2 = 20 \rightarrow$ Substitusi ke Pers. 2: $X_1 = 60$. Didapat **Titik E (60, 20)**.



### Uji Titik Sudut Feasible Region & Hasil Akhir:

Sistem memindai area layak yang dibatasi oleh titik-titik sudut berikut:

* Titik (0, 0) $\rightarrow Z = 15.000(0) + 20.000(0) = \text{Rp0}$
* Titik A (0, 50) $\rightarrow Z = 15.000(0) + 20.000(50) = \text{Rp1.000.000}$
* Titik D (80, 0) $\rightarrow Z = 15.000(80) + 20.000(0) = \text{Rp1.200.000}$
* **Titik E (60, 20) $\rightarrow Z = 15.000(60) + 20.000(20) = \text{Rp1.300.000}$ (SOLUSI OPTIMAL)**

**Kesimpulan Analisis:** Kombinasi produksi harian terbaik untuk meraup profit tertinggi adalah **60 Cup Kopi Susu** dan **20 Cup Matcha Latte** dengan total keuntungan bersih mencapai **Rp1.300.000/hari**.

---

🕹️ 4. Alur Kerja Sistem & Deskripsi Program 

### Fitur Utama Program:

* **Retro Streetwear & Boyish Arcade Look:** Antarmuka visual kontras menggunakan perpaduan warna *White, Cream, Ink Black,* dan *Vandal Red* dengan sudut kaku tajam (`corner_radius=0`) khas mesin terminal arcade game klasik.
* **Integrated Cutscene Dialogue Box:** Gambar wajah karakter Ohyul bersatu di dalam kotak dialog (`bubble_chat_box`). Lebar teks dikunci (`wraplength=230`) untuk mencegah tulisan menabrak foto Ohyul di pojok kanan bawah.
* **Smooth Animation Typewriter with Lip-Sync:** Efek teks mengetik sinematik (45ms delay). Mulut Ohyul akan membuka dan menutup secara berkala setiap kelipatan 4 huruf yang tercetak di layar (`index // 4`).
* **Instant Reveal / Skip Mechanism:** Tombol `NEXT_INTERATION_PHASE()` bersifat multi-fungsi. Jika diklik saat teks sedang mengetik, teks akan langsung muncul secara utuh (*instant reveal*). Jika diklik saat teks sudah berhenti, aplikasi baru akan berpindah ke langkah grafik selanjutnya.
* **Retro Hatched Plotting:** Area *Feasible Region* di-render menggunakan pola arsiran silang miring tebal (`hatch='\\\\\\'`) khas cetakan blueprint komik indie.
* **Dynamic Finish Loop Animation:** Ketika mencapai fase solusi akhir (Step 5), wajah Ohyul otomatis masuk ke mode selebrasi bergerak menaikkan alis secara berulang (`ohyul8.png` $\leftrightarrow$ `ohyul9.png` setiap 400ms).

### Alur Kerja Iterasi Program:

1. **[INITIATED]:** Pengguna memasukkan variabel profit dan kapasitas batas (atau memakai parameter default), lalu mengklik tombol `[ RUN_GRAPHIC_COMPUTATION ]`.
2. **STEP 01:** Program merelasikan input menjadi fungsi tujuan dan fungsi kendala model matematika.
3. **STEP 02:** Menggambar garis batas Kendala Susu beserta visualisasi titik potong koordinat sumbunya.
4. **STEP 03:** Menggambar garis batas Kendala Waktu kerja Barista (berupa garis putus-putus merah).
5. **STEP 04:** Pemindaian ruang keputusan layak dan mengarsir wilayah *Feasible Region* memakai pola retro hatching.
6. **STEP 05 [TARGET FIXED]:** Sistem mengunci titik koordinat persilangan optimal, menampilkan rekomendasi cup produksi harian, mencetak keuntungan maksimum, serta mengaktifkan loop animasi angkat alis Ohyul.

---

📦 Prasyarat & Cara Menjalankan 

### 1. Instalasi Modul Pendukung

Jalankan perintah berikut pada terminal perangkat komputermu untuk menginstal seluruh *dependency library* Python yang digunakan:

```bash
pip install customtkinter matplotlib scipy numpy pillow

```

### 2. Struktur Folder Repositori

Pastikan rangkaian file gambar `.png` diletakkan **sejajar (satu level)** dengan file kodingan utama di dalam folder repositori:

```text
Ohyul-Street-Arcade/
├── app_riset_operasi.py
├── .gitignore
├── README.md
├── ohyul1.png
├── ohyul2.png
...
└── ohyul9.png

```

### 3. Eksekusi Program

Buka PowerShell atau CMD di dalam folder direktori proyek, lalu panggil interpreter Python:

```powershell
python app_riset_operasi.py

```

---

🔗 Output & Lampiran Pendukung UAS 

* 
**Source Code Program:** `app_riset_operasi.py` 


* 
**File Laporan Lapangan:** `[Masukkan_Nama_File_Laporan_Kelompok_Anda.pdf]` 


* 
**File Presentasi (PPTX):** `[Masukkan_Nama_File_Presentasi_Kelompok_Anda.pptx]` 


* 
**Link Dokumentasi Video Demo (YouTube/GDrive):** `[Masukkan_Link_Tautan_Video_Presentasi_UAS_Anda]` 



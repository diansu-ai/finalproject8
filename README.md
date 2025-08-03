# 💰 Financial Planning Advisor

Aplikasi perencanaan keuangan pribadi berbasis AI yang membantu pengguna menganalisis kondisi keuangan, membuat proyeksi tujuan keuangan, dan mendapatkan rekomendasi keuangan yang dipersonalisasi.

## 🚀 Fitur Utama

### 📊 Analisis Keuangan Komprehensif
- **Net Worth Calculator**: Menghitung total aset bersih
- **Rasio Likuiditas**: Mengukur kemampuan membayar pengeluaran dalam 3 bulan
- **Debt-to-Income Ratio**: Menganalisis rasio utang terhadap pendapatan
- **Savings Rate**: Menghitung persentase tabungan dari pendapatan

### 🎯 Perencanaan Tujuan Keuangan
- **Proyeksi Masa Depan**: Menghitung nilai target dengan penyesuaian inflasi
- **Setoran Bulanan**: Menghitung setoran yang diperlukan untuk mencapai tujuan
- **Visualisasi Grafik**: Menampilkan perbandingan target sekarang vs masa depan

### 🤖 AI-Powered Recommendations
- **Konsultasi AI**: Chat interaktif dengan AI Financial Advisor
- **Rekomendasi Personal**: Saran keuangan berdasarkan profil risiko dan kondisi keuangan
- **Multi-Model Support**: Mendukung berbagai model AI (DeepSeek, Qwen, Gemma)

### 📄 Laporan PDF
- **Laporan Lengkap**: Generate laporan PDF dengan analisis keuangan
- **Download Otomatis**: Unduh laporan dalam format PDF
- **Informasi Terstruktur**: Profil klien, analisis, rekomendasi, dan tujuan keuangan

## 🛠️ Teknologi yang Digunakan

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Integration**: OpenRouter API
- **PDF Generation**: FPDF
- **Data Visualization**: Matplotlib
- **Data Processing**: Pandas, NumPy

## 📋 Prerequisites

Sebelum menjalankan aplikasi, pastikan Anda memiliki:

- Python 3.8 atau lebih baru
- pip (Python package manager)
- API Key dari OpenRouter (untuk fitur AI)

## 🔧 Instalasi

### 1. Clone Repository
```bash
git clone <repository-url>
cd finalproject3
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Key
1. Daftar di [OpenRouter](https://openrouter.ai/)
2. Dapatkan API Key
3. Masukkan API Key di sidebar aplikasi saat menjalankan

## 🚀 Cara Menjalankan

### Menjalankan Aplikasi
```bash
streamlit run main.py
```

Aplikasi akan terbuka di browser dengan URL: `http://localhost:8501`

## 📖 Panduan Penggunaan

### 1. Input Data Klien
- **Profil Dasar**: Nama, usia, status keluarga
- **Arus Kas**: Pendapatan tetap/variabel, pengeluaran wajib/diskresioner
- **Aset & Liabilitas**: Tabungan, investasi, properti, utang
- **Tujuan Keuangan**: Target dana, jangka waktu, prioritas
- **Profil Risiko**: Toleransi risiko (1-5)

### 2. Analisis Keuangan
- Sistem akan menghitung metrik keuangan secara otomatis
- Tampilkan grafik proyeksi tujuan keuangan
- Lihat rekomendasi AI berdasarkan kondisi keuangan

### 3. Konsultasi AI
- Pilih model AI yang diinginkan
- Ajukan pertanyaan seputar perencanaan keuangan
- Dapatkan saran personal dari AI Advisor

### 4. Download Laporan
- Klik "Generate PDF Report"
- Download laporan lengkap dalam format PDF
- Laporan berisi analisis dan rekomendasi keuangan

## 📊 Metrik Keuangan

### Net Worth
```
Net Worth = Total Aset - Total Liabilitas
```

### Rasio Likuiditas
```
Liquidity Ratio = Saldo Tabungan / (Pengeluaran Bulanan / 3)
```

### Debt-to-Income Ratio
```
DTI Ratio = Total Utang / Total Pendapatan
```

### Savings Rate
```
Savings Rate = (Pendapatan - Pengeluaran) / Pendapatan
```

## 🤖 Model AI yang Didukung

| Model | Deskripsi | Kecepatan | Akurasi |
|-------|-----------|-----------|---------|
| DeepSeek R1 | Model cepat untuk respons real-time | ⚡⚡⚡ | ⭐⭐⭐ |
| Qwen 3 235B | Model akurat untuk analisis mendalam | ⚡ | ⭐⭐⭐⭐⭐ |
| Gemma 3 12B | Model efisien untuk keseimbangan | ⚡⚡ | ⭐⭐⭐⭐ |

## 📁 Struktur File

```
finalproject3/
├── main.py              # File utama aplikasi
├── requirements.txt      # Dependencies Python
└── README.md           # Dokumentasi proyek
```

## 🔧 Konfigurasi

### Environment Variables (Opsional)
```bash
OPENROUTER_API_KEY=your_api_key_here
```

### Customization
- Modifikasi `clean_text_for_pdf()` untuk menambah karakter Unicode
- Sesuaikan model AI di `get_ai_response()`
- Ubah styling CSS di bagian custom CSS

## 🐛 Troubleshooting

### Error: UnicodeEncodeError
- **Penyebab**: Karakter Unicode dalam PDF
- **Solusi**: Sudah ditangani dengan fungsi `clean_text_for_pdf()`

### Error: API Key Invalid
- **Penyebab**: API Key OpenRouter tidak valid
- **Solusi**: Periksa API Key di sidebar aplikasi

### Error: Connection Timeout
- **Penyebab**: Koneksi internet lambat
- **Solusi**: Coba lagi atau pilih model AI yang lebih cepat

## 📈 Fitur Mendatang

- [ ] Integrasi dengan API bank untuk data real-time
- [ ] Dashboard analisis tren keuangan
- [ ] Notifikasi pengingat investasi
- [ ] Export data ke Excel/CSV
- [ ] Multi-language support
- [ ] Mobile app version

## 🤝 Kontribusi

Kontribusi sangat dihargai! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👨‍💻 Author

**Dian Sulistiadi**
- Email: [your-email@example.com]
- LinkedIn: [your-linkedin]
- GitHub: [your-github]

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) untuk framework UI
- [OpenRouter](https://openrouter.ai/) untuk AI API
- [FPDF](http://www.fpdf.org/) untuk PDF generation
- [Matplotlib](https://matplotlib.org/) untuk visualisasi data

---

⭐ Jika proyek ini membantu Anda, jangan lupa untuk memberikan star! 
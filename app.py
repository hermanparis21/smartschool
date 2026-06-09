import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
from geopy.distance import geodesic

# ==========================================
# 1. KONFIGURASI HALAMAN & FILOSOFI VISUAL (UI/UX)
# ==========================================
st.set_page_config(
    page_title="SMA Muhammadiyah 4 Banjarnegara",
    page_icon="🕌",
    layout="centered"
)

# Custom CSS untuk menginjeksikan Palet Warna Strategis & Estetika Lokal
st.markdown("""
    <style>
    :root {
        --maroon-utama: #800000;
        --emas-aksen: #D4AF37;
        --hitam-solid: #1A1A1A;
        --hijau-alami: #2E7D32;
    }
    
    .stApp {
        background-color: #F9F9F9;
        background-image: radial-gradient(#2e7d320a 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    .custom-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid var(--maroon-utama);
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    .perpus-card {
        background: linear-gradient(135deg, var(--hitam-solid) 0%, #333333 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid var(--emas-aksen);
        position: relative;
        margin-bottom: 20px;
    }
    
    h1, h2, h3 {
        color: var(--maroon-utama) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .emas-text {
        color: var(--emas-aksen);
        font-weight: bold;
    }
    
    .hijau-text {
        color: var(--hijau-alami);
        font-weight: bold;
    }
    
    .stButton>button {
        background-color: var(--maroon-utama);
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: var(--emas-aksen);
        color: var(--hitam-solid);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SIMULASI BACKEND & CACHING LAYER (Redis Mock)
# ==========================================
@st.cache_data
def get_cached_academic_data():
    jadwal = {
        "Senin": ["Al-Islam & Kemuhammadiyahan (ISMU)", "Matematika Peminatan", "Bahasa Inggris"],
        "Selasa": ["Fisika", "Biologi", "Sejarah Indonesia"],
        "Rabu": ["Kimia", "Bahasa Indonesia", "Geografi"],
        "Kamis": ["ISMU (Tahfidz)", "Sosiologi", "Ekonomi"],
        "Jumat": ["Olah Raga / Tapak Suci", "Seni Budaya"]
    }
    return jadwal

if 'poin_siswa' not in st.session_state:
    st.session_state.poin_siswa = 100
if 'log_pelanggaran' not in st.session_state:
    st.session_state.log_pelanggaran = []
if 'minat_bakat_data' not in st.session_state:
    st.session_state.minat_bakat_data = [
        {"nama": "Siswa A", "klaster": "Kuliah", "tujuan": "S1 Teknik Informatika PTM"},
        {"nama": "Siswa B", "klaster": "Kuliah", "tujuan": "S1 Kedokteran PTN"},
        {"nama": "Siswa C", "klaster": "Kerja/Wirausaha", "tujuan": "Kuliner Mandiri"},
        {"nama": "Siswa D", "klaster": "Kuliah", "tujuan": "S1 Hukum PTN"},
        {"nama": "Siswa E", "klaster": "Kerja/Wirausaha", "tujuan": "Teknisi Otomotif"},
    ]

KOORDINAT_SEKOLAH = (-7.216660152883356, 109.64040457368156)

# ==========================================
# 3. STRUKTUR INTERFACE (NAVIGASI)
# ==========================================
st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h2 style='margin-bottom:0;'>M4B Mobile</h2>
        <small style='color: gray;'>Maju, Berakhlak, Berbudaya</small>
        <hr style='border-top: 2px solid #800000;'>
    </div>
""", unsafe_allow_html=True)

# Navigasi Menu Utama
peran = st.sidebar.radio(
    "Pilih Portal Pengguna:",
    ["Dashboard & Perpus", "Portal Akademik", "Karakter & Kedisiplinan", "Minat & Karir (BK)", "Orang Tua / Administrasi"]
)

st.sidebar.markdown("""
    <div style='opacity: 0.2; font-size: 11px; margin-top: 50px; text-align: center;'>
        🍃 <i>M4B Design System v1.0<br>Perpaduan Batik Jawa Tengah & Daun Teh Kalibening</i>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# A. DASHBOARD UTAMA & IDENTITAS DIGITAL
# ==========================================
if peran == "Dashboard & Perpus":
    st.title("Dashboard Utama")
    
    token_seed = datetime.now().strftime("%Y-%m-%d %H:%M")
    dynamic_token = f"JWT_M4B_{hash(token_seed) % 1000000:06d}"
    
    st.markdown(f"""
        <div class="perpus-card">
            <span style="position: absolute; right: 20px; top: 20px; font-size: 24px;">🕌</span>
            <small style="letter-spacing: 2px; color: #D4AF37;">KARTU IDENTITAS DIGITAL & PERPUSTAKAAN</small>
            <h3 style="color: white !important; margin: 10px 0 0 0;">MUHAMMAD RIFQI</h3>
            <p style="margin: 0; font-size: 13px; opacity: 0.8;">NISN: 006721931 / NBM: 114.33.22</p>
            <hr style="border-top: 1px solid rgba(255,255,255,0.2); margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <small style="opacity: 0.6; display:block;">DYNAMIC ACCESS TOKEN (Expires in 30s)</small>
                    <code style="color: #D4AF37; font-size: 14px; background: transparent;">{dynamic_token}</code>
                </div>
                <div style="background: white; padding: 5px; border-radius: 5px; color: black; font-weight: bold; font-size: 10px;">
                    [ QR CODE ]
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📚 Histori Buku Perpustakaan"):
        st.info("⏰ **Notifikasi H-1:** Sistem otomatis mendeteksi batas waktu pinjam.")
        df_perpus = pd.DataFrame({
            "Judul Buku": ["Fisika Dasar XI", "Sejarah Kemuhammadiyahan", "Negeri di Ujung Tanduk"],
            "Tgl Pinjam": ["2026-06-01", "2026-06-03", "2026-06-05"],
            "Jatuh Tempo": ["2026-06-09", "2026-06-10", "2026-06-12"],
            "Status": ["⚠️ Batas Waktu Besok", "Aman", "Aman"]
        })
        st.table(df_perpus)

    st.subheader("📸 Presensi Kehadiran & Sholat Dhuha")
    st.caption("Lokasi Target: Kawasan Pegunungan Kalibening (Toleransi Radius 100 Meter)")
    
    col1, col2 = st.columns(2)
    with col1:
        lat_user = st.number_input("Simulasi Garis Lintang (Latitude)", value=-7.2166, format="%.6f")
    with col2:
        lon_user = st.number_input("Simulasi Garis Bujur (Longitude)", value=109.6404, format="%.6f")
        
    tipe_absen = st.selectbox("Jenis Presensi", ["Presensi Masuk Sekolah", "Sholat Dhuha Bersama"])
    file_selfie = st.checkbox("Simulasi Deteksi Wajah Bergerak/Kedip (Liveness Detection Pass)")
    
    if st.button("Kirim Presensi Digital"):
        jarak = geodesic((lat_user, lon_user), KOORDINAT_SEKOLAH).meters
        if jarak <= 100 and file_selfie:
            st.success(f"✅ Presensi Berhasil! Anda berada {jarak:.2f} meter dari sekolah.")
            st.markdown("<span class='hijau-text'>🟢 Indikator Hijau Alami: Kehadiran Terbaca di Dashboard Guru.</span>", unsafe_allow_html=True)
        else:
            st.error(f"❌ Presensi Gagal! Jarak Anda {jarak:.2f} meter (Maksimal toleransi 100m) atau Liveness Detection gagal.")

    st.subheader("📰 Warta Sekolah & PR IPM")
    st.markdown("""
    <div class="custom-card">
        <h4>Pelantikan Pimpinan Ranting IPM SMA Muhammadiyah 4 Banjarnegara</h4>
        <p style="font-size:13px; color:gray;">Diposting oleh: Pembina IPM • 2 hari lalu</p>
        <p>Mari dukung sinergi kepengurusan baru untuk mewujudkan iklim kreatif di lingkungan sekolah pegunungan kita!</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# B. PORTAL AKADEMIK & RUANG KELAS
# ==========================================
elif peran == "Portal Academic" or peran == "Portal Akademik":
    st.title("📚 Portal Akademik & Ruang Belajar")
    
    jadwal_pelajaran = get_cached_academic_data()
    hari_ini = datetime.now().strftime("%A")
    hari_map = {"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis", "Friday": "Jumat"}
    hari_aktif = hari_map.get(hari_ini, "Senin")
    
    st.subheader(f"📅 Jadwal Pelajaran Hari Ini ({hari_aktif})")
    for mapel in jadwal_pelajaran[hari_aktif]:
        st.markdown(f"- **{mapel}**")
        
    st.subheader("📝 Histori Tugas & Progres Belajar")
    tab_pending, tab_submitted, tab_graded = st.tabs(["⏳ Pending", "📤 Submitted", "💯 Graded"])
    
    with tab_pending:
        st.warning("Tugas Analisis Isu Sosial (Sosiologi) - Tenggat: 2 Hari Lagi")
    with tab_submitted:
        st.info("Rangkuman Buku Kemuhammadiyahan Bab 4 - Mengidentifikasi Gerakan KH. Ahmad Dahlan")
    with tab_graded:
        st.success("Evaluasi Bab Matematika Trigonometri - Nilai: 92 (Sangat Baik)")

# ==========================================
# C. PORTAL KARAKTER, KEAGAMAAN, & KEDISIPLINAN
# ==========================================
elif peran == "Karakter & Kedisiplinan":
    st.title("🕌 Portal Adab, Karakter & Log Santri")
    tab_ibadah, tab_tahfidz, tab_bk = st.tabs(["📿 Mutaba'ah Yaumiyah", "📖 Target Tahfidz", "🚨 Sistem Poin Pelanggaran"])
    
    with tab_ibadah:
        st.subheader("Jurnal Ibadah Mandiri")
        st.checkbox("Sholat Shubuh Berjamaah")
        st.checkbox("Sholat Dhuha (Tervalidasi Sistem)")
        st.checkbox("Tadarus Al-Qur'an (1 Halaman)")
        st.button("Simpan Jurnal & Kirim ke Orang Tua")
        
    with tab_tahfidz:
        st.subheader("Progres Capaian Hafalan Al-Qur'an")
        st.metric(label="Surat Terakhir Diuji", value="An-Naba (Ayat 1-40)", delta="Lancar / Mutqin")
        st.text_area("Catatan Guru Penguji:", "Tajwid sudah baik pada mad thabi'i, perhatikan makhraj huruf 'Ain.")
        
    with tab_bk:
        st.subheader("⚖️ Histori Pelanggaran (Sistem Poin Dekremen)")
        poin_sekarang = st.session_state.poin_siswa
        
        if poin_sekarang <= 75:
            st.error(f"🚨 POIN SEKARANG: {poin_sekarang} / 100 - WARNING ALERT DIPICU KE GAWAI ORANG TUA!")
        else:
            st.metric(label="Poin Kedisiplinan Saat Ini", value=f"{poin_sekarang} / 100")
            
        st.write("---")
        st.caption("Pusat Input Pelanggaran (Khusus Guru BK / Wali Kelas)")
        jenis_pelanggaran = st.selectbox("Pilih Jenis Pelanggaran:", [
            "Terlambat Masuk Sekolah (-5 Poin)",
            "Atribut Seragam Tidak Lengkap (-10 Poin)",
            "Meninggalkan Kelas Tanpa Izin (-15 Poin)",
            "Melanggar Aturan Berat (-30 Poin)"
        ])
        
        if st.button("Catat Pelanggaran & Kurangi Poin"):
            bobot = int(jenis_pelanggaran.split("(-")[1].split(" ")[0])
            st.session_state.poin_siswa -= bobot
            st.session_state.log_pelanggaran.append({
                "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Pelanggaran": jenis_pelanggaran,
                "Potongan": f"-{bobot}"
            })
            st.rerun()
            
        if st.session_state.log_pelanggaran:
            st.dataframe(pd.DataFrame(st.session_state.log_pelanggaran))

# ==========================================
# E. MENU PEMETAAN MINAT SISWA (BK)
# ==========================================
elif peran == "Minat & Karir (BK)":
    st.title("🚀 Pemetaan Minat & Masa Depan Siswa")
    tab_form, tab_analitik = st.tabs(["📝 Form Kuesioner Siswa", "📊 Dashboard Analitik BK"])
    
    with tab_form:
        st.subheader("Formulir Rencana Masa Depan (Kelas XI & XII)")
        nama_mhs = st.text_input("Nama Siswa:", "Muhammad Rifqi")
        pilihan_klaster = st.radio("Pilih Klaster Fokus:", ["Klaster Kuliah (Akademik)", "Klaster Kerja/Wirausaha (Vokasional)"])
        
        if pilihan_klaster == "Klaster Kuliah (Akademik)":
            univ = st.text_input("Universitas Impian (PTN/PTM):", "Universitas Muhammadiyah Yogyakarta")
            prodi = st.text_input("Jurusan Dituju:", "S1 Sistem Informasi")
            if st.button("Simpan Pilihan Kuliah"):
                st.session_state.minat_bakat_data.append({"nama": nama_mhs, "klaster": "Kuliah", "tujuan": f"{prodi} di {univ}"})
                st.success("Rekomendasi taktik SNBP berhasil disimpan!")
        else:
            keahlian = st.text_input("Bidang Keahlian / Jenis Usaha:", "Digital Marketing")
            if st.button("Simpan Pilihan Vokasional"):
                st.session_state.minat_bakat_data.append({"nama": nama_mhs, "klaster": "Kerja/Wirausaha", "tujuan": keahlian})
                st.success("Informasi kemitraan vokasional berhasil disimpan!")
                
    with tab_analitik:
        st.subheader("Dashboard Kompas Masa Depan (Akses Pihak Sekolah/BK)")
        df_bk = pd.DataFrame(st.session_state.minat_bakat_data)
        
        fig = px.pie(df_bk, names='klaster', color='klaster',
                     color_discrete_map={'Kuliah': '#800000', 'Kerja/Wirausaha': '#2E7D32'},
                     title="Persentase Minat Kelulusan Satu Angkatan")
        st.plotly_chart(fig)
        st.dataframe(df_bk)

# ==========================================
# F. ADMINISTRASI & KEMITRAAN ORANG TUA
# ==========================================
elif peran == "Orang Tua / Administrasi":
    st.title("👨‍👩‍👦 Parent Portal & Transparansi Keuangan")
    
    st.subheader("🔔 Notifikasi Kehadiran Real-time")
    st.markdown("""
    <div class="custom-card" style="border-left-color: #2E7D32;">
        <span class="hijau-text">🟢 HADIR</span><br>
        Ananda <b>Muhammad Rifqi</b> terdeteksi melakukan tap ID Card pada gerbang utama pada pukul <b>06:45 WIB</b>.
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("💳 E-SPP & Portal Pembayaran")
    st.markdown("<span class='emas-text'>Total Tagihan Bulan Ini: Rp 350.000</span>", unsafe_allow_html=True)
    
    metode_bayar = st.selectbox("Pilih Metode Pembayaran VA:", ["BSI Virtual Account", "Bank Jateng Syariah VA"])
    if st.button("Generate Kode Bayar"):
        kode_va = random.randint(1000000000, 9999999999)
        st.info(f"Nomor Akun Virtual Anda: `{kode_va}`")
        
    st.subheader("💬 Ruang Konsultasi BK & Wali Kelas")
    st.text_area("Pesan untuk Guru BK / Wali Kelas:", placeholder="Tuliskan kendala belajar...")
    if st.button("Kirim Pesan Aman"):
        st.success("Pesan terkirim secara aman ke sistem BK sekolah.")

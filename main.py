import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import requests
import json
import base64
from datetime import datetime

# Konfigurasi tampilan
st.set_page_config(
    page_title="Financial Planning Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk tampilan modern
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .header {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ====================== FUNGSI PERHITUNGAN KEUANGAN ======================
def calculate_future_value(present_value, years, inflation_rate):
    """Hitung nilai masa depan dengan penyesuaian inflasi"""
    return present_value * (1 + inflation_rate) ** years

def calculate_monthly_savings(future_value, years, return_rate):
    """Hitung setoran bulanan yang diperlukan"""
    n = years * 12
    r = return_rate / 12
    return (future_value * r) / ((1 + r) ** n - 1)

def calculate_financials(user_data):
    """Lakukan semua perhitungan keuangan"""
    # Hitung net worth
    assets = user_data['tabungan'] + user_data['investasi'] + user_data['properti']
    liabilities = user_data['kpr'] + user_data['kartu_kredit'] + user_data['pinjaman_lain']
    net_worth = assets - liabilities
    
    # Hitung rasio keuangan
    pendapatan_total = user_data['pendapatan_tetap'] + user_data['pendapatan_variabel']
    pengeluaran_total = user_data['pengeluaran_wajib'] + user_data['pengeluaran_diskresioner']
    
    liquidity_ratio = user_data['tabungan'] / (pengeluaran_total / 3)  # dalam bulan
    dti_ratio = (user_data['kpr'] + user_data['kartu_kredit'] + user_data['pinjaman_lain']) / pendapatan_total
    savings_rate = (pendapatan_total - pengeluaran_total) / pendapatan_total
    
    # Proyeksi tujuan keuangan
    goal_projections = []
    for goal in user_data['tujuan']:
        future_value = calculate_future_value(
            goal['target'], 
            years=goal['tahun'], 
            inflation_rate=0.05  # asumsi inflasi 5%
        )
        monthly_payment = calculate_monthly_savings(
            future_value, 
            years=goal['tahun'], 
            return_rate=0.1  # asumsi return 10% p.a.
        )
        goal_projections.append({
            'nama': goal['nama'],
            'target_sekarang': goal['target'],
            'target_masa_depan': future_value,
            'setoran_bulanan': monthly_payment,
            'jangka_waktu': goal['tahun']
        })
    
    # Rekomendasi AI sederhana
    recommendations = generate_recommendations(user_data, net_worth, dti_ratio, savings_rate)
    
    return {
        'net_worth': net_worth,
        'liquidity_ratio': round(liquidity_ratio, 1),
        'dti_ratio': round(dti_ratio, 2),
        'savings_rate': savings_rate,
        'goal_projections': goal_projections,
        'recommendations': recommendations
    }

def generate_recommendations(user_data, net_worth, dti, savings_rate):
    """Buat rekomendasi keuangan sederhana"""
    recs = []
    
    # Rekomendasi dana darurat
    monthly_expenses = user_data['pengeluaran_wajib'] + user_data['pengeluaran_diskresioner']
    emergency_fund = monthly_expenses * 6
    if user_data['tabungan'] < emergency_fund:
        recs.append(f"💡 Tingkatkan dana darurat hingga Rp {emergency_fund:,.0f} (6x pengeluaran bulanan)")
    
    # Rekomendasi utang
    if dti > 0.4:
        recs.append("⚠️ Kendalikan rasio utang-pendapatan Anda. Pertimbangkan melunasi utang berbiaya tinggi terlebih dahulu")
    
    # Rekomendasi tabungan
    if savings_rate < 0.2:
        recs.append(f"🔧 Tingkatkan savings rate Anda. Idealnya minimal 20% dari pendapatan")
    
    # Rekomendasi alokasi aset
    equity_pct = min(90, 110 - user_data['usia'])
    recs.append(f"📊 Alokasi aset rekomendasi: {equity_pct}% saham, {100-equity_pct}% pendapatan tetap")
    
    return "\n\n".join(recs)

def plot_goals(goals):
    """Buat visualisasi tujuan keuangan menggunakan Plotly"""
    goal_names = [g['nama'] for g in goals]
    current_targets = [g['target_sekarang'] / 1e6 for g in goals]
    future_targets = [g['target_masa_depan'] / 1e6 for g in goals]
    
    # Buat figure dengan Plotly
    fig = go.Figure()
    
    # Tambahkan bar untuk target sekarang
    fig.add_trace(go.Bar(
        name='Target Sekarang',
        x=goal_names,
        y=current_targets,
        marker_color='#6a11cb'
    ))
    
    # Tambahkan bar untuk target masa depan
    fig.add_trace(go.Bar(
        name='Target Masa Depan',
        x=goal_names,
        y=future_targets,
        marker_color='#2575fc'
    ))
    
    # Update layout
    fig.update_layout(
        title='Perbandingan Target Keuangan',
        xaxis_title='Tujuan Keuangan',
        yaxis_title='Juta IDR',
        barmode='group',
        height=500,
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update axes
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    st.plotly_chart(fig, use_container_width=True)

# ====================== FUNGSI AI CHAT ======================
def get_ai_response(prompt, model="deepseek/deepseek-r1-0528-qwen3-8b:free", api_key=None):
    """Dapatkan respons dari OpenRouter API"""
    if not api_key:
        return "🔑 Silakan masukkan API Key OpenRouter di sidebar"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Maaf, terjadi kesalahan: {str(e)}"

# ====================== FUNGSI LAPORAN PDF ======================
class PDFReport(FPDF):
    """Kelas untuk membuat laporan PDF"""
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Laporan Perencanaan Keuangan', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f"Tanggal: {datetime.now().strftime('%d %B %Y')}", 0, 1, 'C')
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 8, body)
        self.ln()

def clean_text_for_pdf(text):
    """Bersihkan teks dari karakter Unicode yang tidak didukung oleh latin-1"""
    # Daftar karakter Unicode yang perlu diganti
    unicode_replacements = {
        '💡': '',
        '⚠️': '',
        '🔧': '',
        '📊': '',
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '•': '-',
        '–': '-',
        '—': '-',
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '…': '...',
        '°': ' derajat',
        '±': '+/-',
        '×': 'x',
        '÷': '/',
        '≤': '<=',
        '≥': '>=',
        '≠': '!=',
        '≈': '~',
        '∞': 'infinity',
        '∑': 'sum',
        '∏': 'product',
        '√': 'sqrt',
        '∫': 'integral',
        '∂': 'partial',
        '∆': 'delta',
        '∇': 'nabla',
        '∈': 'in',
        '∉': 'not in',
        '⊂': 'subset',
        '⊃': 'superset',
        '∪': 'union',
        '∩': 'intersection',
        '∅': 'empty',
        '∀': 'for all',
        '∃': 'exists',
        '∄': 'not exists',
        '∴': 'therefore',
        '∵': 'because',
        '≡': 'equivalent',
        '≅': 'congruent',
        '∝': 'proportional',
        '∞': 'infinity',
        'α': 'alpha',
        'β': 'beta',
        'γ': 'gamma',
        'δ': 'delta',
        'ε': 'epsilon',
        'ζ': 'zeta',
        'η': 'eta',
        'θ': 'theta',
        'ι': 'iota',
        'κ': 'kappa',
        'λ': 'lambda',
        'μ': 'mu',
        'ν': 'nu',
        'ξ': 'xi',
        'ο': 'omicron',
        'π': 'pi',
        'ρ': 'rho',
        'σ': 'sigma',
        'τ': 'tau',
        'υ': 'upsilon',
        'φ': 'phi',
        'χ': 'chi',
        'ψ': 'psi',
        'ω': 'omega',
        'Α': 'Alpha',
        'Β': 'Beta',
        'Γ': 'Gamma',
        'Δ': 'Delta',
        'Ε': 'Epsilon',
        'Ζ': 'Zeta',
        'Η': 'Eta',
        'Θ': 'Theta',
        'Ι': 'Iota',
        'Κ': 'Kappa',
        'Λ': 'Lambda',
        'Μ': 'Mu',
        'Ν': 'Nu',
        'Ξ': 'Xi',
        'Ο': 'Omicron',
        'Π': 'Pi',
        'Ρ': 'Rho',
        'Σ': 'Sigma',
        'Τ': 'Tau',
        'Υ': 'Upsilon',
        'Φ': 'Phi',
        'Χ': 'Chi',
        'Ψ': 'Psi',
        'Ω': 'Omega'
    }
    
    cleaned_text = text
    for unicode_char, replacement in unicode_replacements.items():
        cleaned_text = cleaned_text.replace(unicode_char, replacement)
    
    # Hapus karakter Unicode lainnya yang tidak dalam daftar
    cleaned_text = ''.join(char for char in cleaned_text if ord(char) < 256)
    
    return cleaned_text

def generate_pdf_report(user_data):
    """Hasilkan laporan PDF dari data pengguna"""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Profil Klien
    pdf.chapter_title('Profil Klien')
    profile_data = [
        f"Nama: {clean_text_for_pdf(user_data['nama'])}",
        f"Usia: {user_data['usia']} tahun",
        f"Usia Pensiun: {user_data['usia_pensiun']} tahun",
        f"Status Keluarga: {clean_text_for_pdf(user_data['status_keluarga'])}"
    ]
    pdf.chapter_body("\n".join(profile_data))
    
    # Analisis Keuangan
    analysis = user_data['analysis']
    pdf.chapter_title('Analisis Keuangan')
    financial_data = [
        f"Net Worth: Rp {analysis['net_worth']:,.0f}",
        f"Rasio Likuiditas: {analysis['liquidity_ratio']} bulan",
        f"Debt-to-Income Ratio: {analysis['dti_ratio']:.2f}",
        f"Savings Rate: {analysis['savings_rate']:.2%}"
    ]
    pdf.chapter_body("\n".join(financial_data))
    
    # Rekomendasi - Bersihkan emoji dari teks
    pdf.chapter_title('Rekomendasi')
    clean_recommendations = clean_text_for_pdf(analysis['recommendations'])
    pdf.chapter_body(clean_recommendations)
    
    # Tujuan Keuangan
    pdf.chapter_title('Tujuan Keuangan')
    goals = []
    for goal in analysis['goal_projections']:
        goals.append(
            f"{clean_text_for_pdf(goal['nama'])}: "
            f"Target Rp {goal['target_sekarang']:,.0f} -> "
            f"Rp {goal['target_masa_depan']:,.0f} "
            f"({goal['jangka_waktu']} tahun) - "
            f"Setoran: Rp {goal['setoran_bulanan']:,.0f}/bulan"
        )
    pdf.chapter_body("\n".join(goals))
    
    return pdf.output(dest='S').encode('latin1')

# ====================== UI UTAMA APLIKASI ======================
def main():
    # Inisialisasi session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hai! Saya AI Financial Advisor. Bagaimana saya bisa membantu perencanaan keuangan Anda hari ini?"}
        ]

    # Sidebar untuk API key
    with st.sidebar:
        st.subheader("🔑 Konfigurasi AI")
        openrouter_key = st.text_input("OpenRouter API Key", type="password")
        st.caption("Dapatkan API Key dari [OpenRouter](https://openrouter.ai/)")
        st.divider()
        st.subheader("⚙️ Pengaturan")
        st.caption("Versi Aplikasi: 1.0.0")
        st.caption("© 2024 Financial Planning Advisor")

    # Header aplikasi
    st.markdown("""
    <div class="header">
        <h1>💰 Financial Planning Advisor</h1>
        <p>Solusi lengkap perencanaan keuangan pribadi berbasis AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Form input data klien
    if st.session_state.step == 1:
        client_info_form()
    else:
        show_financial_analysis(openrouter_key)

def client_info_form():
    """Form input data klien"""
    with st.form("client_info"):
        st.subheader("📝 Profil Klien")
        cols = st.columns(2)
        st.session_state.user_data['nama'] = cols[0].text_input("Nama Lengkap")
        st.session_state.user_data['usia'] = cols[1].number_input("Usia", min_value=18, max_value=100, value=30)
        
        cols = st.columns(2)
        st.session_state.user_data['usia_pensiun'] = cols[0].number_input("Usia Pensiun", min_value=40, max_value=80, value=60)
        st.session_state.user_data['status_keluarga'] = cols[1].selectbox(
            "Status Keluarga", 
            ["Lajang", "Menikah", "Menikah + Anak"]
        )
        
        st.divider()
        st.subheader("💵 Arus Kas Bulanan (IDR)")
        cols = st.columns(2)
        st.session_state.user_data['pendapatan_tetap'] = cols[0].number_input("Pendapatan Tetap", min_value=0, value=10000000)
        st.session_state.user_data['pendapatan_variabel'] = cols[1].number_input("Pendapatan Variabel", min_value=0, value=2000000)
        
        cols = st.columns(2)
        st.session_state.user_data['pengeluaran_wajib'] = cols[0].number_input("Pengeluaran Wajib", min_value=0, value=5000000)
        st.session_state.user_data['pengeluaran_diskresioner'] = cols[1].number_input("Pengeluaran Diskresioner", min_value=0, value=3000000)
        
        st.divider()
        st.subheader("🏦 Aset & Liabilitas (IDR)")
        cols = st.columns(2)
        st.session_state.user_data['tabungan'] = cols[0].number_input("Saldo Tabungan", min_value=0, value=5000000)
        st.session_state.user_data['investasi'] = cols[1].number_input("Nilai Investasi", min_value=0, value=10000000)
        
        cols = st.columns(2)
        st.session_state.user_data['properti'] = cols[0].number_input("Nilai Properti", min_value=0, value=0)
        st.session_state.user_data['kpr'] = cols[1].number_input("Sisa KPR", min_value=0, value=0)
        
        cols = st.columns(2)
        st.session_state.user_data['kartu_kredit'] = cols[0].number_input("Tagihan Kartu Kredit", min_value=0, value=0)
        st.session_state.user_data['pinjaman_lain'] = cols[1].number_input("Pinjaman Lainnya", min_value=0, value=0)
        
        st.divider()
        st.subheader("🎯 Tujuan Keuangan")
        goals = []
        for i in range(3):
            cols = st.columns([3,2,2,1])
            goal_name = cols[0].text_input(f"Nama Tujuan {i+1}", key=f"goal_name_{i}", value="")
            goal_amount = cols[1].number_input(f"Target Dana", key=f"goal_amount_{i}", min_value=0, value=0)
            goal_years = cols[2].number_input(f"Jangka Waktu (tahun)", key=f"goal_years_{i}", min_value=1, value=5)
            goal_priority = cols[3].selectbox(f"Prioritas", [1,2,3], key=f"goal_priority_{i}")
            
            if goal_name:
                goals.append({
                    "nama": goal_name,
                    "target": goal_amount,
                    "tahun": goal_years,
                    "prioritas": goal_priority
                })
        
        st.session_state.user_data['tujuan'] = goals
        
        st.divider()
        st.subheader("📊 Profil Risiko")
        st.session_state.user_data['risk_profile'] = st.slider(
            "Seberapa besar toleransi risiko Anda? (1: Sangat Rendah, 5: Sangat Tinggi)", 
            1, 5, 3
        )
        
        if st.form_submit_button("🚀 Lakukan Analisis Keuangan"):
            st.session_state.step = 2
            st.session_state.analysis_done = True
            st.rerun()

def show_financial_analysis(api_key):
    """Tampilkan hasil analisis dan fitur chat"""
    # Tombol kembali ke input
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button("⬅️ Kembali ke Input Data", use_container_width=True):
            st.session_state.step = 1
            st.rerun()
    
    st.divider()
    
    # Lakukan perhitungan
    analysis = calculate_financials(st.session_state.user_data)
    st.session_state.user_data['analysis'] = analysis
    
    # Tampilkan metrik utama
    st.subheader("📊 Hasil Analisis Keuangan")
    cols = st.columns(4)
    cols[0].metric("Net Worth", f"Rp {analysis['net_worth']:,.0f}")
    cols[1].metric("Rasio Likuiditas", f"{analysis['liquidity_ratio']} bulan")
    cols[2].metric("Debt-to-Income", f"{analysis['dti_ratio']:.2f}")
    cols[3].metric("Savings Rate", f"{analysis['savings_rate']:.2%}")
    
    # Tampilkan grafik
    st.subheader("📈 Proyeksi Tujuan Keuangan")
    plot_goals(analysis['goal_projections'])
    
    # Rekomendasi AI
    st.subheader("🔍 AI Powered Recommendations")
    with st.expander("Lihat Rekomendasi Keuangan", expanded=True):
        st.write(analysis['recommendations'])
    
    # Tab untuk chat dan laporan
    chat_tab, report_tab = st.tabs(["💬 Konsultasi AI", "📥 Download Laporan"])
    
    with chat_tab:
        ai_chat_section(api_key)
    
    with report_tab:
        st.subheader("📥 Unduh Laporan Lengkap")
        if st.button("🖨️ Generate PDF Report"):
            report_bytes = generate_pdf_report(st.session_state.user_data)
            st.download_button(
                label="⬇️ Download PDF",
                data=report_bytes,
                file_name="financial_report.pdf",
                mime="application/pdf"
            )

def ai_chat_section(api_key):
    """Section untuk chat dengan AI"""
    st.info("Anda dapat berkonsultasi lebih lanjut dengan AI Financial Advisor")
    
    # Pilih model AI
    model_options = {
        "deepseek/deepseek-r1-0528-qwen3-8b:free": "DeepSeek R1 (Cepat)",
        "qwen/qwen3-235b-a22b:free": "Qwen 3 235B (Akurat)",
        "google/gemma-3-12b-it:free": "Gemma 3 12B (Efisien)"
    }
    selected_model = st.selectbox(
        "Pilih Model AI", 
        list(model_options.keys()), 
        format_func=lambda x: model_options[x]
    )
    
    # Tampilkan history chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    # Input pengguna
    if prompt := st.chat_input("Tanyakan seputar perencanaan keuangan..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Dapatkan respons dari AI
        with st.spinner("AI Advisor sedang berpikir..."):
            context = json.dumps(st.session_state.user_data, indent=2)
            full_prompt = f"""
            Anda adalah financial advisor profesional. Berikut data klien:
            {context}
            
            Pertanyaan: {prompt}
            """
            response = get_ai_response(full_prompt, selected_model, api_key)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
    

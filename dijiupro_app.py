import csv
import io
import streamlit as st
from dijiupro_phonetics import convert_to_ipa, VOICES
st.set_page_config(
    page_title="IPA Studio | Pronunciation Lab",
    page_icon="🔤",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root {
    --primary: #7966F5;
    --secondary: #38BDF8;
    --text: #F3F4F8;
    --muted: #A3A9BD;
    --panel: #171B2B;
}
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(121,102,245,.19), transparent 38%),
        radial-gradient(ellipse at 95% 20%, rgba(56,189,248,.12), transparent 30%),
        #0C0F1A;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
.block-container {
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}
h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.6px;
}
.hero {
    padding: 2.4rem 1rem 2rem;
    text-align: center;
}
.eyebrow {
    display: inline-block;
    color: #C2B9FF;
    background: rgba(121,102,245,.14);
    border: 1px solid rgba(158,145,255,.32);
    border-radius: 30px;
    padding: 7px 14px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.hero-title {
    margin: 20px 0 10px;
    font-size: clamp(36px, 6vw, 58px);
    line-height: 1.1;
    font-weight: 800;
    color: #FFFFFF;
}
.gradient-text {
    background: linear-gradient(90deg, #A99BFF, #64D4FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-description {
    color: #ADB4C8;
    max-width: 650px;
    margin: 0 auto;
    font-size: 16px;
    line-height: 1.8;
}
.feature-row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
    margin-top: 22px;
}
.feature-pill {
    border: 1px solid #2B3045;
    background: rgba(255,255,255,.035);
    color: #C9CDE0;
    padding: 8px 13px;
    border-radius: 10px;
    font-size: 12px;
}
.section-label {
    color: #B7BECE;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.3px;
    margin: 8px 0 12px;
}
div[data-testid="stTextArea"] textarea {
    background: #121625 !important;
    color: #F4F5FF !important;
    border: 1px solid #343A53 !important;
    border-radius: 15px !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #8978FF !important;
    box-shadow: 0 0 0 1px #8978FF !important;
}
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,.025);
    border: 1px dashed #3B4260;
    border-radius: 14px;
    padding: 10px;
}
div.stButton > button {
    width: 100%;
    min-height: 49px;
    border: 0;
    border-radius: 13px;
    background: linear-gradient(100deg, #7966F5, #477FF5);
    color: white;
    font-size: 15px;
    font-weight: 700;
    transition: .2s ease;
}
div.stButton > button:hover {
    border: 0;
    filter: brightness(1.13);
    box-shadow: 0 7px 25px rgba(121,102,245,.25);
    transform: translateY(-1px);
}
.result-card {
    background: linear-gradient(145deg, #191E30, #131725);
    border: 1px solid #30364F;
    border-radius: 18px;
    padding: 22px;
    min-height: 220px;
    margin: 6px 0 14px;
}
.result-header {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 16px;
    font-weight: 700;
    color: #F5F6FF;
    margin-bottom: 18px;
}
.flag {
    display: inline-flex;
    width: 37px;
    height: 37px;
    border-radius: 11px;
    align-items: center;
    justify-content: center;
    background: rgba(121,102,245,.17);
    font-size: 20px;
}
.ipa-output {
    color: #B9ADFF;
    font-size: 24px;
    line-height: 1.9;
    overflow-wrap: anywhere;
    font-family: 'DM Sans', sans-serif;
}
.card-caption {
    color: #858DA8;
    font-size: 12px;
    margin-top: 14px;
}
.info-strip {
    border: 1px solid #2E3550;
    background: rgba(121,102,245,.07);
    padding: 15px 17px;
    border-radius: 13px;
    color: #C4C9DA;
    font-size: 13px;
    line-height: 1.7;
}
.footer {
    color: #747D96;
    text-align: center;
    font-size: 12px;
    padding: 28px 0 5px;
}
hr {
    border-color: #292E43 !important;
    margin: 26px 0 !important;
}
.stDownloadButton button {
    width: 100%;
    border-radius: 12px;
    min-height: 44px;
}
div[data-testid="stAlert"] {
    border-radius: 12px;
}
@media (max-width: 700px) {
    .hero {
        padding: 1.5rem 0 .8rem;
    }
    .result-card {
        padding: 17px;
    }
    .ipa-output {
        font-size: 20px;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="hero">
    <div class="eyebrow">✦ PRONUNCIATION LAB</div>
    <div class="hero-title">
        English to <span class="gradient-text">IPA Studio</span>
    </div>
    <div class="hero-description">
        Discover how English sounds. Transform words and sentences into
        phonetic transcription and compare American and British pronunciation
        in one place.
    </div>
    <div class="feature-row">
        <span class="feature-pill">🇺🇸 American English</span>
        <span class="feature-pill">🇬🇧 British English</span>
        <span class="feature-pill">🔤 IPA Transcription</span>
        <span class="feature-pill">📄 CSV Export</span>
    </div>
</div>
""", unsafe_allow_html=True)
with st.container():
    st.markdown('<div class="section-label">01 — YOUR TEXT</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a text file",
        type=["txt"],
        help="Upload a UTF-8 text file or type your text below."
    )
    default_text = (
        "The quick brown fox jumps over the lazy dog.\n"
        "I can't believe it's already Friday."
    )
    if uploaded_file is not None:
        input_text = uploaded_file.getvalue().decode(
            "utf-8-sig",
            errors="replace"
        )
    else:
        input_text = default_text
    text = st.text_area(
        "Enter English text",
        value=input_text,
        height=170,
        max_chars=5000,
        label_visibility="collapsed",
        placeholder="Type a word, sentence, or paragraph here..."
    )
    st.caption(f"✍️  {len(text)} / 5000 characters")
    col1, col2 = st.columns([1, 1])
    with col1:
        compare_both = st.toggle("Compare both accents", value=True)
    with col2:
        selected_accent = st.selectbox(
            "Accent",
            options=list(VOICES.keys()),
            disabled=compare_both,
            label_visibility="collapsed"
        )
    convert_clicked = st.button(
        "✦  Convert to IPA",
        type="primary",
        use_container_width=True
    )
if convert_clicked:
    if not text.strip():
        st.warning("Please enter some English text first.")
    else:
        accents = list(VOICES.keys()) if compare_both else [selected_accent]
        results = {}
        errors = {}
        with st.spinner("Analyzing pronunciation..."):
            for accent in accents:
                try:
                    results[accent] = convert_to_ipa(text, accent)
                except Exception as exc:
                    errors[accent] = str(exc)
        for accent, error in errors.items():
            st.error(f"{accent}: {error}")
        if results:
            st.markdown("---")
            st.markdown("## Your pronunciation results")
            st.caption("02 — PHONETIC TRANSCRIPTION")
            result_columns = st.columns(len(results))
            accent_details = {
                "American English": ("🇺🇸", "General American voice"),
                "British English": ("🇬🇧", "Southern British voice")
            }
            for column, accent in zip(result_columns, results):
                flag, description = accent_details[accent]
                with column:
                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-header">
                                <span class="flag">{flag}</span>
                                <span>{accent}</span>
                            </div>
                            <div class="ipa-output">{results[accent]}</div>
                            <div class="card-caption">{description}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.code(results[accent], language=None)
                    st.button(
                        f"Copy {accent} IPA",
                        key=f"copy_{accent}",
                        on_click=lambda value=results[accent]: st.session_state.update(
                            copied_ipa=value
                        )
                    )
            if "copied_ipa" in st.session_state:
                st.text_input(
                    "Selected IPA transcription",
                    value=st.session_state["copied_ipa"],
                    help="Select the text and copy it."
                )
            if len(results) == 2:
                buffer = io.StringIO()
                writer = csv.writer(buffer)
                writer.writerow([
                    "English Text",
                    "American IPA",
                    "British IPA"
                ])
                writer.writerow([
                    text,
                    results.get("American English", ""),
                    results.get("British English", "")
                ])
                st.download_button(
                    "⬇  Download comparison as CSV",
                    data=buffer.getvalue().encode("utf-8-sig"),
                    file_name="ipa_comparison.csv",
                    mime="text/csv",
                    use_container_width=True
                )
st.markdown("---")
st.markdown("## How it works")
info1, info2, info3 = st.columns(3)
with info1:
    st.markdown("### 🔤 IPA")
    st.write("See speech sounds represented by phonetic symbols.")
with info2:
    st.markdown("### 🌎 Accent comparison")
    st.write("Compare the transcription generated for two English voices.")
with info3:
    st.markdown("### 📥 Export")
    st.write("Save both transcriptions in a CSV file for further analysis.")
st.markdown("""
<div class="info-strip">
    <strong>About the results</strong><br>
    Transcriptions are generated by eSpeak NG. They are automatic
    phonetic estimates and may differ from specialist dictionaries,
    regional accents, or individual speakers.
</div>
<div class="footer">
    IPA STUDIO · English Pronunciation Lab · Powered by eSpeak NG
</div>
""", unsafe_allow_html=True)

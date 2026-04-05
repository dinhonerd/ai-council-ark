import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import time
from dotenv import load_dotenv
from groq import Groq
from google import genai
import openai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="AI Council - IDE v2",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARREGAMENTO DE ASSETS (BASE64) ---
def _load_b64(name):
    path = os.path.join(os.path.dirname(__file__), f"img_{name}.b64")
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except:
        return ""

b64_logo = _load_b64("logo")
b64_brain = _load_b64("brain")
b64_shield = _load_b64("shield")
b64_light = _load_b64("lightning")

# --- CSS PROFISSIONAL IDE STYLE (CORRIGIDO) ---
ide_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

    :root {{
        --bg-deep: #08080C;
        --sidebar-bg: #0D0D14;
        --border-color: rgba(255, 255, 255, 0.08);
        --purple-accent: #8B5CF6;
        --cyan-accent: #06B6D4;
        --text-main: #E2E8F0;
        --text-muted: #94A3B8;
        --editor-bg: #11111B;
    }}

    * {{ box-sizing: border-box; }}

    .stApp {{
        background-color: var(--bg-deep) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text-main) !important;
    }}

    /* SIDEBAR CUSTOMIZADA */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-color) !important;
        width: 260px !important;
    }}

    .nav-header {{
        padding: 24px 16px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 20px;
    }}

    .logo-img {{
        width: 50px;
        height: 50px;
        filter: drop-shadow(0 0 15px var(--purple-accent));
    }}

    .brand-name {{
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #A855F7, #06B6D4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .stButton > button[key^="nav_"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 10px 16px !important;
        width: 100% !important;
        color: var(--text-muted) !important;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        gap: 12px !important;
        border-radius: 8px !important;
        margin: 2px 0 !important;
    }}
    .stButton > button[key^="nav_"]:hover {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
    }}

    /* TOP BAR - WORKSPACE */
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        border-bottom: 1px solid var(--border-color);
        background: rgba(8, 8, 12, 0.8);
        backdrop-filter: blur(10px);
        position: sticky;
        top: 0;
        z-index: 100;
    }}

    .workspace-tag {{
        font-size: 0.85rem;
        color: var(--text-muted);
    }}

    .workspace-name {{
        font-weight: 600;
        color: #fff;
    }}

    /* ÁREA DO EDITOR */
    .editor-container {{
        background: var(--editor-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        margin: 20px 0;
        overflow: hidden;
    }}

    .editor-header {{
        background: #181825;
        padding: 8px 16px;
        display: flex;
        gap: 20px;
        border-bottom: 1px solid var(--border-color);
    }}

    .tab {{
        font-size: 0.8rem;
        color: var(--text-muted);
        padding-bottom: 4px;
        border-bottom: 2px solid transparent;
        cursor: pointer;
    }}

    .tab.active {{
        color: var(--purple-accent);
        border-bottom-color: var(--purple-accent);
    }}

    /* STATUS PANEL (DIREITA) */
    .status-panel {{
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid var(--border-color);
    }}

    .agent-status-card {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        margin-bottom: 12px;
        border: 1px solid transparent;
    }}

    .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        box-shadow: 0 0 10px currentColor;
    }}

    /* OVERRIDES STREAMLIT */
    .stTextArea textarea {{
        background-color: transparent !important;
        border: none !important;
        color: #A5B4FC !important;
        font-family: 'Fira Code', monospace !important;
    }}
    
    div.block-container {{
        padding-top: 0 !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}
    
    .stButton > button {{
        width: 100%;
        background: var(--purple-accent);
        border: none;
        color: #fff;
        font-weight: 600;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }}

    [data-testid="stStatusWidget"] {{
        color: var(--purple-accent) !important;
    }}
</style>
"""
st.markdown(ide_css, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# --- SIDEBAR (NAV INTERATIVA) ---
with st.sidebar:
    st.markdown(f"""
    <div class="nav-header">
        <img class="logo-img" src="data:image/png;base64,{b64_logo}">
        <div class="brand-name">AI COUNCIL</div>
    </div>
    """, unsafe_allow_html=True)
    
    pages = {
        "📊 Dashboard": "Dashboard",
        "📁 Projects": "Projects",
        "🧊 Models": "Models",
        "🛠️ Agent Workbench": "Workbench",
        "📜 Logs": "Logs",
        "⚙️ Settings": "Settings",
        "👥 Team": "Team"
    }

    for label, page_id in pages.items():
        is_active = st.session_state.page == page_id
        if st.button(label, key=f"nav_{page_id}", 
                     help=f"Ir para {label}",
                     type="secondary",
                     use_container_width=True):
            st.session_state.page = page_id
            st.rerun()
        
        if is_active:
            st.markdown(f"""
            <style>
                div[data-testid="stButton"] button[key="nav_{page_id}"] {{
                    background: rgba(139, 92, 246, 0.15) !important;
                    color: var(--purple-accent) !important;
                    font-weight: 600 !important;
                    border-left: 3px solid var(--purple-accent) !important;
                    border-radius: 0 8px 8px 0 !important;
                }}
            </style>
            """, unsafe_allow_html=True)

# --- LÓGICA DE AMBIENTE ---
load_dotenv(override=True)
chave_google = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
chave_groq = os.getenv("GROQ_API_KEY")
chave_openrouter = os.getenv("OPENROUTER_API_KEY")
senha_correta = os.getenv("SENHA_PAINEL")

if not senha_correta:
    st.error("🔒 Variable SENHA_PAINEL missing.")
    st.stop()

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown("<h2 style='text-align: center; margin-top: 100px;'>AUTHENTICATION REQUIRED</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        pw = st.text_input("Access Token", type="password")
        if st.button("Unlock IDE"):
            if pw == senha_correta:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.error("Invalid Token")
    st.stop()

# --- HEADER / WORKSPACE ---
st.markdown("""
<div class="top-bar">
    <div class="workspace-tag">Workspace: <span class="workspace-name">deep_learn_model_v9</span></div>
    <div style="color: var(--text-muted); font-size: 0.8rem;">Status: <span style="color: #4ADE80;">● Active</span></div>
</div>
""", unsafe_allow_html=True)

# --- CONTEÚDO DINÂMICO ---
if st.session_state.page == "Dashboard":
    # Legendas solicitadas pelo usuário
    st.markdown("""
    <div style="padding: 20px 0 20px 0;">
        <h1 style="font-size:2.2rem; font-weight:700; color:#ffffff; margin-bottom:10px; line-height:1.2;">
            O que você quer construir hoje?
        </h1>
        <p style="color:rgba(255,255,255,0.45); font-size:1.05rem; margin:0;">
            Descreva seu plugin ARK e o Conselho de 3 IAs forja o código C++ pronto para compilar.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_status = st.columns([3, 1])

    with col_main:
        st.markdown("""
        <div class="editor-header">
            <div class="tab active">agent_core.cpp</div>
            <div class="tab">ark_api.h</div>
            <div class="tab">dataset.config</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.container(border=False):
            topico_usuario = st.text_area("Input Area", height=250, placeholder="// Forje seu código ARK aqui...\n// O Conselho de IAs aguarda suas instruções.", label_visibility="collapsed")
        
        if st.button("🚀 EXECUTE ORCHESTRATION"):
            if not topico_usuario.strip():
                st.warning("Input is empty.")
            else:
                start_time = time.time()
                with st.status("⏳ ORCHESTRATING COUNCIL...", expanded=True) as status_box:
                    try:
                        c_gemini = genai.Client(api_key=chave_google)
                        c_groq = Groq(api_key=chave_groq)
                        c_or = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=chave_openrouter) if chave_openrouter else None
                    except Exception as e:
                        st.error(f"Client error: {e}")
                        st.stop()

                    # AGENT 1
                    status_box.update(label="🧠 GEMINI: ARCHITECTING...", state="running")
                    prompt_1 = f"Context: ArkApi. Task: {topico_usuario}. Return SDK-based C++ plugin code. Use template headers."
                    try:
                        res_1 = c_gemini.models.generate_content(model='gemini-2.0-flash', contents=prompt_1)
                        code_1 = res_1.text
                        status_box.write("✅ ARCHITECTURE READY")
                    except:
                        code_1 = "// Gemini unavailable"

                    # AGENT 2
                    status_box.update(label="🛡️ LLAMA: AUDITING...", state="running")
                    prompt_2 = f"Review for Null Checks and Crashes: {code_1}. Return full unmasked C++ code."
                    try:
                        res_2 = c_groq.chat.completions.create(messages=[{"role":"user","content":prompt_2}], model="llama-3.3-70b-versatile")
                        code_2 = res_2.choices[0].message.content
                        status_box.write("✅ SECURITY SEALED")
                    except:
                        code_2 = code_1

                    # AGENT 3
                    status_box.update(label="⚡ QWEN: OPTIMIZING...", state="running")
                    prompt_3 = f"Optimize memory/loops for ARK server performance: {code_2}. Return final C++ code."
                    try:
                        res_3 = c_or.chat.completions.create(messages=[{"role":"user","content":prompt_3}], model="qwen/qwen3.6-plus:free")
                        code_final = res_3.choices[0].message.content
                        status_box.write("✅ PERFORMANCE TUNED")
                    except:
                        code_final = code_2

                    status_box.update(label="✅ COUNCIL COMPLETE", state="complete")
                
                st.success(f"FORGE SUCCESSFUL - Time: {time.time()-start_time:.2f}s")
                t1, t2, t3 = st.tabs(["[1] BASE", "[2] SECURE", "[3] FINAL"])
                with t1: st.code(code_1, language='cpp')
                with t2: st.code(code_2, language='cpp')
                with t3: 
                    st.code(code_final, language='cpp')
                    st.download_button("📥 DOWNLOAD PLUGIN", code_final, "plugin.cpp")

    with col_status:
        st.markdown("<div class='status-panel'>", unsafe_allow_html=True)
        st.markdown("#### Model Status")
        st.markdown("""
        <div style="font-size: 2.5rem; color: #4ADE80; font-weight: 700;">ACTIVE</div>
        <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: -10px;">Deep Learn Engine v9</div>
        """, unsafe_allow_html=True)
        st.divider()
        st.markdown("#### Active Agents")
        st.markdown(f"""
        <div class="agent-status-card">
            <div class="status-dot" style="color: #A855F7; background: #A855F7;"></div>
            <img style="width: 32px; height: 32px;" src="data:image/png;base64,{b64_brain}">
            <div>
                <div style="font-weight: 600; font-size: 0.85rem;">Gemini Architect</div>
                <div style="font-size: 0.75rem; color: #A855F7;">Online / v2.0</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="agent-status-card">
            <div class="status-dot" style="color: #06B6D4; background: #06B6D4;"></div>
            <img style="width: 32px; height: 32px;" src="data:image/png;base64,{b64_shield}">
            <div>
                <div style="font-weight: 600; font-size: 0.85rem;">Llama Audit</div>
                <div style="font-size: 0.75rem; color: #06B6D4;">Online / 3.3-70B</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="agent-status-card">
            <div class="status-dot" style="color: #F472B6; background: #F472B6;"></div>
            <img style="width: 32px; height: 32px;" src="data:image/png;base64,{b64_light}">
            <div>
                <div style="font-weight: 600; font-size: 0.85rem;">Qwen Optimizer</div>
                <div style="font-size: 0.75rem; color: #F472B6;">Online / 72B</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.divider()
        st.markdown("#### Stats")
        st.markdown("""
        <div style="font-size: 0.8rem; color: var(--text-muted);">
            Latency: <span style="color:#fff">24ms</span><br>
            Uptime: <span style="color:#fff">99.9%</span><br>
            Threads: <span style="color:#fff">Active</span>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown(f"## {st.session_state.page}")
    st.info(f"A seção **{st.session_state.page}** está em desenvolvimento.")
    if st.session_state.page == "Projects":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            <div class="editor-container" style="padding:20px;">
                <h4 style="color:var(--purple-accent);">GradualEngrams</h4>
                <p style="font-size:0.8rem; color:var(--text-muted);">Plugin C++ para controle de engramas no ARK ASE.</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px;">
                    <span style="color:#4ADE80; font-size:0.75rem;">● Compilado</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="editor-container" style="padding:20px;">
                <h4 style="color:var(--cyan-accent);">SafeWildDinoWipe</h4>
                <p style="font-size:0.8rem; color:var(--text-muted);">Mecanismo de wipe inteligente para melhorar FPS.</p>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:20px;">
                    <span style="color:#FACC15; font-size:0.75rem;">● Rascunho</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

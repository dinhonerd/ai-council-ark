import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from google import genai

# Configuração da página e logo
st.set_page_config(
    page_title="AI Council - Arquitetura C++",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS Cyberpunk / Glassmorphism
custom_css = """
<style>
    /* Fundo Principal e Painel de Vidro Translúcido */
    .stApp {
        background-color: #03040c;
        color: #e0f8ff;
    }
    
    /* Corpo principal (Flutuando sobre o T-Rex) */
    div.block-container {
        background-color: rgba(4, 6, 15, 0.88);
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.1);
        backdrop-filter: blur(4px);
    }
    
    /* Inputs text-area */
    .stTextArea textarea {
        background-color: rgba(6, 11, 25, 0.85) !important;
        color: #00f3ff !important;
        border: 2px solid #ff00ff !important;
        border-radius: 12px !important;
        font-family: 'Consolas', 'Courier New', monospace;
        box-shadow: 0 0 10px rgba(255, 0, 255, 0.4), inset 0 0 10px rgba(255, 0, 255, 0.2) !important;
    }
    .stTextArea textarea:focus {
        border-color: #00f3ff !important;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.8), inset 0 0 15px rgba(0, 243, 255, 0.4) !important;
    }
    
    /* Botoes Primários Neonexis */
    div.stButton > button:first-child {
        background: transparent !important;
        color: #00f3ff !important;
        border: 2px solid #00f3ff !important;
        border-radius: 30px;
        padding: 0.6rem 2.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.5), inset 0 0 10px rgba(0, 243, 255, 0.3);
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background: #00f3ff !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(0, 243, 255, 0.9), inset 0 0 20px rgba(0, 243, 255, 0.6);
        transform: scale(1.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(3, 4, 12, 0.95) !important;
        border-right: 2px solid #ff00ff;
        box-shadow: 5px 0 25px rgba(255, 0, 255, 0.3);
    }
    
    /* Headings (Brilho no Texto) */
    h1, h2, h3 {
        color: #00f3ff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 0 10px rgba(0, 243, 255, 0.7), 0 0 20px rgba(0, 243, 255, 0.4) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    h3 {
        color: #ff00ff !important;
        text-shadow: 0 0 10px rgba(255, 0, 255, 0.7), 0 0 20px rgba(255, 0, 255, 0.4) !important;
    }
    
    /* Expander / Containers (As Caixas de IA) */
    div[data-testid="stVerticalBlock"] > div > div > div {
        border-color: rgba(0, 243, 255, 0.4) !important;
    }
    
    /* Ajuste de botoes nativos (Download) */
    .stDownloadButton > button {
        background-color: transparent !important;
        color: #ff00ff !important;
        border: 1px solid #ff00ff !important;
        border-radius: 8px;
        box-shadow: 0 0 8px rgba(255, 0, 255, 0.3);
    }
    .stDownloadButton > button:hover {
        background-color: #ff00ff !important;
        color: black !important;
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.8);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Lógica Dinâmica de Imagem ou Vídeo de Fundo
bg_media = ""
if os.path.exists("fundo.mp4"):
    with open("fundo.mp4", "rb") as f:
        video_data = f.read()
    b64_video = base64.b64encode(video_data).decode()
    bg_media = f"""
    <style>
    /* Removemos a cor e o grid do app inteiro para o video aparecer atrás! */
    .stApp {{
        background-color: transparent !important;
        background-image: none !important;
    }}
    </style>
    <video autoplay loop muted playsinline style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; object-fit: cover; z-index: -1;">
        <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
    </video>
    """
    st.markdown(bg_media, unsafe_allow_html=True)
elif os.path.exists("fundo.jpg"):
    with open("fundo.jpg", "rb") as f:
        img_data = f.read()
    b64_fundo = base64.b64encode(img_data).decode()
    bg_media = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64_fundo}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_media, unsafe_allow_html=True)

# Carrega ambiente
load_dotenv()
chave_google = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
chave_groq = os.getenv("GROQ_API_KEY")

with st.sidebar:
    st.markdown("# 🧠 AI Council")
    st.title("Status do Conselho")
    st.markdown("Bem-vindo ao **Painel de Modding Ark C++**.")
    st.markdown("---")
    if not chave_google or not chave_groq or chave_google == "sua_chave_do_google_aqui":
        st.error("⚠️ Chaves de API ausentes!")
    else:
        st.success("✔️ APIs Online")
    
    st.markdown("---")
    st.caption("Configurações Carregadas")

st.title("🧠 Conselho Mult-Agente: ArkApi")
st.markdown("Cole o seu relatório do Codex abaixo e deixe o Arquiteto e o Revisor de Segurança trabalharem lado a lado.")

if not chave_google or not chave_groq or chave_google == "sua_chave_do_google_aqui":
    st.stop()

topico_usuario = st.text_area("📝 Área de Relatório / Desafio C++:", height=150, placeholder="Cole o código crítico ou a missão gigante aqui...")

# Botão enviar
if st.button("🚀 Iniciar Orquestração do Conselho", type="primary"):
    if not topico_usuario.strip():
        st.warning("O relatório está vazio!")
        st.stop()
        
    try:
        client_gemini = genai.Client(api_key=chave_google)
        client_groq = Groq(api_key=chave_groq)
    except Exception as e:
        st.error(f"Erro ao conectar clientes de IA: {e}")
        st.stop()

    # Cria contêineres de status
    status_box = st.status("🔮 Estabelecendo link neural com o Conselho...", expanded=True)
    
    # -----------------------------
    # 1. Leitura do SDK
    # -----------------------------
    status_box.update(label="📂 Injetando SDK da ArkApi...", state="running")
    sdk_base_path = "sdk_files" if os.path.exists("sdk_files/Inventory.h") else "."
    sdk_conteudo = ""
    arquivos_alvo = ["Inventory.h"]
    
    if os.path.exists(sdk_base_path):
        for arquivo in arquivos_alvo:
            caminho = os.path.join(sdk_base_path, arquivo)
            if os.path.exists(caminho):
                with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                    sdk_conteudo += f"\n\n--- INÍCIO DO ARQUIVO {arquivo} ---\n"
                    sdk_conteudo += f.read()
        status_box.write(f"✔️ **SDK Reconhecido**: Lidos {len(sdk_conteudo)} bytes na memória temporal.")
    else:
        status_box.write("⚠️ Pasta do SDK nativo não localizada. Operando sem contexto adicional.")

    # -----------------------------
    # 2. Agente 1 (Gemini)
    # -----------------------------
    status_box.update(label="🧠 Gemini (Arquiteto Sênior) está rascunhando a solução...", state="running")
    prompt_programador = f"""
    Você é um Arquiteto Sênior de C++ focado em plugins para o jogo ARK: Survival Evolved (ArkApi).
    Escreva um código robusto, formatado e pronto para compilar para a seguinte tarefa do usuário.
    NÃO invente funções que não existam no motor.
    
    <SDK_CONTEXT_LOCAL>
    Aqui estão os headers reais extraídos da máquina do usuário agora:
    {sdk_conteudo}
    </SDK_CONTEXT_LOCAL>

    TAREFA DO USUÁRIO: {topico_usuario}
    """

    modelos_tentativa = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-pro', 'gemini-1.5-pro-latest']
    codigo_gemini = None
    erro_log = ""
    
    for modelo in modelos_tentativa:
        try:
            resp_gemini = client_gemini.models.generate_content(
                model=modelo,
                contents=prompt_programador
            )
            codigo_gemini = resp_gemini.text
            status_box.write(f"✔️ **Arquiteto:** Rascunho finalizado via `{modelo}`.")
            break
        except Exception as e:
            msg = f"Rejeito do {modelo}: {e}"
            erro_log += msg + "\n"
            continue

    if not codigo_gemini:
        status_box.update(label="Falha de Comunicação Neural", state="error")
        st.error(f"❌ Gemini falhou. Logs da rejeição:\n\n{erro_log}")
        st.stop()
        
    # -----------------------------
    # 3. Agente 2 (Llama)
    # -----------------------------
    status_box.update(label="🛡️ Llama 3 (Eng. de Segurança) auditando vulnerabilidades...", state="running")
    
    prompt_revisor = f"""
    Você é um Engenheiro Sênior de Segurança de Servidores e C++ Crítico.
    O Arquiteto enviou o seguinte código/análise:
    
    ```cpp
    {codigo_gemini}
    ```
    
    Sua missão: 
    1. Julgue a solução técnica apontada por ele para a Barreira (O que ele sugeriu no lugar de AddItemByClass). Faz sentido para a Unreal Engine / ArkApi?
    2. Revise o código procurando vulnerabilidades de (Null Pointers) em `AActor`, `UPrimalItem` ou `AShooterPlayerController`.
    3. ESCREVA O CÓDIGO CORRIGIDO. NUNCA DEIXE CÓDIGOS PELA METADE COM "//..." (Sem preguiça!). Se não couber tente ao menos entregar a função corrigida completa.
    """

    codigo_final = ""
    try:
        resp_groq = client_groq.chat.completions.create(
            messages=[{"role": "user", "content": prompt_revisor}],
            model="llama-3.3-70b-versatile",
            temperature=0.2,
        )
        codigo_final = resp_groq.choices[0].message.content
        status_box.write("✔️ **Revisor:** Código selado. Auditoria finalizada.")
    except Exception as e:
        status_box.write(f"⚠️ Erro no servidor da Groq: {e}\nLimite atingido ou indisponível.")

    status_box.update(label="✅ Orquestração Concluída!", state="complete")
    st.divider()
    
    # -----------------------------
    # Exibição em Duas Colunas
    # -----------------------------
    st.subheader("📊 Painel de Verificação Lado a Lado")
    
    col_arq, col_rev = st.columns(2)
    
    with col_arq:
        st.markdown("### 💡 1. Arquiteto Sênior (Gemini)")
        st.info("Planta arquitetural pura gerada no motor base.")
        # Botão rápido de cópia + Download!
        st.download_button("📥 Baixar Log do Arquiteto (.md)", data=codigo_gemini, file_name="Arquiteto_Log.md", use_container_width=True)
        with st.container(height=800, border=True):
            st.markdown(codigo_gemini)
            
    with col_rev:
        st.markdown("### 🏆 2. Código Aprovado (Llama 3)")
        if codigo_final:
            st.success("Revisão de Segurança, Patchs anti-nulo e Código Final.")
            # Botão rápido de cópia + Download!
            st.download_button("📥 Baixar Código Final (.cpp)", data=codigo_final, file_name="Codigo_Final.cpp", use_container_width=True)
            with st.container(height=800, border=True):
                st.code(codigo_final, language='cpp') # Adiciona o bloco com botão 'Copy' no canto superior direito nativo!
                st.markdown("---")
                st.markdown("*(Fique à vontade para clicar no botão Copy no canto da caixa preta acima ou usar o botão de Download!)*")
        else:
            st.warning("⚠️ Llama 3 indisponível. Utilize o código original do Arquiteto.")

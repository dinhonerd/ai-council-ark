import os
import base64
import streamlit as st
import streamlit.components.v1 as components
import time
from dotenv import load_dotenv
from groq import Groq
from google import genai
import openai # Para o OpenRouter

# Configuração da página e logo
st.set_page_config(
    page_title="AI Council - Arquitetura C++",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS AgentGPT - Purple Glassmorphism
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    /* Reset e Fundo Radial Roxo */
    * { box-sizing: border-box; }
    .stApp {
        background: radial-gradient(circle at top, #3b0764, #020617) !important;
        font-family: 'Inter', Arial, sans-serif !important;
        color: #fff !important;
    }

    /* Header transparente */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Corpo Principal */
    div.block-container, [data-testid="stAppViewBlockContainer"] {
        background: transparent !important;
        padding-top: 1.5rem !important;
    }

    /* SIDEBAR - Glassmorphism Escuro */
    [data-testid="stSidebar"] {
        background: rgba(0,0,0,0.45) !important;
        border-right: 1px solid rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(20px) !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2d9f3 !important;
    }

    /* HEADINGS */
    h1, h2, h3 {
        color: #fff !important;
        font-weight: 900 !important;
        text-shadow: none !important;
        text-transform: none !important;
        font-family: 'Inter', Arial, sans-serif !important;
        letter-spacing: -0.5px;
    }
    h1 { font-size: 2rem !important; }

    /* TEXT INPUT e TEXTAREA */
    .stTextArea textarea, .stTextInput input {
        background: rgba(2, 6, 23, 0.7) !important;
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        font-family: 'Inter', Arial, sans-serif !important;
        backdrop-filter: blur(10px);
        transition: border 0.3s !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #7c3aed !important;
        box-shadow: 0 0 20px rgba(124,58,237,0.5) !important;
    }

    /* BOTÃO PRINCIPAL */
    div.stButton > button:first-child {
        background: #7c3aed !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 700 !important;
        font-family: 'Inter', Arial, sans-serif !important;
        letter-spacing: 0.3px !important;
        text-transform: none !important;
        box-shadow: 0 0 20px rgba(124,58,237,0.5) !important;
        transition: all 0.3s !important;
    }
    div.stButton > button:first-child:hover {
        background: #6d28d9 !important;
        box-shadow: 0 0 35px rgba(124,58,237,0.9) !important;
        transform: translateY(-2px) !important;
    }

    /* CARDS / CONTAINERS */
    [data-testid="stExpander"],
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s !important;
    }

    /* Tabs */
    [data-testid="stTabs"] button {
        color: rgba(255,255,255,0.6) !important;
        font-family: 'Inter', Arial, sans-serif !important;
        font-weight: 600 !important;
        border-bottom: 2px solid transparent !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #a855f7 !important;
        border-bottom: 2px solid #a855f7 !important;
    }

    /* SUCCESS / INFO / ERROR */
    .stSuccess {
        background: rgba(74,222,128,0.1) !important;
        border-left: 3px solid #4ade80 !important;
        border-radius: 8px !important;
    }
    .stError {
        background: rgba(239,68,68,0.1) !important;
        border-left: 3px solid #ef4444 !important;
        border-radius: 8px !important;
    }
    .stInfo {
        background: rgba(124,58,237,0.15) !important;
        border-left: 3px solid #7c3aed !important;
        border-radius: 8px !important;
    }

    /* DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background: rgba(124,58,237,0.2) !important;
        color: #c4b5fd !important;
        border: 1px solid #7c3aed !important;
        border-radius: 8px !important;
        transition: all 0.3s !important;
    }
    .stDownloadButton > button:hover {
        background: #7c3aed !important;
        color: #fff !important;
    }

    /* CODE BLOCKS */
    code, pre {
        background: rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(124,58,237,0.3) !important;
        border-radius: 8px !important;
        color: #c4b5fd !important;
    }

    /* SPINNER / STATUS */
    [data-testid="stStatusWidget"] {
        color: #a855f7 !important;
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
    /* Subscrita do Loading (Bicicleta) no Topo Direito pelo Dino Neon */
    [data-testid="stStatusWidget"] svg {{
        display: none !important;
    }}
    [data-testid="stStatusWidget"] {{
        background-image: url("https://c.tenor.com/_q_k94sP7j0AAAAd/dino-run-t-rex.gif") !important;
        background-size: contain !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        width: 45px !important;
        height: 45px !important;
        filter: invert(1) hue-rotate(180deg) drop-shadow(0 0 5px #0ff) !important;
        mix-blend-mode: screen !important;
        margin-top: -5px;
    }}
    
    .stApp > header {{
        background-color: transparent;
    }}!important;
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
load_dotenv(override=True)
chave_google = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
chave_groq = os.getenv("GROQ_API_KEY")
chave_openrouter = os.getenv("OPENROUTER_API_KEY")
senha_correta = os.getenv("SENHA_PAINEL") # Vazia por padrão para não vazar no Git!

if not senha_correta:
    st.error("⚠️ **Pausa de Segurança:** A variável `SENHA_PAINEL` não foi detectada.")
    st.warning("Configure essa chave no Gerenciador de Secrets do seu Streamlit ou no arquivo `.env` local para trancar o seu aplicativo e ele voltará a funcionar!")
    st.stop()

# SISTEMA DE SEGURANÇA (LOGIN)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown("## 🔒 Acesso Restrito")
    st.info("Este painel consome cotas de IA privadas. Identifique-se para acessar o Conselho.")
    senha_digitada = st.text_input("Senha de Acesso", type="password")
    if st.button("Desbloquear Painel"):
        if senha_digitada == senha_correta:
            st.session_state["autenticado"] = True
            st.rerun() # Recarrega a página autenticado
        else:
            st.error("❌ Senha Incorreta!")
    # Trava o app aqui se não estiver autenticado
    st.stop()

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
        st.warning("⚠️ Insira o problema do Codex acima para o Arquiteto trabalhar!")
        st.stop()

    # HUD de Cronômetro (Formato HH:MM:SS) Centralizado e Menor
    start_time_total = time.time()
    dino_placeholder = st.empty()
    
    html_dino = """
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Courier New', monospace; color: #0ff; margin-top: 10px;">
        <h5 style="margin-bottom: 5px; font-weight: bold; text-shadow: 0px 0px 8px #0ff; animation: pulse 1s infinite alternate;">FORJANDO OS CÓDIGOS DA ARKAPI...</h5>
        <div style="font-size: 32px; font-weight: bold; text-shadow: 0px 0px 10px #e024c3; color: #fff; border: 1px solid #0ff; padding: 5px 20px; border-radius: 10px; background: rgba(0,0,0,0.5);" id="cronometro">00:00.000</div>
    </div>
    <style>@keyframes pulse { from { opacity: 0.6; } to { opacity: 1; } }</style>
    <script>
        let inicio = Date.now();
        setInterval(function() {
            let ts = Date.now() - inicio;
            let m = Math.floor(ts / 60000).toString().padStart(2, '0');
            let s = Math.floor((ts % 60000) / 1000).toString().padStart(2, '0');
            let ms = (ts % 1000).toString().padStart(3, '0');
            document.getElementById('cronometro').innerText = m + ":" + s + "." + ms;
        }, 47);
    </script>
    """
    
    with dino_placeholder:
        components.html(html_dino, height=120)

    with st.status("⏳ Preparando o ambiente Multi-Agente...", expanded=True) as status_box:
        try:
            client_gemini = genai.Client(api_key=chave_google)
            client_groq = Groq(api_key=chave_groq)
            if chave_openrouter and chave_openrouter != "cole_sua_chave_aqui":
                client_or = openai.OpenAI(base_url="https://openrouter.ai/api/v1", api_key=chave_openrouter)
            else:
                client_or = None
        except Exception as e:
            st.error(f"Erro ao conectar clientes de IA: {e}")
            st.stop()

        # -----------------------------
        # 1. Leitura do SDK (Otimizada por Cota)
        # -----------------------------
        status_box.update(label="📂 Extraindo essência do SDK ArkApi...", state="running")
        sdk_base_path = os.path.join(os.path.dirname(__file__), "sdk_ark")
        sdk_conteudo = ""
        # Colocamos os mais importantes por primeiro
        arquivos_alvo = ["Inventory.h", "Actor.h", "GameMode.h", "PrimalStructure.h"]
        
        tamanho_total_lido = 0
        LIMITE_MAXIMO_BYTES = 700000  # ~700KB (Abaixo dos 250k Tokens da Cota Grátis)
        
        if os.path.exists(sdk_base_path):
            for arquivo in arquivos_alvo:
                if tamanho_total_lido >= LIMITE_MAXIMO_BYTES:
                    break
                    
                caminho = os.path.join(sdk_base_path, arquivo)
                if os.path.exists(caminho):
                    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                        conteudo = f.read()
                        
                        # Compressão: Remove linhas vazias e de comentários para economizar Tokens
                        linhas_limpas = [l.strip() for l in conteudo.split('\n') if l.strip() and not l.strip().startswith('//')]
                        conteudo_comprimido = '\n'.join(linhas_limpas)
                        
                        espaco_restante = LIMITE_MAXIMO_BYTES - tamanho_total_lido
                        if len(conteudo_comprimido) > espaco_restante:
                            conteudo_comprimido = conteudo_comprimido[:espaco_restante] + "\n/* [TRUNCADO PELO LIMITE DE COTA] */"
                            
                        sdk_conteudo += f"\n\n--- INÍCIO DO ARQUIVO {arquivo} ---\n" + conteudo_comprimido
                        tamanho_total_lido += len(conteudo_comprimido)
            
            kb_lidos = tamanho_total_lido / 1024
            status_box.write(f"✔️ **SDK Injetado**: {kb_lidos:.1f} KB comprimidos e alocados (Blindagem Anti-Cota em ação).")
        else:
            status_box.write("⚠️ Cofre Fonte da AseApi não carregado. Operando com instintos básicos.")

        # -----------------------------
        # 2. Agente 1 (Gemini)
        # -----------------------------
        status_box.update(label="🧠 Gemini (Arquiteto Sênior) está rascunhando a solução...", state="running")
        
        template_base = """// ==== ESTRUTURA OBRIGATÓRIA ARKAPI ====
#include <API/ARK/Ark.h>
#include <Logger/Logger.h>
// Inclusões adicionais aqui

void Load() {
    Log::Get().Init("MeuPluginArk");
    // Registro de Hooks e Comandos de Chat:
    // ArkApi::GetHooks().SetHook(...)
    // ArkApi::GetCommands().AddChatCommand(...)
}

void Unload() {
    // Remoção
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH: Load(); break;
    case DLL_PROCESS_DETACH: Unload(); break;
    }
    return TRUE;
}
"""

        prompt_programador = f"""
        Você é um Arquiteto Sênior de C++ focado estritamente na ArkServerApi (BeyondApi) para ARK: Survival Evolved.
        
        O grande erro das IAs é gerar código puro de "Unreal Engine Genérico". Suas soluções falham no servidor se não usarem a infraestrutura de plugins DLL da ArkApi.
        Você DEVE OBRIGATORIAMENTE usar o template abaixo como a espinha dorsal infinita do seu resultado:
        
        ```cpp
        {template_base}
        ```
        
        REGRAS ABSOLUTAS DA ARKAPI:
        1. Para Hooks (Interceptações): Use `DECLARE_HOOK(Classe_Metodo, Retorno, Classe*, Args);`.
        2. Toda a lógica de inicialização vai OBRIGATORIAMENTE no void Load().
        3. Nunca construa funções que precisem ser chamadas pelo console de Blueprint. Tudo opera via `ArkApi::GetCommands().AddChatCommand` ou `AddConsoleCommand`.
        
        <SDK_CONTEXT_LOCAL>
        Headers extraídos para auxílio em funções de itens e jogadores:
        {sdk_conteudo}
        </SDK_CONTEXT_LOCAL>

        TAREFA DO USUÁRIO: {topico_usuario}
        Retorne a solução completa, programada de dentro da DllMain e arquivos de hook. E use blocos markdown ` ```cpp ` para o código.
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
            dino_placeholder.empty()
            st.error(f"❌ Gemini falhou em todas as tentativas. Expanda a caixa acima ou leia o log aqui:\n\n{erro_log}")
            st.stop()
            
        # -----------------------------
        # 3. Agente 2 (Llama)
        # -----------------------------
        status_box.update(label="🛡️ Llama 3 (Eng. de Segurança) auditando vulnerabilidades...", state="running")
        
        prompt_revisor = f"""
        Você é o Engenheiro Chefe de Segurança e Integridade do código C++ para Servidores ARK.
        O Arquiteto gerou o esqueleto da ArkApi abaixo:
        
        ```cpp
        {codigo_gemini}
        ```
        
        Sua missão: 
        1. OBRIGATÓRIO: Verifique se a estrutura base (Load, Unload, DllMain) foi mantida! Se o arquiteto removeu, recoloque Imediatamente!
        2. Analise severamente todas as pontes de memória: Null Check (if (!player) return;) é estrito antes de usar qualquer método em `AShooterPlayerController` ou `UPrimalItem`. O servidor dá Crash no banco de dados se não houver Null Check.
        3. Valide o método de spawn e strings (`FString`).
        4. OBRIGATÓRIO: Forneça DE VOLTA o código compilável completo em C++ pronto para o usuário copiar/colar na íntegra. Não deixe partes "// ...resto fica igual", escreva o arquivo unificado inteiro atualizado e bloqueado com Anti-Null.
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

        # -----------------------------
        # 4. Agente 3 (Qwen 72B - OpenRouter)
        # -----------------------------
        status_box.update(label="⚙️ Qwen 72B (Eng. de Performance) reduzindo carga do servidor...", state="running")
        
        prompt_otimizador = f"""
        Você é um Engenheiro Sênior C++ Fanático por Eficiência focado no kernel de Servidores Game (ArkApi).
        O código seguro foi fornecido pela engenharia:
        
        ```cpp
        {codigo_final if codigo_final else codigo_gemini}
        ```
        
        Sua ÚNICA missão (sem alterar a DllMain e o comportamento em si):
        1. Refatorar loops e eliminar passagens pesadas na cópia de variáveis (substitua chamadas cópias enormes de `FString` ou vetores por cópias por referência `const TArray<>&` ou Strings decodificadas rápidas).
        2. Garanta a máxima enxugada térmica no processo base.
        3. RETORNE O CÓDIGO FONTE 100% UNIFICADO. O usuário é leigo, não retorne apenas a função modificada, retorne todo o arquivo `.cpp` limpo e brilhante incluindo o `#include` e `DllMain` já ajustado pela performance, para ele realizar Copiar/Colar e ir jogar.
        """

        codigo_otimizado = ""
        erro_or = ""
        modelos_otimizacao = [
            'meta-llama/llama-3.3-70b-instruct:free', 
            'nousresearch/hermes-3-llama-3.1-405b:free',
            'qwen/qwen3.6-plus:free'
        ]

        if client_or:
            for modelo_ativo in modelos_otimizacao:
                try:
                    resp_or = client_or.chat.completions.create(
                        messages=[{"role": "user", "content": prompt_otimizador}],
                        model=modelo_ativo,
                        temperature=0.1,
                    )
                    codigo_otimizado = resp_or.choices[0].message.content
                    status_box.write(f"✅ **Otimizador:** Custo de Processamento Enxuto. Ferreiro ativo: `{modelo_ativo}`.")
                    break
                except Exception as e:
                    erro_or += f"Tentativa {modelo_ativo} falhou: {str(e)}\n"
                    continue
            
            if not codigo_otimizado:
                status_box.write("⚠️ Todos os motores de Otimização falharam por congestionamento.")
        else:
            erro_or = "Chave do OpenRouter ausente no .env"
            status_box.write("⚠️ Chave do OpenRouter ausente no .env")

        # Atualiza o status box E GERA UM RELOAD nele via manager que evita que ele fique girando!
        status_box.update(label="✅ Orquestração Concluída!", state="complete")
    
    # Destrói o hud de carregamento e mostra o botão final de tempo
    dino_placeholder.empty()
    tempo_gasto = time.time() - start_time_total
    
    mins = int(tempo_gasto // 60)
    secs = int(tempo_gasto % 60)
    milis = int((tempo_gasto % 1) * 1000)
    st.success(f"🏁 **Missão Completa!** Tempo recorde de forja pelo Conselho: **{mins:02d}:{secs:02d}.{milis:03d}**")

    st.divider()
    
    # -----------------------------
    # Exibição em Abas Separadas (Tabs)
    # -----------------------------
    st.subheader("👁️ Painel de Verificação do Conselho")
    st.info("💡 **Dica:** Clique nas abas abaixo para navegar entre as soluções dos diferentes agentes Especialistas em C++ da ArkApi!")
    
    tab1, tab2, tab3 = st.tabs([
        "🧠 1. Arquiteto (Gemini)", 
        "🛡️ 2. Eng. de Segurança (Llama)", 
        "⚡ 3. Otimizador de Desempenho (Qwen 72B)"
    ])
    
    # --- ABA 1 ---
    with tab1:
        st.markdown("### 🧠 Arquiteto Sênior (Gemini-Flash)")
        st.info("Planta arquitetural pura gerada direto no motor base da ArkApi.")
        st.download_button("📥 Baixar Base (.md)", data=codigo_gemini, file_name="Arquiteto_Log.md", use_container_width=True)
        with st.container(height=700, border=True):
            st.markdown(codigo_gemini)
            
    # --- ABA 2 ---
    with tab2:
        st.markdown("### 🛡️ Código Seguro (Llama 3.3)")
        if codigo_final:
            st.success("Revisão de Segurança: Patchs anti-nulo e controle de vazamentos de memória (Ponteiros).")
            st.download_button("📥 Baixar Código de Segurança (.cpp)", data=codigo_final, file_name="Codigo_Seguro.cpp", use_container_width=True)
            with st.container(height=700, border=True):
                st.code(codigo_final, language='cpp', wrap_lines=True)
        else:
            st.warning("⚠️ Llama 3 indisponível ou falhou ao analisar.")

    # --- ABA 3 ---
    with tab3:
        st.markdown("### ⚡ Código de Alta Performance (Rede OpenRouter)")
        if codigo_otimizado:
            st.success("Refatoração Otimizada: Este agente monstro pescou os códigos seguros e lapidou tudo para a menor carga térmica na CPU.")
            st.download_button("📥 Baixar Código Final Otimizado (.cpp)", data=codigo_otimizado, file_name="Codigo_Otimizado_Tuning.cpp", use_container_width=True)
            with st.container(height=700, border=True):
                st.code(codigo_otimizado, language='cpp', wrap_lines=True)
        else:
            st.warning(f"⚠️ Todos os canais Congestionados no momento. Logs:\n{erro_or}")
            

    st.divider()
    
    # -----------------------------
    # Botão de Reset do Painel
    # -----------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Painel de Comandos", use_container_width=True):
        st.rerun()

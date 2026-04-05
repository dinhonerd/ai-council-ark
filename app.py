import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from google import genai

# Configuração da página e logo
st.set_page_config(
    page_title="AI Council - Arquitetura C++",
    page_icon="🤖",
    layout="wide"
)

# Carrega ambiente
load_dotenv()
chave_google = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
chave_groq = os.getenv("GROQ_API_KEY")

st.title("🤖 Conselho de IAs - Modding Ark C++")
st.markdown("Seja bem-vindo ao painel gráfico do Conselho de IAs. Cole o seu relatório do Codex abaixo e os modelos vão trabalhar lado a lado.")

if not chave_google or not chave_groq or chave_google == "sua_chave_do_google_aqui":
    st.error("Chaves de API ausentes! Verifique o arquivo .env.")
    st.stop()

topico_usuario = st.text_area("📝 Relatório / Problema C++:", height=300, placeholder="Cole o Relatório Técnico Gigante aqui...")

if st.button("🚀 Submeter ao Conselho de IA", type="primary"):
    if not topico_usuario.strip():
        st.warning("O relatório está vazio!")
        st.stop()
        
    try:
        client_gemini = genai.Client(api_key=chave_google)
        client_groq = Groq(api_key=chave_groq)
    except Exception as e:
        st.error(f"Erro ao conectar clientes de IA: {e}")
        st.stop()

    # Cria contêineres de status e logs
    status_box = st.status("Preparando fluxo do Conselho...", expanded=True)
    
    # -----------------------------
    # 1. Leitura do SDK
    # -----------------------------
    status_box.update(label="📂 Buscando motor ArkApi...", state="running")
    # O caminho agr é super flexível: procura na pasta e também "solto" do lado dele.
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
        status_box.write(f"✔️ **SDK Injetado**: Lidos {len(sdk_conteudo)} caracteres (Limitado apenas a Inventory.h p/ poupar cota).")
    else:
        status_box.write("⚠️ Pasta do SDK não encontrada, usando memória nativa da IA.")

    # -----------------------------
    # 2. Agente 1 (Gemini)
    # -----------------------------
    status_box.update(label="🧠 Arquiteto Sênior (Gemini) está pensando e decodificando SDK...", state="running")
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
            status_box.write(f"🟢 **O Arquiteto** entregou a arquitetura principal usando o `{modelo}`!")
            break
        except Exception as e:
            msg = f"Rejeitado: modelo '{modelo}'. Motivo: {e}"
            erro_log += msg + "\n"
            status_box.write(f"⚠️ {msg}")
            continue

    if not codigo_gemini:
        status_box.update(label="Falha Crítica no Gemini", state="error")
        st.error(f"❌ Sua nova chave do Google falhou em todos os modelos permitidos. Motivos do bloqueio:\n\n{erro_log}")
        st.stop()
        
    st.markdown("### 💡 Arquitetura e Código (Gemini)")
    # Opcional exibir na tela para revisão, pois markdown dá destaque visual a C++
    with st.expander("Ver Reposta Original do Gemini", expanded=True):
        st.markdown(codigo_gemini)
        
    # -----------------------------
    # 3. Agente 2 (Llama)
    # -----------------------------
    status_box.update(label="🕵️ Llama 3 (Engenheiro Revisor) está criticando vulnerabilidades...", state="running")
    
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
        status_box.write("🟢 **O Revisor** finalizou a etapa de segurança!")
    except Exception as e:
        status_box.write(f"🔴 Erro na etapa de revisão da Groq: {e}\nMuitos tokens pro plano grátis?")

    status_box.update(label="✅ Orquestração finalizada com Sucesso!", state="complete")
    
    if codigo_final:
        st.divider()
        st.header("🏆 RESULTADO FINAL APROVADO PELO Llama 3:")
        st.markdown(codigo_final)
    else:
        st.info("A API da Groq sofreu um erro ou excedeu a cota, mas fique tranquilo, você pode seguir a arquitetura do Gemini Logo acima!")

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime
from typing import List, Dict

# Carregar variáveis do .env
load_dotenv()

# Configuração das APIs
serpapi_key = os.getenv("SERPAPI_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Inicializar clientes
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
else:
    groq_client = None

if openai_api_key:
    from openai import OpenAI
    openai_client = OpenAI(api_key=openai_api_key)
else:
    openai_client = None

# Configuração da página
st.set_page_config(
    page_title="🔍 Motor de Busca Inteligente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .search-result {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
    }
    .source-link {
        background: #f0f2f6;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    .groq-badge {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Interface principal
st.markdown("""
<div class="main-header">
    <h1>🔍 Motor de Busca Inteligente</h1>
    <p>Busque qualquer tema e receba um resumo detalhado com IA</p>
    <span class="groq-badge">🆕 OpenAI OSS 120B + GroqCloud</span>
</div>
""", unsafe_allow_html=True)

# Sidebar com configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Botões de controle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpar Cache", help="Limpa todos os dados em cache"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Cache limpo!")
    
    with col2:
        if st.button("🔄 Resetar App", help="Reseta completamente a aplicação"):
            st.cache_data.clear()
            st.cache_resource.clear()
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("App resetado!")
            st.rerun()
    
    # Verificar status das APIs
    st.subheader("Status das APIs")
    if serpapi_key:
        st.success("✅ SerpAPI configurada")
    else:
        st.error("❌ SerpAPI não configurada")
    
    if groq_api_key:
        st.success("✅ GroqCloud configurada")
    else:
        st.error("❌ GroqCloud não configurada")
        
    if openai_api_key:
        st.success("✅ OpenAI configurada")
    else:
        st.error("❌ OpenAI não configurada")
    
    # Configurações de busca
    st.subheader("Configurações de Busca")
    num_results = st.slider("Número de resultados", 3, 20, 10)
    language = st.selectbox("Idioma", ["pt", "en", "es"], index=0)
    country = st.selectbox("País", ["br", "us", "es", "global"], index=0)
    
    # Configurações do modelo
    st.subheader("Configurações da IA")
    
    # Seletor de provedor
    ai_provider = st.selectbox(
        "Provedor de IA",
        ["GroqCloud", "OpenAI"],
        index=0,
        help="Escolha entre GroqCloud (rápido) ou OpenAI (modelos o1)"
    )
    
    if ai_provider == "OpenAI":
        model_choice = st.selectbox(
            "Modelo OpenAI", 
            [
                "o1",                           # Novo modelo o1 (120B equivalente)
                "o1-preview",                   # o1-preview (reasoning)
                "o1-mini",                      # o1-mini (mais rápido)
                "gpt-4o",                       # GPT-4o mais recente
                "gpt-4o-mini",                  # GPT-4o mini
                "gpt-3.5-turbo"                 # Clássico
            ],
            index=0,
            help="Modelos OpenAI - o1 é o mais avançado (reasoning)"
        )
        
        # Informações sobre modelos OpenAI
        openai_info = {
            "o1": "🧠 OpenAI o1 - Reasoning avançado, modelo mais inteligente",
            "o1-preview": "🔬 o1-preview - Versão de desenvolvimento do o1", 
            "o1-mini": "⚡ o1-mini - Reasoning rápido e eficiente",
            "gpt-4o": "🚀 GPT-4o - Multimodal e versátil",
            "gpt-4o-mini": "💨 GPT-4o mini - Rápido e econômico",
            "gpt-3.5-turbo": "📝 GPT-3.5 - Clássico e confiável"
        }
        st.info(openai_info.get(model_choice, "Modelo selecionado"))
        
    else:  # GroqCloud
        model_choice = st.selectbox(
            "Modelo GroqCloud", 
            [
                "openai/gpt-oss-120b",         # 🆕 OpenAI OSS 120B (flagship)
                "openai/gpt-oss-20b",          # 🆕 OpenAI OSS 20B (eficiente)
                "llama-3.3-70b-versatile",      # Llama 3.3 
                "llama3-70b-8192",              # Llama 3 estável
                "llama3-8b-8192",               # Mais rápido
                "mixtral-8x7b-32768",           # Contexto longo
                "gemma2-9b-it",                 # Eficiente
            ],
            index=0,
            help="Modelos GroqCloud - Agora com OpenAI OSS!"
        )
        
        # Informação sobre o modelo GroqCloud selecionado
        groq_info = {
            "openai/gpt-oss-120b": "🚀 OpenAI OSS 120B - Flagship open-source da OpenAI (NOVO!)",
            "openai/gpt-oss-20b": "⚡ OpenAI OSS 20B - Eficiente e rápido (NOVO!)",
            "llama-3.3-70b-versatile": "🦙 Llama 3.3 - Meta's mais recente",
            "llama3-70b-8192": "💪 Llama 3 70B - Balanceado e confiável", 
            "llama3-8b-8192": "⚡ Llama 3 8B - Rápido e eficiente",
            "mixtral-8x7b-32768": "📚 Mixtral - Melhor para textos longos",
            "gemma2-9b-it": "🎯 Gemma2 - Otimizado e preciso"
        }
        st.info(groq_info.get(model_choice, "Modelo selecionado"))
    
    temperature = st.slider("Criatividade (Temperature)", 0.0, 1.0, 0.2)
    max_tokens = st.slider("Tamanho do resumo", 300, 2000, 800)
    
    # Nota especial para modelos especiais
    if ai_provider == "OpenAI" and model_choice.startswith("o1"):
        st.warning("⚠️ Modelos o1 usam reasoning interno e podem demorar mais, mas são mais precisos!")
    elif ai_provider == "GroqCloud" and "gpt-oss" in model_choice:
        st.success("🆕 Modelo OpenAI OSS - Open Source da OpenAI rodando no GroqCloud!")
    
    # Informações sobre velocidade
    if ai_provider == "GroqCloud":
        if "gpt-oss-120b" in model_choice:
            st.info("🚀 OpenAI OSS 120B: ~500+ tokens/s - Qualidade OpenAI com velocidade Groq!")
        elif "gpt-oss-20b" in model_choice:
            st.info("⚡ OpenAI OSS 20B: ~1000+ tokens/s - Ultra rápido!")
        else:
            st.info("⚡ GroqCloud oferece inferência ultrarrápida!")
    else:
        st.info("🧠 OpenAI o1 oferece reasoning avançado para análises profundas!")

def search_web(query: str, num_results: int = 10) -> List[Dict]:
    """Buscar informações na web usando SerpAPI"""
    if not serpapi_key:
        st.error("❌ SERPAPI_KEY não configurada. Adicione no arquivo .env")
        return []
    
    params = {
        "q": query,
        "api_key": serpapi_key,
        "engine": "google",
        "num": num_results,
        "hl": language,
        "gl": country if country != "global" else "us",
        "safe": "active",
        "tbm": "nws" if st.session_state.get('search_news', False) else None
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=15)
        response.raise_for_status()
        results = response.json()
        
        # Extrair diferentes tipos de resultados
        all_results = []
        
        # Resultados orgânicos
        organic_results = results.get("organic_results", [])
        for item in organic_results:
            all_results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("displayed_link", ""),
                "type": "web"
            })
        
        # Resultados de notícias
        news_results = results.get("news_results", [])
        for item in news_results:
            all_results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("source", ""),
                "type": "news",
                "date": item.get("date", "")
            })
        
        # Knowledge graph (se disponível)
        knowledge_graph = results.get("knowledge_graph", {})
        if knowledge_graph:
            all_results.insert(0, {
                "title": knowledge_graph.get("title", ""),
                "link": knowledge_graph.get("website", ""),
                "snippet": knowledge_graph.get("description", ""),
                "source": "Knowledge Graph",
                "type": "knowledge"
            })
        
        return all_results
        
    except requests.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return []
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return []

def generate_summary_with_ai(query: str, search_results: List[Dict], ai_provider: str, model_choice: str) -> str:
    """Gerar resumo usando OpenAI ou GroqCloud"""
    
    # Preparar contexto dos resultados
    context = ""
    for i, result in enumerate(search_results[:12], 1):  # Limitar a 12 resultados
        context += f"[FONTE {i}]\n"
        context += f"Título: {result['title']}\n"
        context += f"Tipo: {result['type'].upper()}\n"
        context += f"Fonte: {result['source']}\n"
        if result.get('date'):
            context += f"Data: {result['date']}\n"
        context += f"Conteúdo: {result['snippet']}\n"
        context += f"Link: {result['link']}\n\n"
    
    # Prompt otimizado para análise
    if model_choice.startswith("o1"):
        # Prompt especial para modelos o1 (reasoning)
        prompt = f"""Analise profundamente as informações sobre "{query}" e forneça uma análise estruturada e detalhada.

FONTES DISPONÍVEIS:
{context}

Como um analista especializado, crie um resumo abrangente que demonstre raciocínio crítico e análise profunda. Use apenas as informações das fontes fornecidas.

Estruture sua resposta com:
- Resumo executivo dos pontos principais
- Análise detalhada com insights críticos
- Tendências e padrões identificados
- Implicações e perspectivas futuras
- Conclusões fundamentadas

Seja preciso, analítico e use markdown para formatação."""
    else:
        # Prompt padrão para outros modelos
        prompt = f"""Você é um analista especializado em síntese de informações. Analise as fontes sobre "{query}" e crie um resumo completo e estruturado.

FONTES CONSULTADAS:
{context}

INSTRUÇÕES:
1. Crie um resumo abrangente e bem fundamentado
2. Use APENAS informações das fontes fornecidas
3. Organize o conteúdo de forma lógica e fluida
4. Destaque tendências e padrões importantes
5. Mantenha neutralidade e objetividade
6. Use formatação markdown para clareza
7. Cite insights de diferentes fontes quando relevante

ESTRUTURA OBRIGATÓRIA:
## 🎯 Resumo Executivo
[Síntese dos pontos principais em 2-3 parágrafos]

## 📊 Análise Detalhada
[Desenvolvimento aprofundado dos temas centrais]

## 🔍 Insights Principais
• [Ponto relevante 1]
• [Ponto relevante 2] 
• [Ponto relevante 3]
• [Outros insights importantes]

## 📈 Tendências e Perspectivas
[Análise de tendências e projeções quando aplicável]

## 💡 Conclusões
[Síntese final e considerações importantes]

Responda APENAS com o resumo estruturado. Seja preciso e informativo."""
    
    try:
        if ai_provider == "OpenAI":
            if not openai_client:
                return "❌ OpenAI não configurada. Configure OPENAI_API_KEY no arquivo .env"
            
            # Configurações específicas para modelos o1
            if model_choice.startswith("o1"):
                response = openai_client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    # Modelos o1 não suportam system message, temperature, etc.
                )
            else:
                response = openai_client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um especialista em análise de informações que cria resumos precisos e bem estruturados baseados em fontes web confiáveis."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
            
            return response.choices[0].message.content
            
        else:  # GroqCloud
            if not groq_client:
                return "❌ GroqCloud não configurada. Configure GROQ_API_KEY no arquivo .env"
            
            response = groq_client.chat.completions.create(
                model=model_choice,
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um especialista em análise de informações que cria resumos precisos e bem estruturados baseados em fontes web confiáveis."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9,
                stream=False
            )
            
            return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Erro ao gerar resumo: {str(e)}\n\nVerifique se sua chave de API está correta."

def display_sources(search_results: List[Dict]):
    """Exibir fontes de forma organizada"""
    st.subheader("📚 Fontes Consultadas")
    
    # Separar por tipo
    knowledge_results = [r for r in search_results if r.get('type') == 'knowledge']
    news_results = [r for r in search_results if r.get('type') == 'news']
    web_results = [r for r in search_results if r.get('type') == 'web']
    
    # Exibir em abas
    tab1, tab2, tab3 = st.tabs(["🌐 Web", "📰 Notícias", "🧠 Knowledge Graph"])
    
    with tab1:
        if web_results:
            for i, result in enumerate(web_results, 1):
                with st.expander(f"{i}. {result['title'][:70]}..."):
                    st.write(f"**🔗 Fonte:** {result['source']}")
                    st.write(f"**📝 Resumo:** {result['snippet']}")
                    st.markdown(f"[➡️ Acessar link completo]({result['link']})")
        else:
            st.info("Nenhum resultado web encontrado.")
    
    with tab2:
        if news_results:
            for i, result in enumerate(news_results, 1):
                with st.expander(f"{i}. {result['title'][:70]}..."):
                    st.write(f"**📰 Fonte:** {result['source']}")
                    if result.get('date'):
                        st.write(f"**📅 Data:** {result['date']}")
                    st.write(f"**📝 Resumo:** {result['snippet']}")
                    st.markdown(f"[➡️ Ler notícia completa]({result['link']})")
        else:
            st.info("Nenhuma notícia encontrada.")
    
    with tab3:
        if knowledge_results:
            for result in knowledge_results:
                st.write(f"**🧠 Título:** {result['title']}")
                st.write(f"**📝 Descrição:** {result['snippet']}")
                if result['link']:
                    st.markdown(f"[➡️ Mais informações]({result['link']})")
        else:
            st.info("Nenhum Knowledge Graph disponível.")

# Interface principal
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    query = st.text_input(
        "🔍 Digite sua pesquisa:",
        placeholder="Ex: inteligência artificial 2024, economia brasileira, tecnologia...",
        help="Digite qualquer tema para buscar informações atualizadas e receber análise por IA"
    )

with col2:
    search_type = st.selectbox("Tipo", ["Geral", "Notícias"], key="search_type")
    if search_type == "Notícias":
        st.session_state['search_news'] = True
    else:
        st.session_state['search_news'] = False

with col3:
    search_button = st.button("🚀 Buscar", type="primary", use_container_width=True)

# Executar busca
if query and (search_button or st.session_state.get('last_query') != query):
    st.session_state['last_query'] = query
    
    if not serpapi_key:
        st.error("⚠️ Configure SERPAPI_KEY no arquivo .env")
    elif ai_provider == "OpenAI" and not openai_api_key:
        st.error("⚠️ Configure OPENAI_API_KEY no arquivo .env para usar modelos OpenAI")
    elif ai_provider == "GroqCloud" and not groq_api_key:
        st.error("⚠️ Configure GROQ_API_KEY no arquivo .env para usar GroqCloud")
    else:
        # Container para resultados
        results_container = st.container()
        
        with results_container:
            # Mostrar progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Passo 1: Buscar na web
            status_text.text("🔍 Buscando informações na web...")
            progress_bar.progress(30)
            
            search_results = search_web(query, num_results)
            
            if not search_results:
                progress_bar.empty()
                status_text.empty()
                st.warning("❌ Nenhum resultado encontrado. Tente termos diferentes ou verifique sua conexão.")
            else:
                # Passo 2: Gerar resumo com IA
                if ai_provider == "GroqCloud" and "gpt-oss" in model_choice:
                    provider_text = "🚀 Analisando com OpenAI OSS..."
                elif model_choice.startswith("o1"):
                    provider_text = "🧠 o1 Reasoning..."
                else:
                    provider_text = f"⚡ Analisando com {ai_provider}..."
                    
                status_text.text(provider_text)
                progress_bar.progress(70)
                
                # Cronometrar a geração
                start_time = datetime.now()
                summary = generate_summary_with_ai(query, search_results, ai_provider, model_choice)
                end_time = datetime.now()
                generation_time = (end_time - start_time).total_seconds()
                
                # Passo 3: Finalizar
                status_text.text("✅ Análise concluída!")
                progress_bar.progress(100)
                
                # Limpar indicadores
                progress_bar.empty()
                status_text.empty()
                
                # Métricas detalhadas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Fontes", len(search_results))
                with col2:
                    web_count = len([r for r in search_results if r.get('type') == 'web'])
                    st.metric("🌐 Sites", web_count)
                with col3:
                    news_count = len([r for r in search_results if r.get('type') == 'news'])
                    st.metric("📰 Notícias", news_count)
                with col4:
                    st.metric("⚡ Velocidade", f"{generation_time:.1f}s")
                
                # Resumo principal
                st.markdown("---")
                st.markdown("## 📋 Análise Inteligente")
                
                # Exibir o resumo
                if "❌" not in summary:
                    st.markdown(summary)
                else:
                    st.error(summary)
                
                # Fontes
                st.markdown("---")
                display_sources(search_results)
                
                # Informações adicionais
                st.markdown("---")
                info_col1, info_col2 = st.columns(2)
                with info_col1:
                    st.info(f"🕒 Pesquisa realizada: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
                with info_col2:
                    if ai_provider == "OpenAI":
                        if model_choice.startswith("o1"):
                            st.success(f"🧠 Reasoning completo em {generation_time:.1f}s")
                        else:
                            st.success(f"🤖 OpenAI processou em {generation_time:.1f}s")
                    else:
                        if "gpt-oss" in model_choice:
                            st.success(f"🚀 OpenAI OSS processou em {generation_time:.1f}s")
                        else:
                            st.success(f"⚡ GroqCloud processou em {generation_time:.1f}s")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 2rem;'>
    <p>💡 <strong>Motor de Busca Inteligente</strong></p>
    <p>🚀 Powered by <strong>OpenAI OSS 120B</strong> + <strong>GroqCloud</strong> + SerpAPI</p>
    <p><small>Configure GROQ_API_KEY e SERPAPI_KEY no arquivo .env</small></p>
</div>
""", unsafe_allow_html=True)

# Dicas na sidebar
with st.sidebar:
    st.markdown("---")
    st.subheader("💡 Dicas de Uso")
    st.markdown("""
    **🆕 OpenAI OSS vs Outros:**
    - 🚀 **OSS 120B**: Qualidade OpenAI + Velocidade Groq
    - ⚡ **OSS 20B**: Ultra rápido (1000+ t/s)
    - 🦙 **Llama**: Open source tradicional
    
    **Termos específicos** funcionam melhor:
    - ✅ "IA generativa trends 2025"
    - ✅ "Bitcoin análise mercado"
    - ❌ "tecnologia" (muito amplo)
    
    **Para notícias** use o filtro "Notícias"
    """)
    
    st.markdown("---")
    st.markdown("**🔑 APIs Necessárias:**")
    st.markdown("- [GroqCloud](https://console.groq.com) (Gratuito + OSS)")
    st.markdown("- [SerpAPI](https://serpapi.com) (Busca web)")
    
    st.markdown("---")
    st.subheader("🆕 OpenAI OSS Models")
    st.markdown("""
    **GPT-OSS 120B**: Mixture-of-Experts (MoE) com 20B parâmetros ativos e 128 experts
    
    **Performance**: Near-parity com o4-mini em reasoning, roda em single 80GB GPU
    
    **Velocidade**: 500+ tokens/s (120B) e 1000+ tokens/s (20B)
    """)

🔍 Motor de Busca Inteligente
Um sistema de busca avançado que combina busca web em tempo real com análise de IA para gerar resumos inteligentes e estruturados sobre qualquer tema.

🚀 Novidade: OpenAI OSS 120B
Agora com os novos modelos open-source da OpenAI! Aproveite a qualidade OpenAI com a velocidade ultrarrápida do GroqCloud.

🧠 OpenAI OSS 120B: 500+ tokens/s com qualidade premium
⚡ OpenAI OSS 20B: 1000+ tokens/s ultra rápido
🌍 100% Open Source: Transparência total
✨ Funcionalidades
🔍 Busca Web Inteligente: Integração com SerpAPI para resultados atualizados
🤖 Análise por IA: Resumos estruturados usando modelos de ponta
📰 Filtros Especializados: Busca geral ou focada em notícias
⚡ Ultra Velocidade: Processamento em segundos via GroqCloud
📚 Múltiplas Fontes: Web, notícias e knowledge graphs
🎯 Interface Moderna: Design responsivo e intuitivo
🛠️ Tecnologias
Frontend: Streamlit (Python)
IA: OpenAI OSS, Llama 3.3, Mixtral (via GroqCloud)
Busca Web: SerpAPI
Gerenciamento: python-dotenv
📋 Pré-requisitos
Python 3.8+
Chaves de API (gratuitas):
GroqCloud
SerpAPI (100 buscas gratuitas)
🚀 Instalação Rápida
1. Clone o repositório
bash
git clone <url-do-repositorio>
cd motor-busca-inteligente
2. Instale as dependências
bash
pip install streamlit requests python-dotenv groq openai
3. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto:

env
# Obrigatórias
SERPAPI_KEY=sua_chave_serpapi_aqui
GROQ_API_KEY=sua_chave_groq_aqui

# Opcional (para modelos OpenAI o1)
OPENAI_API_KEY=sk-sua_chave_openai_aqui
4. Execute o aplicativo
bash
streamlit run app.py
🎯 Como Usar
Acesse http://localhost:8501 no seu navegador
Escolha o provedor de IA:
GroqCloud: Ultra rápido (recomendado)
OpenAI: Para modelos o1 (reasoning)
Selecione o modelo:
openai/gpt-oss-120b (🔥 Recomendado)
openai/gpt-oss-20b (mais rápido)
Llama, Mixtral, Gemma2
Digite sua pesquisa
Receba análise completa em segundos!
📊 Modelos Disponíveis
🆕 OpenAI OSS (via GroqCloud)
Modelo	Parâmetros	Velocidade	Qualidade	Uso
openai/gpt-oss-120b	120B	500+ t/s	🏆 Excelente	Análises profundas
openai/gpt-oss-20b	20B	1000+ t/s	📝 Muito Boa	Uso geral rápido
🦙 Outros Modelos
Llama 3.3 70B: Meta's mais recente
Mixtral 8x7B: Melhor para contexto longo
Gemma2 9B: Google, eficiente
🧠 OpenAI o1 (opcional)
o1: Reasoning avançado (mais lento)
o1-mini: Reasoning rápido
🎨 Interface
Principais Recursos
🔍 Busca Inteligente: Campo de entrada intuitivo
⚙️ Configurações: Sidebar com controles avançados
📊 Métricas: Estatísticas em tempo real
📚 Fontes Organizadas: Abas separadas por tipo
🔄 Cache Management: Botões de limpeza integrados
Filtros de Busca
Geral: Resultados web + knowledge graphs
Notícias: Foco em conteúdo jornalístico atual
📝 Exemplo de Uso
python
# Busca: "inteligência artificial 2025"
# Resultado: Resumo estruturado com:

## 🎯 Resumo Executivo
Análise das principais tendências...

## 📊 Análise Detalhada  
Desenvolvimento aprofundado dos temas...

## 🔍 Insights Principais
- Tendência 1: Explicação detalhada
- Tendência 2: Análise contextual
- Tendência 3: Perspectivas futuras

## 💡 Conclusões
Síntese final e considerações...
🔧 Configurações Avançadas
Parâmetros de IA
Temperature: Controle de criatividade (0.0 - 1.0)
Max Tokens: Tamanho do resumo (300 - 2000)
Número de Fontes: 3-20 resultados
Configurações de Busca
Idioma: pt, en, es
País: br, us, es, global
Filtros de Segurança: Ativo por padrão
🚨 Solução de Problemas
Erros Comuns
❌ "SERPAPI_KEY não configurada"

bash
# Verifique se o arquivo .env existe e contém:
SERPAPI_KEY=sua_chave_aqui
❌ "Modelo descontinuado"

bash
# Use os modelos atualizados:
openai/gpt-oss-120b  # ✅ Recomendado
llama-3.3-70b-versatile  # ✅ Alternativa
❌ "Nenhum resultado encontrado"

Tente termos mais específicos
Verifique conexão com internet
Teste com palavras-chave diferentes
Limpeza de Cache
Interface: Botões 🗑️ e 🔄 na sidebar
Teclado: Pressione C na página
Terminal: Ctrl+C e reinicie
📈 Performance
Velocidades Típicas
OpenAI OSS 120B: 500+ tokens/s (~2-5 segundos)
OpenAI OSS 20B: 1000+ tokens/s (~1-3 segundos)
Llama 3.3: 300+ tokens/s (~3-7 segundos)
Mixtral: 200+ tokens/s (~5-10 segundos)
Benchmarks
Qualidade: OSS 120B ≈ GPT-4 level
Velocidade: 10x mais rápido que APIs tradicionais
Custo: 80% mais barato que OpenAI oficial
🔐 Segurança e Privacidade
🔒 Chaves Locais: APIs keys ficam no seu .env
🚫 Sem Logs: Não armazenamos suas pesquisas
🛡️ Filtros Seguros: Conteúdo filtrado automaticamente
🌍 GDPR Compliant: Respeita regulamentações
🤝 Contribuição
Contribuições são bem-vindas! Para contribuir:

Fork o projeto
Crie uma branch (git checkout -b feature/nova-funcionalidade)
Commit suas mudanças (git commit -am 'Adiciona nova funcionalidade')
Push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request
📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

🙏 Agradecimentos
OpenAI: Pelos modelos OSS revolucionários
GroqCloud: Pela infraestrutura ultrarrápida
SerpAPI: Pela API de busca confiável
Streamlit: Pelo framework incrível
Meta: Pelos modelos Llama open-source
📞 Suporte
Encontrou um bug ou tem uma sugestão?

🐛 Abra uma issue
💬 Discussões
📧 Contato: [seu-email@exemplo.com]
🗺️ Roadmap
✅ Concluído
 Integração OpenAI OSS
 Interface moderna
 Múltiplos provedores de IA
 Cache inteligente
🔄 Em Desenvolvimento
 Exportação de relatórios (PDF/Word)
 Histórico de pesquisas
 Análise de sentimento
 Suporte a múltiplos idiomas
🎯 Planejado
 API REST
 Plugin para navegadores
 Análise de imagens
 Integração com bases acadêmicas
<div align="center">
🚀 Feito com ❤️ e IA de ponta

⭐ Star no GitHub | 🐛 Reportar Bug | 💡 Sugerir Feature

</div>

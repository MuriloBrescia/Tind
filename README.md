# 💬 Tind AI - Assistente Inteligente de Conversação

Tind AI é um assistente inteligente de conversação que gera respostas contextuais e aprende com o feedback do usuário para melhorar a qualidade da conversa ao longo do tempo.

## ✨ Recursos

### 🧠 Geração Inteligente de Respostas
- **Respostas conscientes do contexto**: Entende o contexto da conversa e gera respostas apropriadas
- **Adaptação de tom**: Adapta-se a diferentes contextos emocionais (triste, feliz, neutro, cumprimentos)
- **Filtragem de conteúdo**: Filtra automaticamente conteúdo inapropriado para conversas seguras
- **Múltiplas opções de resposta**: Gera 5 opções diferentes de resposta para cada contexto

### 🎯 Feedback do Usuário e Aprendizado
- **Sistema de feedback interativo**: Usuários podem selecionar a melhor resposta entre as opções geradas
- **Aprendizado contínuo**: IA melhora baseada nas preferências e feedback dos usuários
- **Coleta de dados de treinamento**: Armazena com segurança dados de conversa anônimos para melhoria do modelo
- **Acompanhamento de progresso**: Indicadores visuais de progresso mostrando o avanço do aprendizado da IA

### 🌐 Interface Web Moderna
- **Design responsivo**: Funciona perfeitamente em desktop, tablet e dispositivos móveis
- **UI bonita**: Design gradiente moderno com animações e transições suaves
- **Validação em tempo real**: Validação de entrada com contadores de caracteres e mensagens de erro úteis
- **Estados de carregamento**: Feedback visual durante a geração de respostas e salvamento de dados

### 📊 Análise e Monitoramento
- **Dashboard de estatísticas**: Visualize progresso do treinamento, contagens de conversa e métricas de melhoria da IA
- **Monitoramento de saúde**: Endpoints integrados de verificação de saúde para monitoramento do sistema
- **Tratamento de erros**: Tratamento abrangente de erros com páginas de erro amigáveis ao usuário
- **Sistema de logging**: Logging estruturado para depuração e monitoramento

### 🔧 Recursos para Desenvolvedores
- **API REST**: Endpoints de API JSON para acesso programático
- **Type hints**: Anotações de tipo completas para melhor clareza de código e suporte do IDE
- **Arquitetura modular**: Separação clara de responsabilidades com estrutura de código organizada
- **Thread safety**: Acesso concorrente seguro a recursos compartilhados
- **Configuração de ambiente**: Configurável via variáveis de ambiente

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd tind
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   python src/app.py
   ```

4. **Abra seu navegador**
   Navegue para `http://localhost:5000`

### Alternativa: Interface de Linha de Comando

Você também pode usar o Tind AI pela linha de comando:

```bash
# Modo de conversa interativa
python src/agent.py

# Fine-tuning do modelo
python src/fine_tune.py
```

## 📁 Estrutura do Projeto

```
tind/
├── src/
│   ├── agent.py           # Agente IA principal com geração de respostas
│   ├── app.py             # Aplicação web Flask
│   ├── fine_tune.py       # Treinamento e fine-tuning do modelo
│   └── templates/         # Templates HTML
│       ├── index.html     # Interface principal de conversa
│       ├── responses.html # Página de seleção de resposta
│       ├── error.html     # Página de tratamento de erros
│       └── stats.html     # Dashboard de estatísticas
├── data/
│   └── training_data.json # Feedback do usuário e dados de treinamento
├── models/
│   ├── model.txt          # Arquivo do modelo IA
│   └── model_metadata.json # Metadados e informações de versão do modelo
├── requirements.txt       # Dependências Python
└── README.md             # Este arquivo
```

## 🎮 Guia de Uso

### Interface Web

1. **Iniciar uma conversa**
   - Digite o contexto da sua conversa na área de texto
   - Exemplos: "Oi! Como está seu dia?" ou "Estou me sentindo triste hoje"
   - Clique em "Gerar Respostas" para obter sugestões da IA

2. **Selecionar a melhor resposta**
   - Revise as 5 respostas geradas
   - Clique na resposta que soa mais natural
   - Envie seu feedback para ajudar a melhorar a IA

3. **Monitorar progresso**
   - Visite `/stats` para ver progresso do treinamento e estatísticas
   - Verifique `/health` para status do sistema

### Endpoints da API

- `POST /api/responses` - Gerar respostas (JSON)
- `POST /api/feedback` - Enviar feedback (JSON)
- `GET /health` - Verificação de saúde
- `GET /stats` - Página de estatísticas

### Uso por Linha de Comando

```bash
# Modo interativo
python src/agent.py

# Fine-tuning
python src/fine_tune.py
```

## 🔧 Configuração

### Variáveis de Ambiente

- `SECRET_KEY` - Chave secreta do Flask (padrão: 'dev-key-change-in-production')
- `PORT` - Porta do servidor (padrão: 5000)
- `FLASK_ENV` - Modo do ambiente ('development' ou 'production')

### Exemplo de Configuração

```bash
export SECRET_KEY="sua-chave-secreta-aqui"
export PORT=8080
export FLASK_ENV=development
python src/app.py
```

## 🏗️ Arquitetura

### Componentes Principais

1. **TindAgent** - Classe principal do agente IA lidando com geração de respostas e aprendizado
2. **ModelTrainer** - Lida com fine-tuning e avaliação do modelo
3. **Flask App** - Interface web e endpoints da API
4. **Templates** - Templates HTML modernos e responsivos

### Principais Melhorias Implementadas

#### 🔒 Segurança e Confiabilidade
- Validação e sanitização de entrada
- Proteção XSS com escape adequado de HTML
- Operações de arquivo thread-safe
- Tratamento abrangente de erros
- Considerações de limitação de taxa

#### 🎨 Experiência do Usuário
- Design moderno e responsivo
- Validação de entrada em tempo real
- Estados de carregamento e indicadores de progresso
- Mensagens de erro amigáveis
- Interface otimizada para mobile

#### 🛠️ Qualidade do Código
- Type hints em todo o código
- Logging abrangente
- Arquitetura modular e sustentável
- Separação adequada de responsabilidades
- Documentação e comentários

#### 📈 Recursos
- Dashboard de estatísticas e análise
- Endpoints de monitoramento de saúde
- API para acesso programático
- Versionamento e metadados do modelo
- Acompanhamento de progresso

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erros de módulo não encontrado**
   ```bash
   # Certifique-se de estar na raiz do projeto e instale as dependências
   pip install -r requirements.txt
   ```

2. **Erros de permissão em operações de arquivo**
   ```bash
   # Garanta que os diretórios data e models sejam graváveis
   chmod 755 data models
   ```

3. **Porta já em uso**
   ```bash
   # Use uma porta diferente
   export PORT=8080
   python src/app.py
   ```

### Modo Debug

Execute em modo debug para informações detalhadas de erro:

```bash
export FLASK_ENV=development
python src/app.py
```

## 📊 Performance e Escalabilidade

- **Leve**: Dependências mínimas, inicialização rápida
- **Thread-safe**: Tratamento de requisições concorrentes
- **Eficiente**: Operações de I/O de arquivo otimizadas
- **Escalável**: Fácil de containerizar e implantar

## 🤝 Contribuindo

1. Faça fork do repositório
2. Crie uma branch de feature
3. Faça suas melhorias
4. Adicione testes se aplicável
5. Envie um pull request

## 📝 Licença

Este projeto é open source e disponível sob a Licença MIT.

## 🙏 Agradecimentos

- Construído com Flask e tecnologias web modernas
- Inspirado pela necessidade de melhor IA conversacional
- Obrigado a todos os usuários que fornecem feedback para melhorar a IA

## 📞 Suporte

Para problemas, dúvidas ou solicitações de recursos, por favor abra uma issue no repositório ou entre em contato com a equipe de desenvolvimento.

---

**Boas Conversas! 💬✨**
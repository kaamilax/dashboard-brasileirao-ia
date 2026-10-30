# &#x20;Dashboard do Brasileirão com Assistente de IA

Projeto desenvolvido em Python com o objetivo de explorar e visualizar dados do Campeonato Brasileiro de Futebol por meio de um dashboard interativo, contando também com um assistente de Inteligência Artificial integrado à API do Google Gemini.

## &#x20;Funcionalidades

- Visualização de dados históricos do Campeonato Brasileiro.
- Filtros por ano e clube.
- Gráficos interativos para análise dos clubes.
- Exibição de indicadores estatísticos.
- Tabela com informações dos clubes.
- Chat flutuante com assistente de IA.
- Respostas a perguntas sobre os dados do campeonato, utilizando o Google Gemini.

## &#x20;Tecnologias utilizadas

- **Python** — linguagem principal.
- **Dash** — desenvolvimento do dashboard interativo.
- **Plotly** — criação de gráficos.
- **Pandas** — manipulação e análise dos dados.
- **Dash Bootstrap Components** — estilização da interface.
- **Google Gemini API** — integração com Inteligência Artificial.
- **Python-dotenv** — gerenciamento de variáveis de ambiente.

## 📂 Estrutura do projeto

```text
PROJECT PYTHON TO PROJECT ONE/
│
├── assets/
│   └── style.css
│
├── COMPONENTS/
│   └── Tabela_Clubes.csv
│
├── app2.py
├── assistent_IA.py
├── textAssistentIA.py
├── .env
├── .gitignore
└── README.md
```

## ⚙️ Como executar o projeto

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
```

### 2. Entre na pasta do projeto

```bash
cd dashboard-brasileirao-ia
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install dash dash-bootstrap-components pandas plotly google-genai python-dotenv
```

### 6. Configure a chave da API Gemini

Crie um arquivo `.env` na pasta principal do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
```

Substitua `sua_chave_aqui` pela sua chave da API Gemini.

### 7. Execute o dashboard

```bash
python app2.py
```

Após iniciar, acesse o endereço local exibido no terminal.

## &#x20;Assistente de Inteligência Artificial

O projeto conta com um assistente integrado ao Google Gemini, permitindo que o usuário faça perguntas em linguagem natural sobre as estatísticas do Campeonato Brasileiro.

As respostas são baseadas nos dados disponíveis no dashboard e nos filtros selecionados.

## &#x20;Objetivo

Este projeto tem como objetivo praticar conceitos de programação em Python, análise e manipulação de dados, visualização de informações e integração de APIs de Inteligência Artificial.

---

Desenvolvido como projeto de estudo.

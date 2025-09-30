## 📄 README.md: Classificador Inteligente de E-mails Financeiros

# Classificador Inteligente de E-mails (AI Email Sorter)

Solução digital desenvolvida em Python (FastAPI) e Inteligência Artificial (Gemini API) para automatizar a classificação de e-mails em categorias produtivas ou improdutivas e sugerir respostas automáticas. Criado como parte de um desafio para otimizar o fluxo de trabalho de uma grande empresa do setor financeiro com alto volume de comunicação.

---

## 🚀 Solução Online (Deploy)

A aplicação está hospedada e acessível publicamente através do Render, pronta para testes.

| Descrição | Link |
| :--- | :--- |
| **Aplicação Web Funcional** | `https://email-classifier-mateus-batista.onrender.com` |
| **Vídeo Demonstração (YouTube)** | `https://youtu.be/CQLELSioez8` |

---

## ✨ Recursos e Funcionalidades

A solução atende aos requisitos do desafio focando em uma experiência de usuário (UX) clara e eficiente:

1.  **Interface Intuitiva:** Frontend simples em HTML/CSS/JavaScript para inserção direta do conteúdo do e-mail.
2.  **Classificação Imediata:** Categoriza o texto inserido em **Produtivo** (requer ação) ou **Improdutivo** (apenas informativo).
3.  **Geração de Resposta por IA:** Sugere uma resposta automática adequada ao tom e à categoria identificada.
4.  **Backend Moderno:** Utiliza **FastAPI** para um serviço Python assíncrono e de alta performance.
5.  **Tecnologia de IA:** Integração com a **Gemini API** para classificação zero-shot e geração de texto de alta qualidade via **Prompt Engineering**.

---

## 💻 Tecnologias Utilizadas

| Componente | Tecnologia | Versão/Justificativa |
| :--- | :--- | :--- |
| **Backend** | Python | 3.10+ |
| **Framework Web** | FastAPI | Escolhido por ser rápido e assíncrono (ASGI). |
| **Servidor de Produção**| Gunicorn + Uvicorn | Combinação ASGI/WSGI para deploy robusto e multi-processamento. |
| **Inteligência Artificial**| Google Gemini API | Utilizada para classificação (*zero-shot*) e geração de respostas. |
| **Frontend** | HTML5, CSS (Bootstrap), JavaScript | Interface simples e responsiva. |
| **Hospedagem** | Render | Plataforma de deploy contínuo (PaaS). |

---

## 🛠️ Instruções para Execução Local

Siga estes passos para configurar e rodar a aplicação em seu ambiente local.

### Pré-requisitos

* Python 3.8+
* `pip` (Gerenciador de pacotes do Python)
* Chave de API da Gemini

### 1. Configuração do Ambiente

Clone o repositório e navegue até a pasta do projeto:

```bash
git clone [https://github.com/Mateus-SBatista/email-classifier.git]
cd email_classifier
```

### 2. Instalação de Dependências
Instale todas as bibliotecas necessárias usando o requirements.txt:

```bash
pip install -r requirements.txt
```
### 3. Configuração da Chave de API
É obrigatório definir sua chave de API como uma variável de ambiente:

Linux/macOS:

```bash
export GEMINI_API_KEY="SUA_CHAVE_AQUI"
```
Windows (CMD):

```bash

set GEMINI_API_KEY="SUA_CHAVE_AQUI"
```

### 4. Inicialização do Servidor
Inicie a aplicação utilizando o Uvicorn (modo de desenvolvimento) ou o Gunicorn (simulando produção):

```bash
# Modo Desenvolvimento (com recarregamento automático)
uvicorn app:app --reload

# Ou, simulando o modo Produção (usado no Render)
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 5. Acesso
Abra seu navegador e acesse: http://127.0.0.1:8000

---

## 🧠 Detalhes Técnicos e Prompt Engineering
O núcleo da aplicação reside na engenharia de prompts (instruções dadas à IA) para garantir resultados precisos e relevantes:

Classificação de Alto Nível
O sistema utiliza a Gemini API com prompts focados para categorizar o e-mail em uma das duas categorias definidas (Produtivo ou Improdutivo). A IA é instruída a retornar apenas a categoria, simplificando o fluxo de processamento no Python.

Geração de Resposta Condicional
O backend decide qual prompt enviar à IA com base na categoria:

'Produtivo': O prompt solicita uma resposta profissional com confirmação de recebimento, garantindo ao cliente que um analista está ciente e dará seguimento.

'Improdutivo': O prompt solicita uma resposta breve e cordial de agradecimento, liberando a equipe de ter que gastar tempo em mensagens que não requerem ação.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from google import genai
from google.genai.errors import APIError

# Configuração do FastAPI 
app = FastAPI()

# Configuração de templates para servir o HTML
templates = Jinja2Templates(directory="templates")

# Configuração da API Key (Recomendado: usar variáveis de ambiente!)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    try:
        with open("Gemini_Key.txt", "r") as f:
            GEMINI_API_KEY = f.read().strip()
            print("Chave GEMINI_API_KEY carregada do arquivo gemini_key.txt.")
    except Exception:
        print("AVISO: A variável de ambiente GEMINI_API_KEY não está definida e o arquivo gemini_key.txt não foi encontrado.")

# Modelo de dados para a requisição de classificação
class EmailInput(BaseModel):
    email_text: str

# --- Funções de IA (Prompt Engineering) ---

def get_gemini_client():
    """Inicializa e retorna o cliente Gemini se a chave estiver definida."""
    if not GEMINI_API_KEY:
        return None
    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Erro ao inicializar o cliente Gemini: {e}")
        return None

def classify_email(email_text: str) -> str:
    """Classifica o email em 'Produtivo' ou 'Improdutivo' usando a Gemini API."""
    client = get_gemini_client()
    if not client:
        return "Erro de Inicialização da API"

    # Prompt de Classificação
    prompt = f"""
    Você é um classificador de emails para uma grande instituição financeira.
    Classifique o email a seguir estritamente em uma das duas categorias: 'Produtivo' ou 'Improdutivo'.
    - 'Produtivo': Requer uma ação imediata (suporte, atualização de status, dúvida sobre o sistema).
    - 'Improdutivo': Não requer ação (felicitação, agradecimento, mensagem não relevante).

    Email a classificar:
    ---
    {email_text}
    ---
    Responda apenas com a palavra da categoria (ex: Produtivo ou Improdutivo).
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        # Limpa e padroniza a resposta
        category = response.text.strip().capitalize()
        return category if category in ["Produtivo", "Improdutivo"] else "Improdutivo"

    except APIError as e:
        print(f"Erro de API na classificação: {e}")
        return "Erro na Classificação (API)"
    except Exception as e:
        print(f"Erro inesperado na classificação: {e}")
        return "Erro Inesperado"

def generate_response(category: str, email_text: str) -> str:
    """Gera uma resposta automática com base na categoria."""
    client = get_gemini_client()
    if not client:
        return "Não foi possível gerar a resposta devido a um erro na API."

    # Prompts Condicionais
    if category == "Produtivo":
        prompt = f"""
        O email abaixo foi classificado como 'Produtivo'.
        Gere uma resposta automática profissional e empática para o cliente de uma instituição financeira. A resposta deve:
        1. Confirmar o recebimento da solicitação.
        2. Informar que a equipe irá iniciar a análise e responder em breve.
        3. Ser concisa (máximo de 3 frases).

        Email original: "{email_text[:100]}..."
        """
    elif category == "Improdutivo":
        prompt = """
        O email foi classificado como 'Improdutivo'.
        Gere uma resposta automática breve e cordial, agradecendo pela mensagem e desejando o mesmo (Ex: 'Agradecemos a gentileza e desejamos um ótimo final de ano!'). A resposta deve ter no máximo 2 frases.
        """
    else:
        return "Categoria desconhecida para gerar resposta."
        
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except APIError as e:
        print(f"Erro de API na geração de resposta: {e}")
        return "Erro na Geração de Resposta (API)"
    except Exception as e:
        print(f"Erro inesperado na geração de resposta: {e}")
        return "Erro Inesperado"

# --- Endpoints da API ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve a página HTML principal."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/classify")
async def process_email(input_data: EmailInput):
    """Endpoint principal para classificar e gerar a resposta."""
    email_text = input_data.email_text.strip()
    
    if not email_text:
        return {"category": "Erro", "response_suggestion": "Por favor, insira o texto do email."}

    # 1. Classificação
    category = classify_email(email_text)
    
    # 2. Geração de Resposta
    response_suggestion = generate_response(category, email_text)
    
    # Retorna o resultado
    return {
        "category": category,
        "response_suggestion": response_suggestion
    }

# --- Inicialização ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
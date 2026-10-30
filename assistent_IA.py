import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key: 
    raise ValueError("GEMINI_APT_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

def quest_timeWithMoreVictory(dados):

    if dados.empty:
        return "Não existem dados para esse filtro."

    valids_dados = dados.dropna(subset=["Vitorias"])

    if valids_dados.empty:
        return "Não existem dados válidos."

    i = valids_dados["Vitorias"].idxmax()

    clube = valids_dados.loc[i, "Clube"]
    v = int(valids_dados.loc[i, "Vitorias"])

    return f"{clube} teve mais vitórias, com {v} vitórias."

def result_quest(quest, result): 
    """
    Recebe uma pergunta do usuário e os dados do Brasileirão.
    Retorna uma resposta gerada pelo Gemini.
    
    """
    
    
    prompt = f"""
    
    Você é um assitente especializado em analisar dados do Campeonado Brasileiro de Futebol.
    
    Reponda em português, utilizando somente as informações fornecidas abaixo. Não invente estastísticas.
        
    RESULTADO CALCULADO PELO SISTEMA: 
    {result}
    
    PERGUNTA DO USUÁRIO:
    {quest}
    
    """
    
    resposta = client.models.generate_content(
        model="gemini-3.8-flash", contents=prompt
    )
    
    return resposta.text


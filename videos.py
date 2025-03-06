from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer "}  # Gere um token na Hugging Face

# token: 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

# video_url = "https://www.youtube.com/watch?v=Vohk5wgTf4A"

def analisar_sentimento(texto):
    response = requests.post(API_URL, headers=headers, json={"inputs": texto})
    return response.json()

@app.route('/busca_comentarios', methods=['GET'])
def obter_comentarios():
    url = request.args.get("url")  # Obtém a URL da query string
    if not url:
        return jsonify({"erro": "Parâmetro 'url' ausente"}), 400

    # Configurando o Chrome para rodar em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # Para rodar sem o uso da GPU (pode ser útil no modo headless)

    driver = webdriver.Chrome(options=options)  # Usando a configuração acima
    driver.get(url)
    time.sleep(3)

    for _ in range(3):  # Rola a página para carregar mais comentários
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

    comentarios = driver.find_elements(By.CSS_SELECTOR, "#content-text")
    
    # Substituindo \n por um espaço simples em cada comentário
    lista_comentarios = [comentario.text.replace("\n", "") for comentario in comentarios]
    
    driver.quit()
    return jsonify(lista_comentarios)  # Retorna os comentários como JSON

@app.route('/classificar_comentarios', methods=['GET'])
def classificar_comentarios():
    url = request.args.get("url")  # Obtém a URL da query string
    if not url:
        return jsonify({"erro": "Parâmetro 'url' ausente"}), 400

    resultado_json = []
    response = obter_comentarios(url)  # Obtém a resposta JSON
    comentarios = response.get_json() # Extrai a lista de comentários
    
    for comentario in comentarios:
        texto = comentario  # Pegamos diretamente o texto do comentário
        resultado = analisar_sentimento(texto)

        maior_avaliacao = None
        maior_score = 0

        if not resultado:
            continue

        for item in resultado[0]:
            if item.get('score') >= maior_score:
                maior_avaliacao = item.get('label')
                maior_score = item.get('score')

        if maior_avaliacao in ["5 stars", "4 stars"]:
            avaliacao = "Positivo"
        elif maior_avaliacao in ["2 stars", "1 star"]:
            avaliacao = "Negativo"
        else:
            avaliacao = "Neutro"

        resultado_json.append({"comentario": texto, "avaliação": maior_avaliacao, "classificação": avaliacao})

    return jsonify(resultado_json)

app.run(port=5001, host='localhost', debug=True)
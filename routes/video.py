from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from flask import jsonify, request, Blueprint

video_route = Blueprint("videos", __name__)

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer "}  # Gere um token na Hugging Face

# TOKEN: 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
# VIDEO: https://www.youtube.com/watch?v=r9GvvW9Gvcg&list=RDO84LRHxuYL8&index=10&ab_channel=Mission%C3%A1rioShalom-Topic

def analisar_sentimento(texto):
    response = requests.post(API_URL, headers=headers, json={"inputs": texto})
    return response.json()

@video_route.route('/busca_comentarios', methods=['GET'])
def obter_comentarios():
    url = request.args.get("url")  # Obtém a URL da query string
    if not url:
        return jsonify({"erro": "Parâmetro 'url' ausente"}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content-text")))

        for _ in range(5):  # Role mais vezes para garantir o carregamento dos comentários
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)

        comentarios = driver.find_elements(By.CSS_SELECTOR, "#content-text")
        lista_comentarios = [comentario.text.replace("\n", " ") for comentario in comentarios if comentario.text.strip()]
    except Exception as e:
        lista_comentarios = []
        print(f"Erro ao buscar comentários: {e}")

    driver.quit()
    return jsonify(lista_comentarios)

@video_route.route('/classificar_comentarios', methods=['GET'])
def classificar_comentarios():
    url = request.args.get("url")  # Obtém a URL da query string
    if not url:
        return jsonify({"erro": "Parâmetro 'url' ausente"}), 400

    resultado_json = []
    response = obter_comentarios()  # Obtém a resposta JSON
    comentarios = response.get_json()  # Extrai a lista de comentários

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

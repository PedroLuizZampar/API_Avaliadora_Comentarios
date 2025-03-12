import requests
from youtube_comment_downloader import YoutubeCommentDownloader
from flask import jsonify, request, Blueprint
from database.models.videos import Videos
from database.models.comentarios import Comentarios
from database.models.classificacoes import Classificacoes

video_route = Blueprint("videos", __name__)

API_URL = "https://api-inference.huggingface.co/models/tabularisai/multilingual-sentiment-analysis"
headers = {"Authorization": "Bearer "}  # Gere um token na Hugging Face

# TOKEN: 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
# VIDEO: https://www.youtube.com/watch?v=r9GvvW9Gvcg&list=RDO84LRHxuYL8&index=10&ab_channel=Mission%C3%A1rioShalom-Topic

def analisar_sentimento(texto):
        response = requests.post(API_URL, headers=headers, json={"inputs": texto})
        if response.status_code == 200:
            resultado = response.json()
            if isinstance(resultado, list) and len(resultado) > 0:
                return resultado[0]
            else:
                return None
        else:
            return None

@video_route.route('/cadastra_video', methods=['POST'])
def cadastrar_video():
    dados = request.form

    nome_video = dados['nome_video']
    qtde_comentarios = int(dados['qtde_comentarios'])
    url = dados['url']

    video = Videos.create(
        nome_video = nome_video,
        qtde_comentarios = qtde_comentarios,
        url = url
    )

    lista_comentarios = obter_comentarios(video.id, qtde_comentarios)

    for comentario in lista_comentarios:
        Comentarios.create(
            video = video,
            comentario = comentario,
            classificado = False
        )

    return jsonify(lista_comentarios)

def obter_comentarios(id, qtde_comentarios):    
    video = Videos.get_by_id(id)
    url = video.url
    
    try:
        downloader = YoutubeCommentDownloader()
        comments_generator = downloader.get_comments_from_url(url)
        
        # Coletar apenas os primeiros 10 comentários
        lista_comentarios = []
        for i, comment in enumerate(comments_generator):
            if i >= qtde_comentarios:
                break
            text = comment.get('text', '').replace('\n', ' ').strip()
            if text:
                lista_comentarios.append(text)
        
        return lista_comentarios
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar comentários: {str(e)}"})

@video_route.route('/classificar_comentarios/<int:id>', methods=['GET'])
def classificar_comentarios(id):
    video = Videos.get_by_id(id)
    comentarios = Comentarios.select().where(Comentarios.video == video)

    resultado_json = []

    for comentario in comentarios:
        texto = comentario.comentario

        resultado = analisar_sentimento(texto)

        if not resultado or not isinstance(resultado, list):
            continue

        maior_score = 0

        # Percorre a lista de classificações e seleciona a de maior score
        for item in resultado:
            if item.get('score', 0) > maior_score:
                maior_score = item.get('score')
            
        classificacao = item.get('label')

        resultado_json.append({
            "comentario": texto,
            "classificação": classificacao,
            "pontuação": maior_score
        })

        Classificacoes.create(
            comentario=comentario,
            classificacao=classificacao,
            confianca=maior_score
        )

    return jsonify(resultado_json)

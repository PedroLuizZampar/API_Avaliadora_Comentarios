import requests
from youtube_comment_downloader import YoutubeCommentDownloader
from flask import jsonify, request, Blueprint
from database.models.videos import Videos
from database.models.comentarios import Comentarios
from database.models.classificacoes import Classificacoes

video_route = Blueprint("videos", __name__)

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer "}  # Gere um token na Hugging Face

# TOKEN: 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
# VIDEO: https://www.youtube.com/watch?v=r9GvvW9Gvcg&list=RDO84LRHxuYL8&index=10&ab_channel=Mission%C3%A1rioShalom-Topic

def analisar_sentimento(texto):
    response = requests.post(API_URL, headers=headers, json={"inputs": texto})
    return response.json()

@video_route.route('/cadastra_video', methods=['POST'])
def cadastrar_video():
    dados = request.form

    nome_video = dados['nome_video']
    qtde_comentarios = dados['qtde_comentarios']
    url = dados['url']

    video = Videos.create(
        nome_video = nome_video,
        qtde_comentarios = qtde_comentarios,
        url = url
    )

    lista_comentarios = obter_comentarios(video.id)

    for comentario in lista_comentarios:
        Comentarios.create(
            video = video,
            comentario = comentario,
            classificado = False
        )

    return jsonify(lista_comentarios)

def obter_comentarios(id):    
    video = Videos.get_by_id(id)
    url = video.url
    
    try:
        downloader = YoutubeCommentDownloader()
        comments_generator = downloader.get_comments_from_url(url)
        
        # Coletar apenas os primeiros 10 comentários
        lista_comentarios = []
        for i, comment in enumerate(comments_generator):
            if i >= 10:
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
        resultado = analisar_sentimento(comentario.comentario)

        maior_avaliacao = None
        maior_score = 0

        if not resultado:
            continue

        for item in resultado[0]:
            if item.get('score') >= maior_score:
                maior_avaliacao = item.get('label')
                maior_score = item.get('score')

        if maior_avaliacao in ["5 stars", "4 stars"]:
            classificacao = "Positivo"
        elif maior_avaliacao in ["2 stars", "1 star"]:
            classificacao = "Negativo"
        else:
            classificacao = "Neutro"

        resultado_json.append({
            "comentario": comentario.comentario,  # Agora apenas o texto do comentário
            "avaliação": maior_avaliacao,
            "classificação": classificacao
        })

        Classificacoes.create(
            comentario = comentario,
            avaliacao = maior_avaliacao,
            classificacao = classificacao
        )

    return jsonify(resultado_json)  # Retorna o resultado em formato JSON

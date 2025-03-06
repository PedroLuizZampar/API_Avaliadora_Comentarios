import requests
from flask import Flask, jsonify, request

API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
headers = {"Authorization": "Bearer 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"}  # Gere um token na Hugging Face

comentarios = comentarios_com_ids = [
    {"id": 1, "comentario": "Shang-Chi trouxe uma ação incrível e cenas de luta muito bem coreografadas. Finalmente um herói novo que empolga!"},
    {"id": 2, "comentario": "WandaVision foi uma série inovadora, cheia de simbolismos e com atuações brilhantes, especialmente da Elizabeth Olsen."},
    {"id": 3, "comentario": "Loki expandiu o multiverso de forma genial! Tom Hiddleston está impecável no papel."},
    {"id": 4, "comentario": "O Homem-Aranha: Sem Volta Para Casa foi pura nostalgia! A aparição dos três Homens-Aranha foi épica!"},
    {"id": 5, "comentario": "Pantera Negra: Wakanda Para Sempre fez uma linda homenagem a Chadwick Boseman e emocionou do começo ao fim."},
    {"id": 6, "comentario": "Guardiões da Galáxia Vol. 3 trouxe um encerramento perfeito para a equipe! Humor, emoção e ação na medida certa."},
    {"id": 7, "comentario": "A introdução do Kang em Homem-Formiga e a Vespa: Quantumania foi um dos melhores momentos das novas fases!"},
    {"id": 8, "comentario": "Desde Ultimato, o MCU perdeu o rumo. Muitos filmes e séries sem conexão e sem impacto real no universo."},
    {"id": 9, "comentario": "Doutor Estranho no Multiverso da Loucura prometeu muito e entregou pouco. A história ficou bagunçada e Wanda foi mal aproveitada."},
    {"id": 10, "comentario": "Thor: Amor e Trovão foi uma decepção! Exageraram no humor e o vilão do Christian Bale foi mal explorado."},
    {"id": 11, "comentario": "Cavaleiro da Lua começou bem, mas o final foi apressado e sem grandes consequências para o MCU."},
    {"id": 12, "comentario": "Invasão Secreta tinha potencial para ser uma série épica de espionagem, mas virou um desperdício de tempo."},
    {"id": 13, "comentario": "A Fase 4 da Marvel pareceu sem direção. Muitos personagens novos, mas sem uma história realmente cativante."},
    {"id": 14, "comentario": "A CGI está piorando a cada produção. Quantumania parecia um jogo de PS3 em alguns momentos!"},
    {"id": 15, "comentario": "A Fase 4 da Marvel trouxe muitas séries e filmes, explorando novos personagens e expandindo o multiverso."},
    {"id": 16, "comentario": "Alguns amam o novo estilo da Marvel, outros acham que perdeu a magia. Depende muito do que você espera do MCU."},
    {"id": 17, "comentario": "Desde Ultimato, a Marvel está focando mais em séries no Disney+, o que pode ser bom para aprofundar personagens."},
    {"id": 18, "comentario": "A introdução do multiverso trouxe novas possibilidades, mas também tornou a história mais complexa e difícil de acompanhar."},
    {"id": 19, "comentario": "Muitos filmes da Fase 4 e 5 focam em diversidade e representatividade, o que agrada alguns fãs e desagrada outros."},
    {"id": 20, "comentario": "Com a chegada do Kang, a Marvel parece estar preparando um novo grande evento, mas ainda não sabemos se será tão grandioso quanto Ultimato."},
    {"id": 21, "comentario": "Homem-Aranha: Sem Volta Para Casa trouxe uma das melhores experiências de cinema dos últimos anos!"},
    {"id": 22, "comentario": "Ms. Marvel foi uma surpresa agradável! Ótima representatividade e uma vibe divertida."},
    {"id": 23, "comentario": "A trilha sonora de Wakanda Para Sempre foi simplesmente espetacular!"},
    {"id": 24, "comentario": "A atuação de Jonathan Majors como Kang foi incrível, ele realmente impõe presença!"},
    {"id": 25, "comentario": "A conexão entre Loki e o multiverso foi muito bem feita e deixou um gostinho de quero mais."},
    {"id": 26, "comentario": "Thor: Amor e Trovão parecia mais uma paródia do que um filme sério do MCU."},
    {"id": 27, "comentario": "Muitos efeitos especiais da Fase 5 parecem apressados, prejudicando a imersão."},
    {"id": 28, "comentario": "A Marvel está exagerando no número de produções, o que torna difícil acompanhar tudo."},
    {"id": 29, "comentario": "Não há mais o mesmo impacto emocional nos filmes da Marvel desde Ultimato."},
    {"id": 30, "comentario": "Quantumania tentou ser grandioso, mas o roteiro foi fraco e sem emoção."},
    {"id": 31, "comentario": "A qualidade das séries da Marvel varia bastante, algumas são incríveis, outras decepcionam."},
    {"id": 32, "comentario": "O futuro do MCU parece incerto, mas a Saga do Multiverso pode surpreender."},
    {"id": 33, "comentario": "Alguns personagens novos são interessantes, mas falta um foco maior na narrativa geral."},
    {"id": 34, "comentario": "As séries no Disney+ trouxeram um novo formato para o MCU, mas nem todas foram bem aproveitadas."},
    {"id": 35, "comentario": "O CGI em alguns filmes é ótimo, mas em outros deixa a desejar, dependendo do orçamento."},
    {"id": 36, "comentario": "Gavião Arqueiro trouxe uma história leve e divertida, e a introdução da Kate Bishop foi ótima!"},
    {"id": 37, "comentario": "Eu amei a série do Cavaleiro da Lua! Oscar Isaac entregou uma performance incrível!"},
    {"id": 38, "comentario": "Doutor Estranho no Multiverso da Loucura teve uma direção fantástica de Sam Raimi, cheia de identidade!"},
    {"id": 39, "comentario": "A química entre Tom Holland e Zendaya faz toda a diferença nos filmes do Homem-Aranha."},
    {"id": 40, "comentario": "What If? explorou histórias alternativas muito criativas e expandiu o conceito do multiverso."},
    {"id": 41, "comentario": "A Marvel está apostando demais em humor exagerado, o que torna alguns filmes cansativos."},
    {"id": 42, "comentario": "A morte do T’Challa deixou um vazio na história do MCU que não foi bem resolvido."},
    {"id": 43, "comentario": "Secret Invasion poderia ter sido um thriller político épico, mas foi muito mal executado."},
    {"id": 44, "comentario": "She-Hulk tentou inovar, mas a quebra de quarta parede ficou forçada e sem graça."},
    {"id": 45, "comentario": "Eternos trouxe muitos personagens novos de uma vez, dificultando a conexão com o público."},
    {"id": 46, "comentario": "As produções do MCU estão mais diversificadas, o que pode ser positivo ou negativo, dependendo do público."},
    {"id": 47, "comentario": "O conceito de variantes foi bem introduzido, mas às vezes confunde o espectador casual."},
    {"id": 48, "comentario": "As séries têm explorado personagens secundários de maneira interessante."},
    {"id": 49, "comentario": "Com tantas produções, fica difícil saber quais são realmente essenciais para a trama geral do MCU."},
    {"id": 50, "comentario": "O hype em torno dos filmes da Marvel diminuiu, mas ainda há expectativa para os próximos lançamentos."}
]

app = Flask(__name__)

@app.route('/comentarios', methods=['GET'])
def buscar_comentarios():
    return jsonify(comentarios)

@app.route('/comentarios/<int:id>', methods=['GET'])
def buscar_comentario_por_id(id):
    for comentario in comentarios:
        if comentario.get("id") == id:
            return comentario
        
@app.route('/analisar', methods=['GET'])
def analisar_comentarios():
    resultado_json = []
    for comentario in comentarios:
        texto = comentario.get("comentario")
        resultado = analisar_sentimento(texto)

        maior_avaliacao = None
        maior_score = 0
        for item in resultado[0]:
            if item.get('score') >= maior_score:
                maior_avaliacao = item.get('label')
                maior_score = item.get('score')

        resultado_json.append({"comentario": texto, "avaliação": maior_avaliacao})
    return jsonify(resultado_json)

@app.route('/analisar/<int:id>', methods=['GET'])
def analisar_comentario_por_id(id):
    resultado_json = []
    for comentario in comentarios:
        if comentario.get("id") == id:
            texto = comentario.get("comentario")
            resultado = analisar_sentimento(texto)
            maior_avaliacao = None
            maior_score = 0
            for item in resultado[0]:
                if item.get('score') >= maior_score:
                    maior_avaliacao = item.get('label')
                    maior_score = item.get('score')

            resultado_json.append({"comentario": texto, "avaliação": maior_avaliacao})
        return jsonify(resultado_json)

def analisar_sentimento(texto):
    response = requests.post(API_URL, headers=headers, json={"inputs": texto})
    return response.json()

app.run(port=5001, host='localhost', debug=True)
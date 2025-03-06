from flask import Flask, jsonify, request

# API é um lugar para disponibilizar recursos e/ou funcionalidades

# 1. Objetivo - Criar uma API para o CRUD de livros
# 2. URL Base - localhost
# 3. Endpoints 
#   - localhost/livros (GET)
#   - localhost/livros/id (GET)
#   - localhost/livros (POST)
#   - localhost/livros/id (PUT)
#   - localhost/livros/id (DELETE)
# 4. Recursos - Livros

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'Harry Potter e a Pedra Filosofal',
        'autor': 'J.K. Rowling'
    },
    {
        'id': 2,
        'titulo': 'Harry Potter e a Câmara Secreta',
        'autor': 'J.K. Rowling'
    },
    {
        'id': 3,
        'titulo': 'Harry Potter e o Prisioneiro de Azkaban',
        'autor': 'J.K. Rowling'
    },
]

@app.route('/livros', methods=['GET'])
def obter_livros():
    """ CONSULTAR TODOS OS LIVROS """
    return jsonify(livros)

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    """ CONSULTAR UM ÚNICO LIVRO PELO ID """
    for livro in livros:
        if livro.get('id') == id:
            return jsonify(livro)
        
@app.route('/livros', methods=['POST'])
def incluir_novo_livro():
    """ INCLUIR NOVO LIVRO """
    novo_livro = request.get_json()
    livros.append(novo_livro)
    return jsonify(livros)
        
@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro(id):
    """ EDITAR LIVRO USANDO O ID PARA BUSCÁ-LO """
    livro_alterado = request.get_json()
    for i, livro in enumerate(livros):
        if livro.get('id') == id:
            livros[i].update(livro_alterado)
            return jsonify(livro)
        
@app.route('/livros/<int:id>', methods=['DELETE'])
def excluir_livro(id):
    for i, livro in enumerate(livros):
        if livro.get('id') == id:
            del livros[i]
            return jsonify(livro)
    return jsonify(livros)

app.run(port=5000, host='localhost', debug=True)
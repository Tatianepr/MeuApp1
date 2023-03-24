from flask import Flask, request, send_from_directory, render_template, jsonify, make_response
from sqlalchemy.exc import IntegrityError
from model import Session, Produto
from model.comentario import Comentario
from app import app



@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


@app.route('/add_produto', methods=['POST'])
def add_produto():
    session = Session()
    produto = Produto(
        nome=request.form.get("nome"),
        quantidade=request.form.get('quantidade'),
        valor=request.form.get('valor')
    )
    try:
        # para adicionar o produto
        session.add(produto)
        # efetivar o comando de adição na tabela
        session.commit()
        msg = {
            'id': produto.id,
            'nome': produto.nome,
            'quantidade': produto.quantidade,
            'valor': produto.valor
        }
        response = make_response(jsonify({"message": msg}),200)
        response.headers["Content-Type"] = "application/json"
        return response

    except IntegrityError as e:
        error_msg = 'Produto de mesmo nome já salvo na base.'
        response = make_response(jsonify({"message": error_msg}), 409)
        response.headers["Content-Type"] = "application/json"
        return response

    except Exception as e:
        error_msg = 'Não foi possível adicionar o item.'
        print(str(e))
        response = {
            'message': error_msg
        }

        response = make_response(jsonify({"message": error_msg}), 400)
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/get_produto/<produto_id>', methods=['GET'])
def get_produto(produto_id):
    session = Session()
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        error_msg = 'Produto não encontrado'
        response = make_response(jsonify({"message": error_msg}), 409)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        msg = {
            'id': produto.id,
            'nome': produto.nome,
            'quantidade': produto.quantidade,
            'valor': produto.valor,
            'total_comentarios': len(produto.comentarios),
            'comentarios': [{
                'autor':comentario.autor,
                'texto': comentario.texto,
                'estrelas': comentario.n_estrelas
            } for comentario in produto.comentarios]
        }

    response = make_response(jsonify({"message": msg}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/del_produto/<produto_id>', methods=['DELETE'])
def del_produto(produto_id):
    session = Session()

    comentario = session.query(Comentario).filter(
        Comentario.produto == produto_id).first()

    if comentario:
        count = session.query(Comentario).filter(
            Comentario.produto == produto_id).delete()
        session.commit()

    count = session.query(Produto).filter(Produto.id == produto_id).delete()
    session.commit()
    print(count)

    if count == 1:
        msg = 'Produto deletado'
        response = make_response(jsonify({'msg': msg}, 200))
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        error_msg = 'Produto não existe'
        response = make_response(jsonify({"message": error_msg}), 400)
        response.headers["Content-Type"] = "application/json"
        return response


@app.route('/add_comentario/<produto_id>', methods=['POST'])
def add_comentario(produto_id):
    session = Session()
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        error_msg = "Produto não encontrado na base :/"
        response = make_response(jsonify({'error': error_msg}, 404))
        return response

    autor = request.form.get('autor')
    texto = request.form.get('texto')
    n_estrelas = request.form.get('estrelas')

    if n_estrelas:
        n_estrelas = int(n_estrelas)

    comentario = Comentario(autor, texto, n_estrelas)
    produto.adiciona_comentario(comentario)
    session.commit()

    msg = {
        'message': 'Comentário adicionado com sucesso',
        'id': produto.id,
        'nome': produto.nome,
        'quantidade': produto.quantidade,
        'valor': produto.valor,
        'total_comentarios': len(produto.comentarios),
        'comentarios': [{
            'autor': comentario.autor,
            'texto': comentario.texto,
            'estrelas': comentario.n_estrelas
        } for comentario in produto.comentarios]
    }

    response = make_response(jsonify({"message": msg}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


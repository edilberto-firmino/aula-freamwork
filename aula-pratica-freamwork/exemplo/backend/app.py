from contextlib import closing
from pathlib import Path
import re
import sqlite3

from flask import Flask, jsonify, request

BASE = Path(__file__).resolve().parent


def criar_app(caminho_banco=None):
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024
    caminho = Path(caminho_banco) if caminho_banco else BASE / 'cadastros.db'

    def conectar():
        banco = sqlite3.connect(caminho)
        banco.row_factory = sqlite3.Row
        return banco

    with closing(conectar()) as banco, banco:
        banco.execute('''CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL CHECK(length(trim(nome)) BETWEEN 2 AND 80),
            email TEXT NOT NULL UNIQUE COLLATE NOCASE,
            curso TEXT NOT NULL CHECK(length(trim(curso)) BETWEEN 2 AND 80)
        )''')

    @app.get('/api/alunos')
    def listar():
        with closing(conectar()) as banco:
            linhas = banco.execute(
                'SELECT id, nome, email, curso FROM alunos ORDER BY id DESC'
            ).fetchall()
        return jsonify([dict(linha) for linha in linhas])

    @app.post('/api/alunos')
    def cadastrar():
        dados = request.get_json(silent=True)
        if not isinstance(dados, dict):
            return jsonify(erro='Envie um objeto JSON válido.'), 400
        campos = ('nome', 'email', 'curso')
        if any(not isinstance(dados.get(campo), str) for campo in campos):
            return jsonify(erro='Nome, e-mail e curso devem ser textos.'), 400
        nome, email, curso = (dados[campo].strip() for campo in campos)
        email = email.lower()
        if not (2 <= len(nome) <= 80 and 2 <= len(curso) <= 80):
            return jsonify(erro='Nome e curso precisam ter de 2 a 80 caracteres.'), 400
        if len(email) > 120 or not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            return jsonify(erro='Informe um e-mail válido com até 120 caracteres.'), 400
        try:
            with closing(conectar()) as banco, banco:
                cursor = banco.execute(
                    'INSERT INTO alunos (nome, email, curso) VALUES (?, ?, ?)',
                    (nome, email, curso),
                )
                aluno_id = cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            if erro.sqlite_errorname == 'SQLITE_CONSTRAINT_UNIQUE':
                return jsonify(erro='Este e-mail já está cadastrado.'), 409
            raise
        return jsonify(id=aluno_id, nome=nome, email=email, curso=curso), 201

    @app.errorhandler(413)
    def muito_grande(erro):
        return jsonify(erro='O corpo da requisição excedeu o limite.'), 413

    return app


if __name__ == '__main__':
    criar_app().run(host='127.0.0.1', port=3000, debug=False)

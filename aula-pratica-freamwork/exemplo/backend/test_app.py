import tempfile
import unittest
from pathlib import Path

from app import criar_app


class CadastroTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.banco = Path(self.temp.name) / 'teste.db'
        self.client = criar_app(self.banco).test_client()

    def tearDown(self):
        self.temp.cleanup()

    def aluno(self, **mudancas):
        return dict(nome="Ana d'Ávila", email='ana@example.com', curso='Computação', **mudancas)

    def test_lista_vazia(self):
        resposta = self.client.get('/api/alunos')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json, [])

    def test_cadastro_normalizacao_e_persistencia(self):
        dados = self.aluno()
        dados['email'] = ' ANA@EXAMPLE.COM '
        resposta = self.client.post('/api/alunos', json=dados)
        self.assertEqual(resposta.status_code, 201)
        self.assertEqual(resposta.json['email'], 'ana@example.com')
        outra = criar_app(self.banco).test_client()
        self.assertEqual(outra.get('/api/alunos').json, [resposta.json])

    def test_duplicidade(self):
        self.client.post('/api/alunos', json=self.aluno())
        dados = self.aluno()
        dados['email'] = 'ANA@example.com'
        self.assertEqual(self.client.post('/api/alunos', json=dados).status_code, 409)
        self.assertEqual(len(self.client.get('/api/alunos').json), 1)

    def test_entradas_invalidas(self):
        for dados in [[], {}, {'nome': 12}, {**self.aluno(), 'nome': ' '},
                      {**self.aluno(), 'email': 'sem-arroba'},
                      {**self.aluno(), 'curso': 'x' * 81}]:
            with self.subTest(dados=dados):
                self.assertEqual(self.client.post('/api/alunos', json=dados).status_code, 400)
        resposta = self.client.post('/api/alunos', data='{', content_type='application/json')
        self.assertEqual(resposta.status_code, 400)

    def test_texto_html_preservado(self):
        dados = {**self.aluno(), 'nome': '<b>Ana</b>'}
        self.assertEqual(self.client.post('/api/alunos', json=dados).json['nome'], '<b>Ana</b>')

    def test_limite_corpo(self):
        resposta = self.client.post('/api/alunos', data='x' * 17000, content_type='application/json')
        self.assertEqual(resposta.status_code, 413)


if __name__ == '__main__':
    unittest.main()

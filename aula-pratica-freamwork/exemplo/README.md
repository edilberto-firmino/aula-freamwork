# Cadastro de alunos com React, Flask e SQLite

Exemplo da aula prática 5. Use dados fictícios. React executa a interface; Flask recebe e valida as requisições; SQLite persiste os registros.

## Requisitos

- Python 3.11 ou superior.
- Node.js 22.12 ou superior e npm.
- Internet para instalar dependências.

## Terminal 1 — backend

Abra o terminal na raiz desta pasta. No PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Confira http://127.0.0.1:3000/api/alunos. Um banco novo retorna `[]`.
Se `py` não existir, use `python`. No Linux/macOS, crie a venv com `python3` e execute por `.venv/bin/python`.

## Terminal 2 — frontend

Abra outro terminal na raiz desta pasta:

```powershell
cd frontend
npm.cmd ci
npm.cmd run dev
```

Abra http://127.0.0.1:5173. Deixe os dois processos executando. Se estiver montando os arquivos manualmente e ainda não houver package-lock.json, use `npm.cmd install` no lugar de `ci`. No Linux/macOS, use `npm`.

O proxy do Vite encaminha `/api` para a porta 3000. A raiz da porta 3000 não entrega a tela. Não use Live Server nem abra frontend/index.html com duplo clique.

## Testar

1. Cadastre Ana Souza / ana@example.com / Computação.
2. Confira a lista e o contador. Filtre por Ana.
3. Tente o mesmo e-mail: deve aparecer a mensagem de duplicidade (HTTP 409).
4. Recarregue a página e confirme que o aluno continua.
5. Pare e reinicie o backend com Ctrl+C; atualize a lista e confirme a persistência.
6. Envie JSON inválido diretamente à API; espere 400.
7. Use Tab e Enter para conferir a navegação por teclado.

Testes automatizados, dentro de backend (bancos temporários):

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

Build, dentro de frontend:

```powershell
npm.cmd run build
```

`dist` contém somente o frontend. O proxy foi definido para o servidor de desenvolvimento (`npm.cmd run dev`); servir o build exige configurar o encaminhamento da API. Esta prática não inclui implantação.

## Retomar e preservar o banco

Após a primeira instalação, basta iniciar app.py e executar npm.cmd run dev. O banco fica em backend/cadastros.db e é criado automaticamente. Não o apague para reiniciar.

Para trazer os dados da aula anterior, pare os servidores, faça backup e copie o banco de mesmo esquema para backend/cadastros.db. Não coloque o banco em frontend. Não envie dados pessoais, .venv ou node_modules ao repositório.

## Rotas

| Método | Rota | Resposta |
| --- | --- | --- |
| GET | /api/alunos | 200, array de alunos |
| POST | /api/alunos | 201, aluno com id |

POST recebe nome, email e curso como strings. Nome e curso: 2 a 80 caracteres após trim; e-mail: formato básico e até 120 caracteres. E-mail é normalizado em minúsculas. Erros: 400 para dados inválidos, 409 para duplicidade e 413 para corpo acima de 16 KiB.

## Organização

- backend/app.py: rotas, validação e SQL com parâmetros.
- frontend/src/App.jsx: estado compartilhado e consulta inicial.
- frontend/src/api.js: fetch e tratamento de respostas HTTP.
- frontend/src/components: formulário controlado e lista com filtro.
- frontend/vite.config.js: porta fixa e proxy.

Referências: https://react.dev/learn · https://vite.dev/guide/ · https://flask.palletsprojects.com/ · https://docs.python.org/3/library/sqlite3.html

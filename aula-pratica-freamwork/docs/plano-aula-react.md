# Aula prática 5: React, API e SQLite

Objetivo: dar continuidade ao cadastro de alunos da aula 4 com um manual HTML autônomo, em português, e um exemplo executável. Autorização: usuário pediu para fazer o novo conteúdo após a análise da aula anterior.

Decisões: React com JavaScript e Vite; manter Flask e SQLite para concentrar o aprendizado na interface. API em 127.0.0.1:3000 e Vite em 127.0.0.1:5173 com proxy /api. Cadastro e consulta como escopo principal; contador e filtro como aplicação de estado derivado. Sem login ou exclusão nesta aula.

Alternativas: Express permitiria uma linguagem só, mas mudaria o percurso principal anterior; manter Flask preserva a API e o banco. Escolha técnica do implementador.

## Etapas
- [ ] Escrever testes de contrato da API, validação e persistência em banco temporário; confirmar falha inicial.
- [ ] Criar exemplo/backend/app.py, requirements.txt e exemplo/frontend com componentes React, estados, fetch e proxy.
- [ ] Criar index.html com conceitos, roteiro de 180 minutos, comandos PowerShell, código integral, diagnóstico, atividade, avaliação e referências oficiais. Gerar blocos diretamente dos arquivos do exemplo.
- [ ] Instalar dependências, executar testes da API e build do frontend; conferir recursos e links do manual e empacotar exemplo sem dependências ou dados.

Verificação: GET vazio, POST 201, validação 400, duplicidade 409, corpo grande 413, nome com apóstrofo e texto HTML, persistência entre instâncias. Build React e teste HTTP pelo proxy. Revisão visual do manual se navegador disponível.

"""Gera o manual com os arquivos reais do exemplo, sem dependências externas."""
from pathlib import Path
from html import escape
import zipfile

BASE = Path(__file__).resolve().parent
partes = []
menu = []


def secao(numero, titulo, conteudo):
    menu.append(f'<a href="#s{numero}"><span>{numero:02}</span> {titulo}</a>')
    partes.append(f'<section id="s{numero}"><p class="eyebrow">PASSO {numero:02}</p><h2>{titulo}</h2>{conteudo}</section>')


def terminal(texto):
    return '<div class="code-head">TERMINAL · PowerShell · uma linha por vez</div><pre><code>' + escape(texto.strip()) + '</code></pre>'


def arquivo(caminho):
    texto = (BASE / 'exemplo' / caminho).read_text(encoding='utf-8')
    return f'<div class="code-head"><span>{escape(caminho)}</span><a href="exemplo/{caminho}" download>Baixar arquivo</a><button class="copiar" type="button">Copiar</button></div><pre><code>{escape(texto)}</code></pre>'


secao(1, 'O que vamos construir', '''
<p>Na aula anterior, o JavaScript procurava elementos no HTML e alterava a lista manualmente. Nesta aula, vamos reconstruir o cadastro de alunos com <strong>React</strong>. A interface terá formulário, lista, contador, filtro e mensagens de carregamento, sucesso e erro.</p>
<p>O contrato continua o mesmo: <code>nome</code>, <code>email</code> e <code>curso</code>. O backend valida e grava em SQLite. O frontend não abre o arquivo do banco.</p>
<div class="note"><strong>Objetivo da aula:</strong> explicar e demonstrar o caminho de um cadastro, do evento no React até a gravação no SQLite e sua exibição na tela. Use somente dados fictícios.</div>
<p>Escopo principal: criar e consultar registros. Login, edição, exclusão e publicação ficam fora desta prática. React é uma biblioteca de interfaces; Vite é a ferramenta que prepara e serve o frontend durante o desenvolvimento.</p>
<h3>Ao final, você conseguirá</h3><ul><li>Separar a interface em componentes e transmitir dados por props.</li><li>Controlar campos, lista e mensagens com <code>useState</code>.</li><li>Carregar dados com <code>useEffect</code> e enviar JSON com <code>fetch</code>.</li><li>Identificar se uma falha está no React, no HTTP ou no SQLite.</li></ul>''')

secao(2, 'Roteiro de 180 minutos', '''
<div class="table-wrap"><table><thead><tr><th>Tempo</th><th>Etapa</th><th>Evidência</th></tr></thead><tbody>
<tr><td>0–20 min</td><td>Revisar as camadas e entender React</td><td>Desenhar o fluxo dos dados</td></tr>
<tr><td>20–45 min</td><td>Preparar e testar Flask + SQLite</td><td>GET retorna []</td></tr>
<tr><td>45–70 min</td><td>Preparar Vite e a entrada React</td><td>Abrir a interface na porta 5173</td></tr>
<tr><td>70–125 min</td><td>Estudar e montar os componentes</td><td>Cadastrar e listar um aluno</td></tr>
<tr><td>125–155 min</td><td>Testar erro, filtro e persistência</td><td>409 e registro após reinício</td></tr>
<tr><td>155–180 min</td><td>Personalizar, explicar e entregar</td><td>Código e evidências</td></tr>
</tbody></table></div><p>Em dupla, alternem quem digita e quem explica. Para duas aulas, encerre a primeira com backend e estrutura React prontos. Retome pelos componentes e testes.</p>''')

secao(3, 'Da aula anterior para React', '''
<div class="table-wrap"><table><thead><tr><th>Antes</th><th>Agora</th></tr></thead><tbody>
<tr><td>HTML da página</td><td>JSX retornado por componentes</td></tr>
<tr><td>querySelector e textContent</td><td>Estado e expressões no JSX</td></tr>
<tr><td>addEventListener('submit')</td><td>onSubmit={enviar}</td></tr>
<tr><td>createElement e append</td><td>alunos.map(...) com key</td></tr>
<tr><td>form.reset()</td><td>Atualizar o estado dos campos</td></tr>
<tr><td>fetch, API e SQLite</td><td>Continuam com a mesma função</td></tr>
</tbody></table></div><p><strong>Componente</strong> é uma função que retorna a interface. <strong>JSX</strong> é a sintaxe de marcação dentro do JavaScript. <strong>Props</strong> são dados recebidos do componente pai. <strong>Estado</strong> é a memória que influencia a renderização.</p>
<p>Use <code>className</code> no lugar de <code>class</code> e <code>htmlFor</code> no lugar de <code>for</code>. Expressões JavaScript ficam entre chaves. Nomes de componentes começam com maiúscula.</p>
<div class="note">Não modifique arrays de estado com <code>push</code>. Crie um novo array e chame o setter. Atualizar o estado solicita uma nova renderização; não altera imediatamente a variável da função em execução.</div>''')

secao(4, 'Entender as portas e o proxy', '''
<div class="flow"><div><b>React + Vite</b><span>Navegador · porta 5173</span></div><i>↓ /api</i><div><b>Proxy do Vite</b><span>Encaminha a requisição</span></div><i>↓ HTTP</i><div><b>Flask</b><span>API · porta 3000</span></div><i>↓ SQL com parâmetros</i><div><b>SQLite</b><span>backend/cadastros.db</span></div></div>
<p>O navegador pede <code>/api/alunos</code> à porta 5173. O Vite encaminha para <code>http://127.0.0.1:3000/api/alunos</code>. A resposta JSON faz o caminho de volta. Isso evita configurar CORS nesta prática.</p>
<p><strong>Dois terminais ficam abertos:</strong> um para Flask e outro para Vite. Node executa as ferramentas do frontend; Python executa a API. O SQLite acompanha o Python.</p>
<table><thead><tr><th>Rota da API</th><th>Resultado</th></tr></thead><tbody><tr><td>GET /api/alunos</td><td>200 e array de alunos</td></tr><tr><td>POST /api/alunos</td><td>201 e novo aluno; 400 para dados inválidos; 409 para e-mail repetido</td></tr></tbody></table>
<p>A raiz da porta 3000 pode retornar 404: este backend entrega apenas a API. A tela fica na porta 5173.</p>''')

secao(5, 'Preparar as ferramentas', '''
<p>Use VS Code, Python 3.11 ou superior e Node.js 22.12 ou superior. Os comandos desta aula usam PowerShell. Confira antes de criar arquivos:</p>''' + terminal('py --version\npy -m pip --version\nnode --version\nnpm.cmd --version') + '''
<p>Se <code>py</code> não existir, tente <code>python</code> e use esse nome nos próximos comandos. Instale pelas páginas oficiais e reabra o terminal depois. <code>npm.cmd</code> evita o bloqueio de <code>npm.ps1</code> no PowerShell.</p>
<p>As dependências do exemplo estão fixadas em <code>package.json</code> e <code>requirements.txt</code>. Para reproduzir o frontend entregue, use o <code>package-lock.json</code> com <code>npm.cmd ci</code>. Não precisa instalar React, Vite ou SQLite globalmente.</p>
<div class="note">É necessário acesso à internet para instalar dependências. Não copie a pasta .venv nem node_modules de outro computador.</div>''')

secao(6, 'Organizar o projeto', '''
<p>Escolha um caminho: <strong>acompanhar digitando</strong> ou <strong>executar o exemplo pronto</strong>. No primeiro, crie uma pasta nova, abra-a no VS Code e execute:</p>''' + terminal('mkdir cadastro-alunos-react\ncd cadastro-alunos-react\nmkdir backend\nmkdir frontend\nmkdir frontend/src\nmkdir frontend/src/components') + '''
<pre><code>cadastro-alunos-react/
  .gitignore
  backend/
    app.py
    requirements.txt
    test_app.py          # opcional: testes automatizados
    cadastros.db         # criado pelo backend
    .venv/              # criado pelo Python
  frontend/
    index.html
    package.json
    package-lock.json   # gerado pelo npm / incluído no exemplo
    vite.config.js
    src/
      main.jsx
      App.jsx
      api.js
      style.css
      components/
        FormularioAluno.jsx
        ListaAlunos.jsx</code></pre>
<p>Para usar o exemplo pronto, baixe <a href="cadastro-alunos-react.zip" download>o projeto ZIP</a>, extraia e abra a pasta <code>cadastro-alunos-react</code> no VS Code. Pule os comandos de criação de pastas e a cópia dos arquivos; siga a instalação do backend e do frontend.</p>
<p>Este <code>index.html</code> é o manual. O <code>frontend/index.html</code> do projeto é a entrada da aplicação. Abrir esse segundo arquivo com duplo clique não executa React.</p>''' + arquivo('.gitignore'))

secao(7, 'Preparar o backend e o SQLite', '''
<p>Vamos preservar o percurso Python/Flask da aula anterior. Crie os dois arquivos abaixo dentro de <code>backend</code>. O backend prepara a tabela quando <code>criar_app()</code> é chamado.</p>''' + arquivo('backend/requirements.txt') + arquivo('backend/app.py') + '''
<h3>Leia antes de executar</h3><ul><li><code>criar_app</code> organiza a inicialização e permite testar com um banco temporário.</li><li><code>Path(__file__)</code> mantém o banco ao lado de app.py, independentemente da pasta do terminal.</li><li><code>with banco</code> confirma a transação no sucesso e reverte em caso de erro; <code>closing</code> fecha a conexão.</li><li>Os <code>?</code> recebem valores separados do SQL. Nunca monte SQL concatenando os campos.</li><li>O e-mail é normalizado e tem restrição UNIQUE. A validação do servidor continua obrigatória.</li></ul>
<p>Para reaproveitar dados da aula anterior, pare o backend antigo, faça uma cópia de segurança e copie o <code>cadastros.db</code> para <code>backend</code>. A tabela precisa ter o mesmo esquema. Não mova o banco para frontend. Sem essa cópia, esta aula inicia um banco novo.</p>''')

secao(8, 'Iniciar e testar a API', '''
<p>No <strong>terminal 1</strong>, começando na raiz do projeto:</p>''' + terminal('cd backend\npy -m venv .venv\n.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt\n.\\.venv\\Scripts\\python.exe app.py') + '''
<p>Deixe esse terminal aberto. Acesse <a href="http://127.0.0.1:3000/api/alunos">http://127.0.0.1:3000/api/alunos</a>. Resultado esperado em banco novo: <code>[]</code>. Confira se <code>backend/cadastros.db</code> apareceu.</p>
<p>Não é necessário ativar a .venv. Usar o executável diretamente evita problemas de política do PowerShell. Para parar, pressione Ctrl+C.</p>
<details><summary>Linux e macOS</summary>''' + terminal('cd backend\npython3 -m venv .venv\n.venv/bin/python -m pip install -r requirements.txt\n.venv/bin/python app.py') + '''<p>Nos comandos do frontend, use <code>npm</code> no lugar de <code>npm.cmd</code>.</p></details>''')

secao(9, 'Preparar React com Vite', '''
<p>Salve estes arquivos em <code>frontend</code>. Esta aula usa uma configuração mínima montada manualmente: não execute também um gerador de projeto sobre esta pasta.</p>''' + arquivo('frontend/package.json') + arquivo('frontend/vite.config.js') + arquivo('frontend/index.html') + '''
<p><code>type: module</code> permite import/export. O Vite transforma os arquivos JSX. <code>jsx: automatic</code> configura a transformação sem exigir importação do objeto React em cada componente. Nesta configuração mínima, não usamos o plugin React; mudanças podem recarregar a tela e reiniciar o estado local.</p>
<p><code>strictPort: true</code> impede o Vite de trocar de porta silenciosamente. O proxy só existe no servidor de desenvolvimento: ele não acompanha automaticamente os arquivos de build.</p>
<p>No <strong>terminal 2</strong>, aberto na raiz do projeto:</p>''' + terminal('cd frontend\nnpm.cmd install') + '''
<p>Esse comando instala as dependências e gera o lockfile. Se você extraiu o ZIP e já tem <code>package-lock.json</code>, use <code>npm.cmd ci</code> no lugar de install. Ainda faltam os arquivos de src; vamos criá-los antes de iniciar a tela.</p>''')

secao(10, 'Criar a entrada e a comunicação HTTP', arquivo('frontend/src/main.jsx') + '''
<p><code>createRoot</code> conecta React ao elemento <code>root</code>. <code>StrictMode</code> ajuda a identificar problemas durante o desenvolvimento. Ele pode executar um ciclo extra de configuração e limpeza de efeitos; não coloque cadastros POST no efeito inicial.</p>''' + arquivo('frontend/src/api.js') + '''
<p>O módulo centraliza o acesso HTTP. <code>fetch</code> não lança erro automaticamente para status 400 ou 409: por isso verificamos <code>resposta.ok</code>. <code>JSON.stringify</code> transforma o objeto em texto para envio.</p>
<p><code>signal</code> permite cancelar consultas antigas com AbortController. O caminho relativo <code>/api/alunos</code> passa pelo proxy; não o substitua pela porta 3000 no frontend sem tratar CORS.</p>''')

secao(11, 'Componente do formulário', '''
<p>Crie <code>FormularioAluno.jsx</code>. Cada campo tem <code>value</code> vindo do estado e <code>onChange</code> para atualizá-lo. Esse é um formulário controlado.</p>''' + arquivo('frontend/src/components/FormularioAluno.jsx') + '''
<h3>Entenda o fluxo</h3><ol><li>O usuário digita; <code>alterar</code> cria uma cópia de campos com o valor novo.</li><li>O submit chama <code>enviar</code>; <code>preventDefault</code> evita a navegação padrão.</li><li>O botão e os campos ficam desabilitados durante o envio.</li><li>A API valida e responde com o aluno salvo, incluindo o id.</li><li>A prop <code>aoCadastrar</code> avisa o componente pai; o formulário limpa o estado.</li><li>Um erro mantém os valores digitados e exibe uma mensagem.</li></ol>
<p><code>useRef</code> mantém uma trava imediata entre renderizações, sem renderizar a tela ao mudar. <code>useState</code> continua responsável pela aparência do botão. Os hooks ficam no topo do componente, nunca dentro de condições ou loops.</p>
<p><code>required</code> e os limites ajudam o usuário; requisições diretas podem ignorá-los. Por isso o backend faz as mesmas verificações.</p>''')

secao(12, 'Componente da lista', arquivo('frontend/src/components/ListaAlunos.jsx') + '''
<p>A lista recebe dados por props. <code>map</code> descreve um item para cada aluno e <code>key={aluno.id}</code> fornece uma identidade estável. Não use a posição no array como identidade de um registro.</p>
<p>O contador vem de <code>alunos.length</code>. O filtro é calculado com <code>filter</code> durante a renderização: não precisamos guardar outra cópia da lista em estado nem criar um efeito só para filtrar.</p>
<p>O total indica todos os registros carregados; filtrar altera apenas os itens visíveis. Os dados continuam no banco. Um nome como <code>&lt;b&gt;Ana&lt;/b&gt;</code> aparece como texto porque React escapa strings interpoladas. Não use <code>dangerouslySetInnerHTML</code> para esses campos.</p>''')

secao(13, 'Componente principal: juntar as partes', arquivo('frontend/src/App.jsx') + '''
<p><code>App</code> é dono do estado compartilhado. Ele passa a lista para <code>ListaAlunos</code> e a função <code>adicionar</code> para <code>FormularioAluno</code>. Esse fluxo permite que componentes irmãos compartilhem dados por meio do pai.</p>
<h3>Por que useEffect?</h3><p>A consulta inicial sincroniza a tela com um sistema externo: a API. O array vazio indica que o efeito não depende de valores reativos que mudam. A limpeza cancela uma consulta pendente quando o efeito é encerrado.</p>
<p><code>atualizar</code> usa setters e uma ref estáveis, sem ler estado de uma renderização anterior. Cada consulta cancela a anterior, evitando que uma resposta atrasada substitua uma lista mais recente. Ao cadastrar, cancelamos uma consulta anterior e inserimos o registro retornado pela API no estado.</p>
<div class="note">O POST pertence ao evento do formulário. O efeito inicial faz somente GET. No StrictMode você pode observar uma consulta cancelada seguida de outra: isso é esperado durante o desenvolvimento.</div>
<p>Depois de salvar, a lista é atualizada usando o objeto retornado pelo backend; o botão Atualizar lista faz uma nova consulta completa. Essa atualização local não substitui a persistência: recarregar a página permite verificá-la.</p>''')

secao(14, 'Estilizar e executar a interface', arquivo('frontend/src/style.css') + '''
<p>O CSS mantém o foco visível e adapta as duas colunas para uma em telas menores. Os componentes usam rótulos associados aos inputs e regiões de status para mensagens.</p>
<p>No terminal 2, dentro de frontend:</p>''' + terminal('npm.cmd run dev') + '''
<p>Abra <a href="http://127.0.0.1:5173">http://127.0.0.1:5173</a>. O terminal 1 precisa continuar executando Flask.</p>
<ol><li>Cadastre Ana Souza, ana@example.com, Sistemas de Informação.</li><li>Confira a mensagem de sucesso, o aluno e o contador.</li><li>Cadastre Bruno Lima com outro e-mail.</li><li>Digite Ana no filtro e observe a lista.</li><li>Limpe o filtro e clique em Atualizar lista.</li><li>Recarregue a página: os registros devem continuar.</li></ol>''')

secao(15, 'Inspecionar HTTP e o banco', '''
<p>Abra F12 → Rede/Network. Cadastre um aluno com e-mail novo. Inspecione o <code>POST /api/alunos</code>: o payload deve conter nome, email e curso; a resposta deve ter status 201 e incluir id.</p>
<p>A URL vista pelo navegador usa a porta 5173. O proxy conversa com Flask na 3000. O botão Atualizar lista gera GET com status 200.</p>
<p>Em um terceiro terminal, faça um teste direto da API:</p>''' + terminal('Invoke-RestMethod http://127.0.0.1:3000/api/alunos\n$aluno = @{ nome = "Carla Lima"; email = "carla@example.com"; curso = "Computação" } | ConvertTo-Json\nInvoke-RestMethod -Uri http://127.0.0.1:3000/api/alunos -Method Post -ContentType "application/json; charset=utf-8" -Body ([System.Text.Encoding]::UTF8.GetBytes($aluno))') + '''
<p>Repetir o envio deve resultar em 409. Isso comprova a restrição de e-mail único. O PowerShell pode mostrar esse status como erro de requisição: é o resultado esperado.</p>
<p>Para inspecionar o SQLite, abra <code>backend/cadastros.db</code> no DB Browser for SQLite, selecione Browse Data e a tabela alunos. Evite manter uma transação de edição aberta enquanto testa o sistema.</p>''')

secao(16, 'Testar comportamento e persistência', '''
<p>Marque cada item somente após observar o resultado. As marcações ficam apenas nesta página, sem salvar progresso.</p>
<div class="checklist">''' + ''.join(f'<label><input type="checkbox"> {x}</label>' for x in [
'API nova retorna lista vazia; interface mostra o estado vazio.',
'Cadastro válido recebe 201, aparece na tela e aumenta o contador.',
'Campos vazios são bloqueados pelo navegador.',
'JSON com nome vazio ou numérico recebe 400 no backend.',
'E-mail repetido, inclusive com diferença de maiúsculas, recebe 409 sem outra linha.',
"Nome com apóstrofo, como Ana d’Ávila, é salvo corretamente.",
'Texto <b>Ana</b> é exibido literalmente, sem virar marcação HTML.',
'Filtro altera os itens visíveis e mantém o total de cadastros.',
'Tab percorre os controles, Enter envia e o layout cabe no celular.',
'Parar Flask e atualizar a lista mostra erro; religar e atualizar recupera os dados.',
'Após parar e reiniciar Flask e Vite, os registros continuam no mesmo banco.',
]) + '''</div><p>Para testar o servidor sem a validação HTML, altere o objeto PowerShell: use nome vazio, um número no nome ou e-mail inválido. Não basta uma captura da página aberta: registre resultado esperado e observado.</p>
<h3>Testes automatizados opcionais</h3><p>O exemplo inclui <code>backend/test_app.py</code>. Os testes usam bancos temporários e não alteram seus cadastros. Dentro de backend:</p>''' + terminal('.\\.venv\\Scripts\\python.exe -m unittest -v') + '''
<p>Verifique também a geração dos arquivos do frontend, dentro de frontend:</p>''' + terminal('npm.cmd run build') + '''
<p>O build gera <code>dist</code>. Isso não publica a API nem leva o banco para o navegador. <code>npm.cmd run preview</code> serve para inspecionar o build local; o proxy deste exemplo foi configurado em <code>server</code>, para <code>npm.cmd run dev</code>. Para testar o sistema completo nesta aula, use dev.</p>''')

secao(17, 'Resolver os erros mais comuns', '''
<div class="table-wrap"><table><thead><tr><th>Sintoma</th><th>O que conferir</th></tr></thead><tbody>
<tr><td>node ou npm não encontrado</td><td>Instale Node compatível e reabra o VS Code.</td></tr>
<tr><td>npm.ps1 bloqueado</td><td>Use npm.cmd nos comandos do PowerShell.</td></tr>
<tr><td>Erro de versão / engines</td><td>Confira node --version e use Node 22.12 ou superior.</td></tr>
<tr><td>No module named flask</td><td>Instale e execute pelo mesmo Python da .venv.</td></tr>
<tr><td>404 na porta 3000</td><td>Use /api/alunos para API; a tela está na porta 5173.</td></tr>
<tr><td>Failed to fetch / ECONNREFUSED</td><td>Confira Flask no terminal 1, proxy e porta 3000.</td></tr>
<tr><td>Resposta inesperada / HTML em vez de JSON</td><td>Confira a rota /api, backend e vite.config.js. Reinicie Vite após mudar a configuração.</td></tr>
<tr><td>Tela branca</td><td>Leia Console, verifique imports, nomes dos arquivos e erros de JSX.</td></tr>
<tr><td>Porta ocupada</td><td>Pare o servidor anterior com Ctrl+C; Vite está configurado para exigir 5173.</td></tr>
<tr><td>Dois GETs no desenvolvimento</td><td>StrictMode verifica efeitos. A limpeza cancela a consulta anterior; não remova a proteção como correção.</td></tr>
<tr><td>Lista não acompanha uma mudança</td><td>Use o setter com novo array; não modifique o estado diretamente.</td></tr>
<tr><td>409 ao cadastrar</td><td>E-mail existente. Use outro e-mail.</td></tr>
<tr><td>database is locked</td><td>Feche transações de edição no visualizador do banco.</td></tr>
<tr><td>Dados desapareceram</td><td>Confira a cópia do projeto e backend/cadastros.db; não apague o banco ao reiniciar.</td></tr>
</tbody></table></div><p>Leia primeiro o terminal, depois Console e Rede. Identifique a camada da falha antes de mudar o código.</p>''')

secao(18, 'Atividade e desafios', '''
<h3>Atividade principal</h3><p>Personalize o cadastro para participantes de uma oficina. Altere título, cores e textos, mantendo o contrato nome/email/curso. Cadastre três pessoas fictícias e explique o fluxo do dado por cada componente e camada.</p>
<h3>Desafios progressivos</h3><ol><li>Mostrar “X de Y alunos” quando houver filtro, calculando os números a partir da lista.</li><li>Adicionar um filtro por curso sem nova consulta ao banco.</li><li>Separar o cabeçalho em outro componente com título recebido por prop.</li><li>Adicionar telefone: planejar a coluna no banco, migração, validação, API e campo controlado.</li><li>Implementar DELETE com confirmação e tratamento de 404; depois atualizar a lista por estado.</li><li>Implementar edição com PUT, preenchimento do formulário e teste de e-mail duplicado.</li></ol>
<p>Alterar CREATE TABLE IF NOT EXISTS não muda uma tabela existente. Faça backup e planeje ALTER TABLE quando adicionar uma coluna.</p>''')

secao(19, 'Entrega e avaliação', '''
<p>Entregue backend, frontend, .gitignore e README com instruções para instalar, iniciar e testar. Inclua package-lock.json e requirements.txt. Não entregue .venv, node_modules nem dados reais.</p>
<p>Anexe evidências de cadastro, duplicidade e persistência após reinício. Registre quais ações produzem GET e POST e quais somente mudam o estado no navegador.</p>
<table><thead><tr><th>Critério</th><th>Pontos</th></tr></thead><tbody><tr><td>Componentes, props e organização</td><td>2</td></tr><tr><td>Formulário controlado e uso correto de estado</td><td>2</td></tr><tr><td>GET/POST, mensagens e recuperação de falhas</td><td>2</td></tr><tr><td>Validação e persistência SQLite demonstradas</td><td>2</td></tr><tr><td>Acessibilidade, personalização e explicação do fluxo</td><td>2</td></tr></tbody></table>
<h3>Explique com suas palavras</h3><ul><li>Qual a diferença entre estado e props?</li><li>Por que o POST fica no evento, e não no efeito inicial?</li><li>Por que o filtro não precisa de um segundo array em estado?</li><li>Para que serve o proxy? Qual servidor grava no banco?</li><li>O que significam 200, 201, 400 e 409?</li><li>Qual arquivo precisa continuar existindo para preservar os dados?</li></ul>''')

secao(20, 'Encerrar, retomar e consultar', '''
<p>Pressione Ctrl+C nos dois terminais. Para retomar, abra a mesma pasta e execute os comandos abaixo em terminais separados. Não precisa reinstalar dependências a cada aula.</p>''' + terminal('cd backend\n.\\.venv\\Scripts\\python.exe app.py') + terminal('cd frontend\nnpm.cmd run dev') + '''
<p>Abra a porta 5173. Em outro computador, recrie a .venv, instale requirements.txt e use npm.cmd ci no frontend. Para preservar os registros fictícios, leve também uma cópia do banco, feita com o servidor parado.</p>
<div class="note">O manual pode ser hospedado como conteúdo estático. A aplicação completa depende de um backend executando e de armazenamento persistente. Para publicar um sistema real, será necessário definir implantação, acesso, proteção dos dados e backups. O servidor Flask desta prática é de desenvolvimento.</div>
<h3>Referências oficiais</h3><ul>
<li><a href="https://react.dev/learn">React: componentes, JSX, props e estado</a></li>
<li><a href="https://react.dev/learn/build-a-react-app-from-scratch">React: aplicação didática com ferramenta de build</a></li>
<li><a href="https://react.dev/reference/react/useEffect">React: useEffect e limpeza</a></li>
<li><a href="https://vite.dev/guide/">Vite: guia e requisitos</a></li>
<li><a href="https://vite.dev/config/server-options#server-proxy">Vite: proxy no desenvolvimento</a></li>
<li><a href="https://flask.palletsprojects.com/en/stable/quickstart/">Flask: rotas e respostas</a></li>
<li><a href="https://docs.python.org/3/library/sqlite3.html">Python: SQLite, parâmetros e transações</a></li>
<li><a href="https://developer.mozilla.org/pt-BR/docs/Web/API/Fetch_API/Using_Fetch">MDN: fetch</a></li>
<li><a href="https://nodejs.org/en/download">Node.js: instalação</a></li>
<li><a href="https://www.python.org/downloads/">Python: instalação</a></li>
</ul><p>Material preparado para a continuidade da aula prática 4. Data: 30 de outubro de 2026.</p>''')

css = '''
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:#f6f5f0;color:#23332f;font:16px/1.75 system-ui,sans-serif}a{color:#14634e;text-underline-offset:3px}button{font:inherit;cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #be7900;outline-offset:4px}.layout{display:grid;grid-template-columns:270px minmax(0,1fr);max-width:1540px;margin:auto}aside{padding:35px 24px;border-right:1px solid #d8ded5;position:sticky;top:0;height:100vh;overflow:auto}.brand{font-size:13px;font-weight:800;letter-spacing:2px;color:#164f40}.brand small{display:block;letter-spacing:0;font-weight:400;color:#56665f;margin:8px 0 25px}nav a{display:block;text-decoration:none;font-size:12px;line-height:1.45;padding:9px 0;color:#46594f}nav span{display:inline-block;color:#14634e;width:24px;font-weight:700}main{min-width:0;max-width:1100px;padding:0 58px 65px}.hero{padding:65px 0 45px;border-bottom:1px solid #cbd5c9}.eyebrow{font-size:11px;font-weight:800;letter-spacing:2px;color:#176451;margin:0 0 12px}h1{font-size:clamp(40px,5.4vw,72px);line-height:1.04;letter-spacing:-3px;margin:22px 0}h1 em{font-style:normal;color:#176451}.intro{max-width:660px;font-size:19px;color:#4f6258}.chips{display:flex;flex-wrap:wrap;gap:8px;margin:25px 0}.chips span{border:1px solid #b6c9bd;padding:5px 12px;font-size:12px;border-radius:30px}.actions{display:flex;flex-wrap:wrap;gap:12px}.actions a,.actions button{padding:11px 18px;border-radius:7px;border:1px solid #176451;text-decoration:none;font-size:13px;font-weight:700;background:#176451;color:white}.actions button{background:transparent;color:#176451}section{padding:42px 0;border-bottom:1px solid #d8ded5;scroll-margin-top:20px}h2{font-size:29px;line-height:1.25;letter-spacing:-.6px;margin:0 0 22px}h3{font-size:19px;margin-top:28px}p{margin:14px 0}li{margin-bottom:7px}.note{background:#e8eee2;border-left:4px solid #47714e;padding:17px 22px;margin:24px 0;border-radius:0 8px 8px 0}code{font:13px/1.7 Consolas,monospace;overflow-wrap:anywhere;background:#e7ebe3;border-radius:3px;padding:2px 4px}.code-head{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:22px;background:#243d35;color:#d3e2d9;padding:11px 16px;font:12px/1.5 Consolas,monospace;border-radius:8px 8px 0 0}.code-head span{margin-right:auto}.code-head a{color:#d1eddc}.copiar{background:transparent;border:1px solid #718e7e;color:#e7f3e8;border-radius:4px;padding:3px 9px;font-size:11px}pre{background:#172c25;color:#e3eee5;overflow:auto;padding:22px;margin:0 0 24px;border-radius:0 0 8px 8px;font-size:12px;tab-size:2}pre code{background:none;color:inherit;padding:0;border-radius:0;white-space:pre;overflow-wrap:normal;font:12px/1.7 Consolas,monospace}table{border-collapse:collapse;width:100%;font-size:14px;margin:22px 0}th{text-align:left;background:#e6ebe1}td,th{border-bottom:1px solid #cdd7ca;padding:12px;vertical-align:top}.table-wrap{overflow:auto}.flow{padding:24px;border:1px solid #b9cabc;border-radius:12px;background:#edf1e8;text-align:center}.flow div{padding:13px;background:#fff;border:1px solid #c9d6c7;border-radius:7px}.flow b,.flow span{display:block}.flow span{font-size:12px;color:#596e61}.flow i{display:block;font-size:12px;padding:8px;font-style:normal}.checklist label{display:flex;gap:12px;align-items:baseline;border-bottom:1px solid #dce3d6;padding:10px 0}.checklist input{accent-color:#176451;flex-shrink:0}details{padding:14px 0}summary{cursor:pointer;color:#176451;font-weight:700}.skip{position:absolute;left:10px;top:-80px;background:white;padding:10px;z-index:10}.skip:focus{top:10px}footer{padding-top:30px;font-size:12px;color:#5c6f61}.progress{height:3px;background:#176451;position:fixed;top:0;left:0;width:0;z-index:20}.copy-status{font-size:12px;min-height:20px;color:#176451}@media(max-width:1000px){.layout{grid-template-columns:220px minmax(0,1fr)}main{padding:0 28px 40px}aside{padding:28px 18px}}@media(max-width:720px){.layout{display:block}aside{position:static;height:auto;border-right:0;border-bottom:1px solid #d8ded5}nav{display:grid;grid-template-columns:1fr 1fr;gap:0 15px}nav a{font-size:11px}main{padding:0 20px 35px}.hero{padding-top:35px}h1{letter-spacing:-2px}section{padding:30px 0}h2{font-size:25px}pre{padding:16px}}@media print{body{background:white;font-size:10pt;color:#111}.layout{display:block}aside,.actions,.copiar,.progress,.skip,.copy-status{display:none}main{max-width:none;padding:0}.hero{padding:0 0 20px}h1{font-size:34pt}h2{font-size:20pt}section{padding:20px 0;break-inside:auto}h2,h3,.code-head{break-after:avoid}pre{white-space:pre-wrap;background:#f1f3ef;color:#111;border:1px solid #ccd4ca;font-size:8pt}pre code{white-space:pre-wrap;overflow-wrap:anywhere;font-size:8pt}.code-head{background:#e6ebe1;color:#111}.code-head a{color:#111}.note{break-inside:avoid}a{color:#111}.flow{break-inside:avoid}thead{display:table-header-group}tr{break-inside:avoid}}
'''
js = '''
document.querySelector('#imprimir').addEventListener('click',()=>window.print());
document.querySelectorAll('.copiar').forEach(botao=>botao.addEventListener('click',async()=>{
 const texto=botao.parentElement.nextElementSibling.textContent;
 try{await navigator.clipboard.writeText(texto);botao.textContent='Copiado!';document.querySelector('#copy-status').textContent='Código copiado.';}
 catch{botao.textContent='Selecione o código';document.querySelector('#copy-status').textContent='Cópia automática indisponível. Selecione o bloco e use Ctrl+C.';}
 setTimeout(()=>botao.textContent='Copiar',2500);
}));
function progresso(){const altura=document.documentElement.scrollHeight-innerHeight;document.querySelector('.progress').style.width=(altura>0?scrollY/altura*100:0)+'%';}
addEventListener('scroll',progresso,{passive:true});addEventListener('resize',progresso);progresso();
'''
pagina = f'''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Manual passo a passo: cadastro de alunos com React, Vite, Flask e SQLite. Código completo, exercícios e testes."><title>Aula prática 5 — React, API e SQLite</title><style>{css}</style></head><body><a class="skip" href="#conteudo">Ir ao conteúdo</a><div class="progress" aria-hidden="true"></div><div class="layout"><aside><div class="brand">AULA PRÁTICA 05<small>Frontend · Backend · Banco de dados</small></div><nav aria-label="Sumário">{''.join(menu)}</nav></aside><main id="conteudo"><header class="hero"><p class="eyebrow">DESENVOLVIMENTO WEB / MANUAL DE LABORATÓRIO</p><h1>Da tela ao banco.<br><em>Agora com React.</em></h1><p class="intro">O mesmo cadastro. Uma nova forma de construir a interface. Aprenda componentes, estado e integração com uma API que salva dados de verdade.</p><div class="chips"><span>Iniciante em React</span><span>React + Vite</span><span>Python + Flask</span><span>SQLite</span><span>180 minutos</span></div><div class="actions"><a href="#s1">Começar a aula →</a><a href="cadastro-alunos-react.zip" download>Baixar projeto completo</a><button id="imprimir" type="button">Imprimir / salvar PDF</button></div><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p></header>{''.join(partes)}<footer>Aula prática 5 · Continuidade do cadastro de alunos · 30/10/2026<br>Material de leitura estático. A aplicação de exemplo é executada localmente.</footer></main></div><script>{js}</script></body></html>'''
(BASE / 'index.html').write_text(pagina, encoding='utf-8')
with zipfile.ZipFile(BASE / 'cadastro-alunos-react.zip', 'w', zipfile.ZIP_DEFLATED) as pacote:
    for caminho in (BASE / 'exemplo').rglob('*'):
        relativo = caminho.relative_to(BASE / 'exemplo')
        if caminho.is_file() and not any(x in relativo.parts for x in ['.venv', 'node_modules', 'dist', '__pycache__']) and not caminho.name.endswith(('.db', '.db-wal', '.db-shm', '.db-journal')):
            pacote.write(caminho, Path('cadastro-alunos-react') / relativo)
print('Manual e ZIP gerados a partir dos arquivos reais do exemplo.')

# Loja CMS em PHP puro — Plano de Implementação

> **Para agentes executores:** HABILIDADE OBRIGATÓRIA: use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar este plano tarefa por tarefa. Os passos usam caixas de seleção (`- [ ]`) para acompanhamento.

**Objetivo:** Construir uma loja didática em que o CMS e a área do usuário trocam informações por arquivos CSV.

**Arquitetura:** Funções puras em `includes/funcoes.php` centralizam leitura, validação e gravação. Páginas PHP recebem formulários por `POST`, chamam essas funções e redirecionam com mensagens; os dois ambientes usam os mesmos CSVs.

**Tecnologias:** PHP 8.3 puro, HTML5, CSS3, JavaScript e CSV.

**Especificação:** `docs/superpowers/specs/2026-09-11-loja-cms-php-design.md`

## Restrições globais

- Não usar framework, banco de dados ou bibliotecas externas.
- Executar com `php -S localhost:8000`.
- Usar nomes em português e manter o exemplo fácil de explicar em aula.
- Alterações de dados aceitam somente `POST`; toda saída variável no HTML deve ser escapada.
- Escritas em CSV devem usar bloqueio e substituição segura.

---

### Tarefa 1: Armazenamento CSV e catálogo

**Arquivos:**
- Criar: `includes/funcoes.php`
- Criar: `dados/produtos.csv`
- Criar: `dados/pedidos.csv`
- Criar: `tests/teste.php`

**Interfaces:**
- Produz: `lerCsv(string, array): array`, `salvarCsv(string, array, array): void`, `listarProdutos(): array`, `buscarProduto(int): ?array`, `proximoId(array): int`.

- [ ] **Passo 1: escrever testes inicialmente falhos**

```php
<?php
require __DIR__ . '/../includes/funcoes.php';
function verificar(bool $condicao, string $mensagem): void {
    if (!$condicao) { throw new RuntimeException($mensagem); }
}
verificar(proximoId([]) === 1, 'Primeiro ID deve ser 1');
verificar(proximoId([['id' => '2'], ['id' => '7']]) === 8, 'ID deve avançar');
verificar(count(listarProdutos()) >= 2, 'Catálogo inicial deve existir');
```

- [ ] **Passo 2: executar e confirmar a falha**

Executar: `php tests/teste.php`
Esperado: falha porque `includes/funcoes.php` ainda não existe.

- [ ] **Passo 3: implementar armazenamento e dados iniciais**

Criar funções com `fgetcsv`, `fputcsv`, `flock`, arquivo temporário na pasta `dados` e `rename`. Iniciar `produtos.csv` com Camisa PHP, Caneca Dev e Caderno Código; iniciar `pedidos.csv` somente com o cabeçalho.

- [ ] **Passo 4: executar os testes**

Executar: `php tests/teste.php`
Esperado: saída final `Todos os testes passaram.` e código 0.

- [ ] **Passo 5: registrar a tarefa**

```bash
git add includes/funcoes.php dados tests/teste.php
git commit -m "feat: adiciona armazenamento CSV"
```

### Tarefa 2: Regras de produtos e pedidos

**Arquivos:**
- Modificar: `includes/funcoes.php`
- Modificar: `tests/teste.php`

**Interfaces:**
- Consome: funções de CSV da Tarefa 1.
- Produz: `validarProduto(array): array`, `salvarProduto(array): array`, `excluirProduto(int): bool`, `registrarPedido(array): array`, `listarPedidos(): array`, `escapar(string): string`, `formatarPreco(float): string`.

- [ ] **Passo 1: acrescentar testes das regras**

```php
verificar(validarProduto(['nome'=>'', 'descricao'=>'x', 'preco'=>'10', 'estoque'=>'1']) !== [], 'Nome é obrigatório');
verificar(validarProduto(['nome'=>'X', 'descricao'=>'x', 'preco'=>'0', 'estoque'=>'-1']) !== [], 'Preço e estoque inválidos');
verificar(escapar('<b>') === '&lt;b&gt;', 'HTML deve ser escapado');
verificar(formatarPreco(12.5) === 'R$ 12,50', 'Preço deve usar padrão brasileiro');
```

- [ ] **Passo 2: executar e confirmar a falha**

Executar: `php tests/teste.php`
Esperado: erro de função indefinida.

- [ ] **Passo 3: implementar regras completas**

`salvarProduto` cria ou atualiza por ID; `excluirProduto` remove apenas ID existente. `registrarPedido` valida cliente, produto e quantidade, reduz estoque e grava `id,cliente,produto_id,produto,quantidade,total,data`. Todas retornam `['sucesso' => bool, 'mensagem' => string]` quando representam uma ação.

- [ ] **Passo 4: testar regras e sintaxe**

Executar: `php tests/teste.php` e `php -l includes/funcoes.php`
Esperado: testes passam e `No syntax errors detected`.

- [ ] **Passo 5: registrar a tarefa**

```bash
git add includes/funcoes.php tests/teste.php
git commit -m "feat: implementa regras da loja"
```

### Tarefa 3: Área do usuário

**Arquivos:**
- Criar: `index.php`
- Criar: `comprar.php`
- Criar: `assets/css/style.css`
- Criar: `assets/js/script.js`

**Interfaces:**
- Consome: `listarProdutos`, `registrarPedido`, `escapar` e `formatarPreco`.
- Produz: vitrine responsiva e endpoint `POST /comprar.php`.

- [ ] **Passo 1: ampliar o teste de integração**

```php
verificar(is_file(__DIR__ . '/../index.php'), 'A vitrine deve existir');
verificar(is_file(__DIR__ . '/../comprar.php'), 'O endpoint de compra deve existir');
```

- [ ] **Passo 2: executar e confirmar a falha**

Executar: `php tests/teste.php`
Esperado: falha indicando que a vitrine não existe.

- [ ] **Passo 3: implementar a vitrine e a compra**

Exibir cartões de produtos com formulário por produto. `comprar.php` rejeita métodos diferentes de `POST`, chama `registrarPedido` e redireciona para `/?tipo=sucesso|erro&mensagem=...`. JavaScript confirma a compra e CSS diferencia visualmente a loja.

- [ ] **Passo 4: verificar arquivos**

Executar: `php tests/teste.php` e `php -l index.php` e `php -l comprar.php`.
Esperado: todos passam sem erros.

- [ ] **Passo 5: registrar a tarefa**

```bash
git add index.php comprar.php assets tests/teste.php
git commit -m "feat: cria area do usuario"
```

### Tarefa 4: CMS de produtos e pedidos

**Arquivos:**
- Criar: `admin/index.php`
- Criar: `admin/salvar-produto.php`
- Criar: `admin/editar-produto.php`
- Criar: `admin/excluir-produto.php`
- Criar: `admin/pedidos.php`
- Modificar: `tests/teste.php`

**Interfaces:**
- Consome: todas as funções públicas de `includes/funcoes.php`.
- Produz: páginas `/admin/`, `/admin/editar-produto.php?id=N` e `/admin/pedidos.php`; endpoints POST para salvar e excluir.

- [ ] **Passo 1: testar a presença do CMS**

```php
foreach (['index.php', 'salvar-produto.php', 'editar-produto.php', 'excluir-produto.php', 'pedidos.php'] as $pagina) {
    verificar(is_file(__DIR__ . '/../admin/' . $pagina), "Página {$pagina} deve existir");
}
```

- [ ] **Passo 2: executar e confirmar a falha**

Executar: `php tests/teste.php`
Esperado: falha indicando página administrativa ausente.

- [ ] **Passo 3: implementar o CMS**

Criar navegação, formulário de cadastro, tabela com editar/excluir, edição preenchida e tabela de pedidos. Endpoints aceitam somente `POST` e redirecionam ao painel com mensagens. Exclusão usa confirmação JavaScript.

- [ ] **Passo 4: verificar o CMS**

Executar: `php tests/teste.php` e `Get-ChildItem admin -Filter *.php | ForEach-Object { php -l $_.FullName }`.
Esperado: testes passam e todas as páginas têm sintaxe válida.

- [ ] **Passo 5: registrar a tarefa**

```bash
git add admin assets/js/script.js tests/teste.php
git commit -m "feat: cria painel CMS"
```

### Tarefa 5: Documentação e verificação final

**Arquivos:**
- Criar: `README.md`
- Modificar: `tests/teste.php`

**Interfaces:**
- Consome: aplicação completa.
- Produz: instruções de aula e verificação automatizada final.

- [ ] **Passo 1: testar requisitos documentais**

```php
$readme = file_get_contents(__DIR__ . '/../README.md');
verificar(str_contains($readme, 'php -S localhost:8000'), 'README deve ensinar a iniciar');
verificar(str_contains($readme, 'CMS'), 'README deve explicar o CMS');
verificar(str_contains($readme, 'CSV'), 'README deve explicar os dados');
```

- [ ] **Passo 2: executar e confirmar a falha**

Executar: `php tests/teste.php`
Esperado: falha porque `README.md` ainda não existe.

- [ ] **Passo 3: escrever o roteiro didático**

Documentar pré-requisitos, comando de inicialização, endereços da loja e CMS, fluxo dos CSVs, papéis das tecnologias, sequência de demonstração e aviso de que CSV é adequado apenas ao protótipo didático.

- [ ] **Passo 4: executar a verificação completa**

Executar: `php tests/teste.php`; depois `Get-ChildItem -Recurse -Filter *.php | ForEach-Object { php -l $_.FullName }`; iniciar `php -S localhost:8000`, solicitar `/` e `/admin/` e confirmar HTTP 200.
Esperado: testes passam, nenhuma falha de sintaxe e ambas as páginas respondem 200.

- [ ] **Passo 5: registrar a conclusão**

```bash
git add README.md tests/teste.php
git commit -m "docs: adiciona roteiro da aula"
```

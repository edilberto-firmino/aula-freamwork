# Loja didática com CMS e área do usuário

## Objetivo

Criar uma aplicação pequena para demonstrar em aula a diferença entre uma tela de usuário e um CMS. As duas interfaces compartilharão dados por arquivos CSV, permitindo que os alunos enxerguem claramente como uma parte do sistema alimenta a outra.

## Tecnologias e limites

- PHP puro, sem framework ou bibliotecas externas.
- HTML, CSS e JavaScript simples.
- Arquivos CSV no lugar de um banco de dados.
- Execução local pelo servidor embutido do PHP.
- Sem autenticação, pagamento real ou envio de mensagens.

## Estrutura prevista

```text
projeto/
├── index.php
├── comprar.php
├── admin/
│   ├── index.php
│   ├── salvar-produto.php
│   ├── editar-produto.php
│   ├── excluir-produto.php
│   └── pedidos.php
├── dados/
│   ├── produtos.csv
│   └── pedidos.csv
├── includes/
│   └── funcoes.php
├── assets/
│   ├── css/style.css
│   └── js/script.js
└── README.md
```

## Área do usuário

A página `index.php` exibirá os produtos disponíveis em cartões com nome, descrição, preço e estoque. O usuário poderá informar seu nome, a quantidade desejada e confirmar a compra.

Ao comprar, o sistema validará os dados, verificará o estoque, registrará o pedido em `pedidos.csv` e diminuirá a quantidade correspondente em `produtos.csv`. A página exibirá uma mensagem clara de sucesso ou de erro.

## CMS

O painel `admin/index.php` mostrará os produtos em uma tabela e oferecerá formulários para cadastrar e editar nome, descrição, preço e estoque. Também será possível excluir um produto após confirmação no navegador.

A página `admin/pedidos.php` mostrará todos os pedidos com cliente, produto, quantidade, valor total e data. Um menu permitirá alternar entre produtos, pedidos e loja.

## Dados e comunicação

`produtos.csv` terá as colunas `id,nome,descricao,preco,estoque`. O CMS escreverá nesse arquivo e a loja o lerá.

`pedidos.csv` terá as colunas `id,cliente,produto_id,produto,quantidade,total,data`. A área do usuário escreverá nesse arquivo e o CMS o lerá.

As operações de escrita usarão bloqueio de arquivo. Os arquivos serão atualizados por substituição segura dentro da pasta `dados`, reduzindo o risco de conteúdo parcialmente gravado.

## Validação e tratamento de erros

- Campos obrigatórios não poderão ficar vazios.
- Preço deverá ser maior que zero; estoque não poderá ser negativo.
- Quantidade da compra deverá ser inteira, positiva e não superar o estoque.
- Dados exibidos no HTML serão escapados.
- Requisições que alteram dados usarão `POST`.
- Identificadores inexistentes produzirão mensagens de erro, sem interromper a aplicação.

## Aparência e didática

As áreas terão identidade visual diferente: a loja será apresentada como vitrine e o CMS como painel administrativo. O layout será responsivo e usará somente um arquivo CSS.

Os arquivos terão nomes em português e comentários apenas nos pontos importantes. O `README.md` explicará os papéis de HTML, CSS, JavaScript, PHP e CSV, além do comando `php -S localhost:8000` e de um roteiro curto para demonstração.

## Verificação

Serão verificados manualmente e, quando possível, por testes PHP sem bibliotecas:

1. leitura inicial dos produtos;
2. cadastro, edição e exclusão no CMS;
3. exibição das mudanças na loja;
4. compra válida e redução do estoque;
5. bloqueio de compra acima do estoque;
6. exibição do pedido no CMS;
7. sintaxe PHP de todos os arquivos;
8. funcionamento em tamanhos de tela diferentes.

## Critérios de conclusão

O projeto estará concluído quando puder ser iniciado apenas com PHP, quando o fluxo completo entre CMS e usuário funcionar pelos CSVs e quando o README permitir que o professor execute e explique o exemplo sem configuração adicional.

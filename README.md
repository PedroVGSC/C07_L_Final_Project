# Projeto Brasileirão 2026 - Banco de Dados

Este projeto foi feito em MySQL com o objetivo de criar um banco de dados simples para representar o Campeonato Brasileiro de 2026.

No banco foram cadastradas informações sobre clubes, jogadores, treinadores, estádios, partidas, competição, temporada e classificação dos times.

Além das tabelas, o projeto também usa alguns recursos importantes do MySQL, como procedure, function, trigger, view, usuários, roles e permissões.

## O que o projeto faz

O banco de dados criado se chama `brasileirao2026`.

No começo do script, o banco é apagado caso já exista. Fiz isso para conseguir rodar o código várias vezes sem dar erro por já ter tabelas ou dados criados anteriormente.

```sql
DROP DATABASE IF EXISTS brasileirao2026;
CREATE DATABASE brasileirao2026;
USE brasileirao2026;
```

Depois disso, são criadas as tabelas principais do campeonato.

## Tabelas criadas

O projeto possui tabelas para organizar as informações do campeonato.

A tabela `Estadio` guarda os dados dos estádios, como nome, cidade, estado e capacidade.

A tabela `Treinador` guarda os dados dos técnicos dos clubes.

A tabela `Clube` guarda os times participantes e faz ligação com o estádio e o treinador de cada clube.

A tabela `Jogador` guarda os jogadores cadastrados, com nome, nacionalidade, idade, posição, número da camisa e o clube em que joga.

A tabela `Competicao` guarda os dados da competição, nesse caso o Campeonato Brasileiro Série A.

A tabela `Temporada` guarda o ano da competição, data de início, data de fim e a competição relacionada.

A tabela `Participacao` guarda o desempenho de cada clube na temporada, como vitórias, empates, derrotas, gols pró e gols contra.

A tabela `Partida` guarda os jogos cadastrados, com data, rodada, placar, clube mandante, clube visitante, estádio e temporada.

## Inserção de dados

Depois da criação das tabelas, foram inseridos dados de exemplo para testar o banco.

Foram cadastrados estádios, treinadores, clubes, jogadores, uma competição, uma temporada, a participação dos clubes e algumas partidas.

Esses dados servem para conseguir testar os relacionamentos entre as tabelas e fazer consultas no final do script.

## Procedure de cadastro de jogador

No projeto foi criada uma procedure chamada `sp_cadastrar_jogador`.

Essa procedure serve para cadastrar um jogador sem precisar escrever o comando `INSERT` completo toda vez.

Exemplo usado no projeto:

```sql
CALL sp_cadastrar_jogador(
    'Neymar',
    'Brasil',
    34,
    'Atacante',
    10,
    @id_santos
);
```

Antes de cadastrar o Neymar, o código busca o `id_clube` do Santos e guarda em uma variável chamada `@id_santos`.

Depois disso, a procedure é chamada para inserir o jogador Neymar no clube Santos.

## Function de saldo de gols

Também foi criada uma função chamada `fn_saldo_gols`.

Ela recebe dois valores: gols feitos e gols sofridos.

A função retorna o saldo de gols, fazendo a subtração:

```sql
gols_pro - gols_contra
```

Essa function foi usada em uma consulta de partida para mostrar o saldo de gols do mandante e do visitante.

## Trigger de validação de idade

Foi criada uma trigger chamada `trg_validar_idade_jogador`.

Essa trigger é executada antes de inserir um jogador na tabela `Jogador`.

A regra dela é simples: não deixar cadastrar jogador com menos de 15 anos.

Se a idade informada for menor que 15, o banco retorna uma mensagem de erro:

```sql
Jogador deve possuir pelo menos 15 anos
```

Essa parte foi feita para mostrar como uma regra de validação pode ficar dentro do próprio banco de dados.

## Teste da procedure e da trigger

No final do código, foram feitos testes para verificar se a procedure e a trigger estão funcionando.

Primeiro, o código cadastra o Neymar no Santos usando a procedure `sp_cadastrar_jogador`.

Depois, existe uma parte separada para testar a trigger de idade.

Para esse teste realmente gerar erro, o jogador precisa ser cadastrado com menos de 15 anos. Um exemplo seria:

```sql
CALL sp_cadastrar_jogador(
    'Robinho Junior',
    'Brasil',
    14,
    'Atacante',
    7,
    (
        SELECT id_clube
        FROM Clube
        WHERE nome = 'Santos'
        LIMIT 1
    )
);
```

Como a idade é menor que 15, a trigger impede o cadastro e mostra a mensagem de erro.

Esse teste serve para confirmar que a validação de idade está funcionando corretamente.

## View de classificação

Foi criada uma view chamada `classificacao_completa`.

Essa view mostra a tabela de classificação dos clubes de forma mais organizada.

Ela apresenta:

* nome do clube;
* pontos;
* vitórias;
* empates;
* derrotas;
* gols pró;
* gols contra;
* saldo de gols;
* aproveitamento.

A pontuação é calculada com 3 pontos por vitória e 1 ponto por empate.

Para consultar a classificação, basta executar:

```sql
SELECT * FROM classificacao_completa;
```

Com a view, não precisa escrever toda a consulta grande toda vez que quiser ver a classificação.

## Usuários, roles e permissões

O projeto também cria dois usuários:

* `analista`
* `operador`

Também foram criadas duas roles:

* `role_analista`
* `role_operador`

O usuário `analista` tem permissão para consultar todas as tabelas do banco e executar a função de saldo de gols.

O usuário `operador` tem permissões mais limitadas. Ele pode consultar as tabelas de estádio, clube e jogador, além de executar a procedure de cadastro de jogador.

Essa parte foi feita para mostrar como separar níveis de acesso dentro do banco.

## Consultas finais

No final do script foram colocadas algumas consultas para testar o funcionamento do banco.

As consultas verificam, por exemplo:

* se o Neymar foi cadastrado corretamente;
* o saldo de gols de uma partida usando a function;
* a lista de jogadores junto com seus clubes;
* a pontuação parcial dos clubes;
* as partidas cadastradas;
* a classificação completa usando a view.

## Como executar

Para executar o projeto, basta abrir o MySQL Workbench ou outro programa que rode MySQL.

Depois é só colar o script completo e executar.

O banco `brasileirao2026` será criado com as tabelas, dados, usuários, permissões, procedure, function, trigger, view e consultas de teste.

## Conclusão

Esse projeto foi feito para praticar banco de dados relacional usando MySQL.

Nele foram usados conceitos como criação de tabelas, chaves estrangeiras, inserção de dados, consultas com `JOIN`, procedure, function, trigger, view e controle de permissões.

Mesmo sendo um projeto simples, ele mostra como organizar as informações de um campeonato de futebol dentro de um banco de dados.

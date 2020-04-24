# Questao 4

**Usuario**
codUsuario      | nome
--------- | ------
1 | aluno 1
2  | aluno 2

**Duvida**
codDuvida | codUsuario | Texto
--------- | ---------- | --------
1 | 1 | oi?
2 | 2 | nao entendi
3 | 1 | como?

**Resposta**
codResposta | codDuvida| codUsuario | Resposta
---------- | ---------- | ---------- | ----------
1 | 1 | 1 | Resposta da pergunta 1 !
2 | 2 | 1 | Respota da pergunta 2 !!
3 | 3 | 1 | Respota da pergunta 3 !!!
4 | 1 | 2 | Respota da pergunta 1 pelo usuario 2


# Resolucao

1. Multiplicacao entre as seguintes tabelas :
  - Usuario
  - Duvida

**Multiplicacao1**
codUsuario      | nome | codResposta | codDuvida| codUsuario | Resposta
--------- | ------ | ---------- | ---------- | ---------- | ----------
1 | aluno 1 | 1 | 1 | 1 | Resposta da pergunta 1 !
1 | aluno 1 | 2 | 2 | 1 | Respota da pergunta 2 !!
1 | aluno 1 | 3 | 3 | 1 | Respota da pergunta 3 !!!
1 | aluno 1 | 4 | 1 | 2 | Respota da pergunta 1 pelo usuario 2
 | | | 
2  | aluno 2 | 1 | 1 | 1 | Resposta da pergunta 1 !
2  | aluno 2 | 2 | 2 | 1 | Respota da pergunta 2 !!
2  | aluno 2 | 3 | 3 | 1 | Respota da pergunta 3 !!!
2  | aluno 2 | 4 | 1 | 2 | Respota da pergunta 1 pelo usuario 2


Imagine essa tabela como a  relação de 1 aluno respondendo todas as duvidas.

2. Projetar os seguintes campos da tabela *Multiplicacao1*:
  - codUsuario
  - codDuvida

**ProejecaoTodasRespostas**
codUsuario      | codDuvida 
--------- | ------ 
1 | 1
1 | 2
1 | 3
1 | 1
2 | 1
2 | 2
2 | 3
2 | 1 

Pronto, agora temos uma projecao como a relacao de 1 aluno respondendo (**Ficticio**) todas as duvidas,
onde *codUsuario* representa o usuario que respondeu, e *codDuvida* representa o codigo da duvida que ele respondeu.

Agora a ideia é projeta o *codUsuario* e *codDuvida* da tabela Resposta, e em seguida subtrair com a tabela ProejecaoTodasRespostas.

3. Projeta os seguintes campos da tabela *Resposta*:
  - codUsuario
  - codDuvida
 
 **ProejecaoResposta**
 codUsuario      | codDuvida 
--------- | ------ 
1 | 1
1 | 2
1 | 3
2 | 1

Vamos interpretar a tabela ProejecaoResposta:

Ela retorna pra gente uma tabela com a relacao **REAL** onde cada aluno respondeu uma determinada dúvida. Portanto o aluno 1 respondeu
a duvida 1.

Quando subtrairmos na seguinte ordem: ProejecaoTodasRespostas - ProejecaoResposta, teremos uma tabela resultando com os alunos que não responderam.

Analisando com calma essa subtração, o que estamos fazendo é remover da tabela fictícia as ocorrencias que realmente existem.
Portanto, se tiramos as reais sobraram somente as que nao existem, ou seja, onde o aluno não respondeu de fato.


4. Subtrai as tabelas ProejecaoTodasRespostas e ProejecaoResposta nas seguinte ordem:
  1. ProejecaoTodasRespostas
  2. ProejecaoResposta

**SubtracaoRespostas**
 codUsuario      | codDuvida 
--------- | ------ 
2 | 2
2 | 3

Essa tabela mostra pra gente o cod do aluno e o codigo da questao que ele nao respondeu.

5. Projetar os seguintes campos da tabela *SubtracaoRespostas*:
  - codUsuario
 
**AlunosQueNaoRespondeu**
codUsuario |
--------- |
2 | 
2 |

Pronto, temos entao uma tabela com o código dos aluno que não responderam todas as questoes.

6. Projetar os seguintes campos da tabela *Usuario*:
  - codUsuario

**ProjecaoCodUsuario**
codUsuario |
--------- |
1 | 
2 |

7. Subtrai as tabelas ProjecaoCodUsuario e AlunosQueNaoRespondeu nas seguinte ordem:
  1. ProjecaoCodUsuario
  2. AlunosQueNaoRespondeu

**AlunosQueRespondeuTodas**
codUsuario |
--------- |
1 | 

Pronto, agora temos uma tabela com o codigo do aluno que respondeu todas as questoes. Para finalizar é só fazer um JOIN com
a tabela Usuario, e projetar o nome do aluno.

A condição no JOIN deve ser 
```SQL
AlunosQueRespondeuTodas.codUsuario = Usuario.codUsuario
```

8. Projetar os seguintes campos do JOIN ente *AlunosQueRespondeuTodas* e *Usuario*:
  - nome

**NomeDoAlunoQueRespondeuTodas**
Nome |
--------- |
aluno 1 | 


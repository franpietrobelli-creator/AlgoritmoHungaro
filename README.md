# Algoritmo Húngaro – Problema da Atribuição

Implementação em Python do **método húngaro** para resolver o **problema da atribuição**. O trabalho foi feito para o TDE2 da disciplina *Resolução de Problemas com Lógica Matemática* (PUCPR, Engenharia de Software, 2026/2).

## O problema

Dada uma matriz quadrada de custos, em que `custos[i][j]` é o custo do agente `i` executar a tarefa `j`, o objetivo é atribuir **exatamente uma tarefa a cada agente**, sem repetir tarefas, de forma que o **custo total seja o menor possível**.

O exemplo usado no código vem da aula: cinco desenvolvedores, cinco tarefas e o tempo estimado, em horas, de cada pessoa em cada tarefa.

|       | API | Interface | Banco | Testes | Implantação |
|-------|-----|-----------|-------|--------|-------------|
| Ana   | 9   | 11        | 14    | 11     | 7           |
| Bruno | 6   | 15        | 13    | 13     | 10          |
| Carla | 12  | 13        | 6     | 8      | 8           |
| Diego | 11  | 9         | 10    | 12     | 9           |
| Elisa | 7   | 12        | 14    | 10     | 14          |

## Como o algoritmo funciona

O método húngaro é um **método exato**: quando termina, a solução encontrada é garantidamente ótima, sem testar todas as `n!` atribuições possíveis.

1. **Reduzir:** subtrai o menor valor de cada linha e, depois, de cada coluna. Isso não muda qual atribuição é a melhor, porque todas as atribuições perdem o mesmo valor.
2. **Atribuir:** procura `n` zeros independentes, ou seja, um zero por linha e por coluna. Se encontrar, essa é a atribuição ótima.
3. **Cobrir:** se não encontrar, cobre todos os zeros com o menor número possível de linhas e colunas.
4. **Ajustar:** pega o menor valor não coberto (δ), subtrai δ dos elementos não cobertos e soma δ nos elementos cobertos duas vezes. Depois volta para a etapa 2.

O custo final é sempre calculado na **matriz original**.

## Estrutura do código

| Função | O que faz |
|--------|-----------|
| `reduzir_linhas` / `reduzir_colunas` | Subtraem o mínimo de cada linha e de cada coluna, usando NumPy. |
| `procura_zeros` | Monta uma matriz auxiliar com `1` onde há zero e `0` nas demais posições. |
| `tentar_atribuir_linha` | Tenta dar a uma linha uma coluna com zero. Se a coluna já estiver ocupada, tenta realocar a linha que está nela, de forma recursiva. |
| `encontrar_atribuicoes` | Chama a função anterior para cada linha e obtém o maior número possível de zeros independentes. |
| `cobrir_zeros` | Encontra a cobertura mínima: marca as linhas sem atribuição, depois as colunas com zeros nessas linhas, depois as linhas atribuídas nessas colunas, e repete até não haver novas marcações. |
| `hungaro` | Junta tudo: reduz a matriz, repete atribuir → cobrir → ajustar até achar a solução e devolve a atribuição e o custo total. |

## Como executar

Requer Python 3.9+ e NumPy:

```bash
pip install numpy
python ProblemaAtribuicaoTDE2.py
```

Para testar outro caso, basta alterar a lista `custos` no início do arquivo.

Saída para o exemplo acima:

```
Linha 0 com Coluna 4
Linha 1 com Coluna 0
Linha 2 com Coluna 2
Linha 3 com Coluna 1
Linha 4 com Coluna 3
Custo total: 38
```

Ou seja: Ana → Implantação (7 h), Bruno → API (6 h), Carla → Banco (6 h), Diego → Interface (9 h) e Elisa → Testes (10 h), com **38 horas** no total.

## Limitações

- Funciona apenas com **matrizes quadradas**. Para outros tamanhos, a função retorna `None`.
- **Minimiza** o custo. Para um problema de maximização, é preciso transformar os valores antes, por exemplo usando `maior valor − custo`.
- Os zeros são detectados com `valor == 0`. Com custos decimais, erros de arredondamento podem atrapalhar.

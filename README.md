# Métodos Numéricos para Ciências Mecânicas (Refactored)

Este repositório contém a coleção de programas e tarefas desenvolvidos para a disciplina de **Métodos Numéricos para Ciências Mecânicas (MNCM)** na Universidade de Brasília.

O repositório foi reorganizado e refatorado para garantir melhor estruturação, nomes de arquivos padronizados e geração automatizada de resultados visuais.

## Estrutura do Repositório

O projeto está dividido em módulos numerados conforme a ordem de desenvolvimento:

*   **[01_Tarefa_Intro](./01_Tarefa_Intro/)**: Scripts introdutórios em Julia.
*   **[02_Reator_Newton_Raphson](./02_Reator_Newton_Raphson/)**: Solução de sistemas não-lineares (CSTR) com mapas de calor.
*   **[03_Zeros_Funcoes](./03_Zeros_Funcoes/)**: Comparação dos métodos de Müller e Secante para raízes polinomiais.
*   **[04_Conducao_Calor_1D](./04_Conducao_Calor_1D/)**: Simulação transiente de condução de calor (Diferenças Finitas) com animações.
*   **[05_Otimizacao_Multidimensional](./05_Otimizacao_Multidimensional/)**: Comparação de métodos de otimização (Aclive, Gradientes Conjugados, Newton, Levenberg-Marquardt).
*   **[06_Reatores_Mistos](./06_Reatores_Mistos/)**: Solução de EDOs para resposta transiente de reatores.

## Resumo dos Resultados Gerados

Cada pasta acima contém um `README.md` específico e uma subpasta `images/` com seus respectivos resultados. Abaixo estão alguns exemplos dos gráficos gerados automaticamente pelos scripts refatorados:

| Condução de Calor (Animação) | Otimização Multidimensional |
| :---: | :---: |
| ![Calor](04_Conducao_Calor_1D/images/tarefa_2_aplicacao_animacao.gif) | ![Otimização](05_Otimizacao_Multidimensional/images/result_plot.png) |

| Convergência (Raízes) | Reator CSTR (Heatmap) |
| :---: | :---: |
| ![Raízes](03_Zeros_Funcoes/images/grafico_convergencia_primeira_raiz.png) | ![CSTR](02_Reator_Newton_Raphson/images/mapa_concentracao.png) |

## Como Utilizar

Todos os scripts Python foram refatorados para execução direta (sem inputs interativos bloqueantes) e salvam os resultados na pasta `images/` local de cada módulo.

Para rodar qualquer programa, navegue até a pasta e execute:
```bash
cd 0X_Nome_Da_Pasta
python nome_do_script.py
```

## Requisitos Gerais
- Python 3.x
- `numpy`
- `matplotlib`
- `sympy` (apenas para Otimização)
- `pillow` (opcional, para salvar GIFs)

---
*Organizado por Pedro Henrique da Silva Costa - Matrícula 231012639*

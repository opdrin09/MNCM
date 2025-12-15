# Métodos Numéricos para Ciências Mecânicas (MNCM)

Este repositório contém a coleção de scripts e notebooks desenvolvidos para a disciplina de **Métodos Numéricos**, organizados e documentados para estudo e reprodução.

Os projetos cobrem desde a física básica de fluidos até otimização complexa e resolução de equações diferenciais parciais, utilizando **Python** e **Julia**.

## 📚 Índice de Projetos

Cada pasta contém um `README.md` detalhado com a contextualização física, equações governantes e análise dos resultados.

| Pasta | Tópico | Linguagem | Descrição Resumida |
| :--- | :--- | :---: | :--- |
| **[01_Tarefa_Intro](./01_Tarefa_Intro)** | Dinâmica de Partículas | **Julia** | Solução de EDOs para movimento com arrasto de Stokes e quadrático. Link para **Google Colab**. |
| **[02_Reator_Newton_Raphson](./02_Reator_Newton_Raphson)** | Sistemas Não-Lineares | **Python** | Análise de equilíbrio de um reator CSTR (multiplicidade de estados) usando Newton-Raphson. |
| **[03_Zeros_Funcoes](./03_Zeros_Funcoes)** | Raízes de Polinômios | **Python** | Comparação dos métodos de Müller e Secante com deflação polinomial. |
| **[04_Conducao_Calor_1D](./04_Conducao_Calor_1D)** | EDPs e Difusão | **Python** | Solução numérica da Equação do Calor Transiente por Diferenças Finitas (Método Implícito/TDMA). |
| **[05_Otimizacao_Multidimensional](./05_Otimizacao_Multidimensional)** | Otimização | **Python** | Comparação de Gradient Descent, Conjugate Gradient e Newton em superfícies complexas. |
| **[06_Reatores_Mistos](./06_Reatores_Mistos)** | Sistemas de EDOs | **Python** | Simulação transiente dinâmica de reatores químicos usando Runge-Kutta (RK4). |

## 🛠️ Como Utilizar este Repositório

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/opdrin09/MNCM
    ```
2.  **Navegue até a pasta do projeto desejado:**
    ```bash
    cd MNCM_Refactored/04_Conducao_Calor_1D  # Exemplo
    ```
3.  **Instale as dependências (Python):**
    ```bash
    pip install numpy matplotlib sympy
    ```
4.  **Execute o script:**
    ```bash
    python conducao_calor_1d.py
    ```
    *Os resultados (gráficos e animações) serão salvos automaticamente na subpasta `images/` de cada projeto.*

## 👤 Autor
**Pedro Henrique da Silva Costa**
Universidade de Brasília (UnB)
Matrícula: 231012639

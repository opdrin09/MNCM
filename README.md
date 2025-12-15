# Métodos Numéricos para Ciências Mecânicas (MNCM)

Este repositório reúne o conjunto de programas desenvolvidos para a disciplina de **Métodos Numéricos**, abrangendo tópicos desde a dinâmica de fluidos e otimização até a resolução de Equações Diferenciais Parciais (EDPs).

## 📚 Índice de Projetos

Cada diretório contém uma documentação técnica detalhada (README), incluindo a contextualização física, o modelo matemático e a análise dos resultados obtidos.

| Pasta | Tópico | Linguagem | Descrição |
| :--- | :--- | :---: | :--- |
| **[01_Tarefa_Intro](./01_Tarefa_Intro)** | Dinâmica de Partículas | **Julia** | Simulação de partícula em queda livre com arrasto de Stokes e quadrático. **Disponível no Google Colab.** |
| **[02_Reator_Newton_Raphson](./02_Reator_Newton_Raphson)** | Sistemas Não-Lineares | **Python** | Análise de equilíbrio e multiplicidade de estados em reator CSTR via Newton-Raphson. |
| **[03_Zeros_Funcoes](./03_Zeros_Funcoes)** | Raízes de Polinômios | **Python** | Estudo comparativo dos métodos de Müller e Secante com técnica de deflação. |
| **[04_Conducao_Calor_1D](./04_Conducao_Calor_1D)** | EDPs e Difusão | **Python** | Solução numérica da Equação do Calor Transiente via Diferenças Finitas Implícitas (TDMA). |
| **[05_Otimizacao_Multidimensional](./05_Otimizacao_Multidimensional)** | Otimização | **Python** | Comparação de algoritmos: Gradiente, Gradientes Conjugados, Newton e Levenberg-Marquardt. |
| **[06_Reatores_Mistos](./06_Reatores_Mistos)** | Sistemas de EDOs | **Python** | Simulação da dinâmica transiente de reatores químicos utilizando métodos Runge-Kutta (RK4/RK45). |

## 🛠️ Instruções de Uso

1.  **Clonagem do Repositório:**
    ```bash
    git clone https://github.com/opdrin09/MNCM
    ```

2.  **Navegação:**
    Acesse o diretório do projeto de interesse:
    ```bash
    cd MNCM_Refactored/04_Conducao_Calor_1D
    ```

3.  **Instalação de Dependências (Python):**
    ```bash
    pip install numpy matplotlib sympy
    ```

4.  **Execução:**
    ```bash
    python conducao_calor_1d.py
    ```

    Os resultados gráficos e animações gerados são salvos automaticamente no subdiretório `images/` de cada projeto.

## 📝 Sobre este Repositório

**Autor:** Pedro Henrique da Silva Costa  
**Instituição:** Universidade de Brasília (UnB)  
**Matrícula:** 231012639

### Nota sobre Desenvolvimento e Organização

Este repositório foi estruturado e documentado com o auxílio de ferramentas de IA (Large Language Models) com os seguintes objetivos:
- Aprimorar a didática e clareza da documentação técnica.
- Padronizar a estrutura de arquivos e diretórios.
- Implementar funcionalidades de persistência de resultados (salvamento automático de imagens).

**Observação:** Os códigos fonte apresentam pequenas adaptações em relação às versões originais submetidas na disciplina (ex: remoção de interatividade de console bloqueante, organização de pastas), mantendo-se inalterada a lógica numérica fundamental.

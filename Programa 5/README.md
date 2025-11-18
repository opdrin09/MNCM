# Comparação de Métodos de Otimização Multidimensional

Este projeto implementa e compara quatro métodos clássicos de otimização numérica aplicados a funções multidimensionais. O script foi desenvolvido para a disciplina de **Métodos Numéricos de Ciências Mecânicas** da **Universidade de Brasília (UnB)**.

**Aluno:** Pedro Henrique da Silva Costa | **Matrícula:** 231012639  
**Professor:** Rafael Gabler

## 🎯 Objetivo
O algoritmo busca encontrar pontos críticos (Mínimos, Máximos ou Pontos de Sela) em superfícies matemáticas. Ele possui um sistema de *failover*: se a busca por um mínimo divergir (indicando uma função côncava/máximo), ele inverte automaticamente a estratégia para buscar um máximo.

## 🖼 Demonstração Visual

Abaixo, o gráfico de contorno gerado pelo script, mostrando as trajetórias de convergência (ou divergência) de cada método em busca do ponto ótimo para a função configurada.

![Gráfico de Convergência dos Métodos de Otimização](./result_plot.png)

## 🛠 Métodos Implementados

1.  **Aclive/Declive Máximo (Steepest Descent/Ascent):** Um método de primeira ordem que segue a direção oposta (para mínimo) ou na mesma direção (para máximo) do gradiente. Utiliza busca de linha 1D (Newton-Raphson) para encontrar o tamanho de passo ótimo.
2.  **Gradientes Conjugados (Fletcher-Reeves):** Um método mais avançado de primeira ordem que otimiza a direção de busca, incorporando informações das direções anteriores para acelerar a convergência, especialmente em vales estreitos. Também emprega busca de linha 1D.
3.  **Método de Newton Multidimensional:** Um método de segunda ordem que utiliza informações do gradiente e da matriz Hessiana para encontrar um ponto crítico. Converge quadraticamente, mas pode falhar se a Hessiana for singular ou não definida positiva/negativa.
4.  **Levenberg-Marquardt:** Um algoritmo híbrido que combina a robustez do método do Gradiente com a velocidade do método de Newton. Ele adapta dinamicamente entre as duas abordagens através de um parâmetro de amortecimento (`alpha`) que modifica a Hessiana, garantindo passos de busca válidos mesmo em regiões complexas.

## ⚙ Estrutura do Código

O código-fonte (`otimizacao.py`) é modularizado em seções para facilitar a compreensão:

* **SEÇÃO 0: Importações e Justificativa:** Lista as bibliotecas externas necessárias e um breve disclaimer sobre a autoria e uso de IA.
* **SEÇÃO 1: Configuração do Professor:** Variáveis globais para definir o `MODO_TESTE` (função a ser otimizada) e, opcionalmente, a `FUNCAO_PROFESSOR_STRING` para testes personalizados.
* **SEÇÃO 2: Funções de Base (Helper):** Contém a implementação do `newton_raphson` 1D, crucial para a busca de linha em métodos como Aclive e Gradientes Conjugados.
* **SEÇÃO 3: Configuração do Problema:** A função `configurar_funcao_teste` interpreta o `MODO_TESTE` selecionado para gerar a expressão simbólica da função a ser otimizada e suas representações numéricas.
* **SEÇÃO 4: Métodos de Otimização:** Implementa cada um dos quatro algoritmos descritos acima, com o parâmetro `mode` permitindo alternar entre busca de mínimo (`'descent'`) e máximo (`'ascent'`).
* **SEÇÃO 5: Função de Plotagem:** Responsável por gerar o gráfico de contorno visualizando o caminho percorrido por cada método no espaço da função. Salva a imagem automaticamente como `result_plot.png`.
* **SEÇÃO 6: Execução Principal (Main com Failover):** Orquestra a execução, inicialmente tentando encontrar um mínimo. Se os métodos de gradiente divergirem, um mecanismo de *failover* é ativado para tentar encontrar um máximo, adaptando-se à natureza da função.

## 🚀 Como Rodar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado. As dependências podem ser instaladas via pip:

1.  Instale as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```
    *(O arquivo `requirements.txt` com as dependências está disponível na pasta do projeto.)*

2.  Execute o script principal:
    ```bash
    Programa_5_231012639.py
    ```

### Configuração do Teste
Você pode ajustar o comportamento do script editando as variáveis na `SEÇÃO 1: CONFIGURAÇÃO DO PROFESSOR` dentro do arquivo `otimizacao.py`:
  * `MODO_TESTE`: Escolha entre diferentes funções predefinidas (vale estreito, sela) ou uma função manual.
  * `FUNCAO_PROFESSOR_STRING`: Define a expressão da função para `MODO_TESTE = 4`.

## 🤖 Disclaimer de Autoria e Ferramentas

A lógica central da busca de linha 1D (`newton_raphson`) e a diferenciação simbólica usando `sympy` seguiram a abordagem solicitada. A estruturação de comentários, geração de funções auxiliares, sistema de plotagem e a lógica de "failover" foram desenvolvidos com o auxílio de ferramentas de Inteligência Artificial (Gemini), que contribuíram significativamente para a organização e robustez do código. Nenhuma biblioteca de otimização de alto nível (ex: `scipy.optimize`) foi utilizada para resolver o problema, garantindo a implementação "do zero" dos métodos.

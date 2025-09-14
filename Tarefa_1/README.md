# Tarefa 1: Movimento de Partícula com Arrasto

Este documento apresenta a análise e a solução numérica para o movimento de uma partícula sujeito a diferentes regimes de arrasto. O problema é resolvido utilizando o método de Runge-Kutta de 4ª Ordem implementado em Julia.

---

## O Método Numérico: Runge-Kutta de 4ª Ordem (RK4)

Para resolver as equações diferenciais ordinárias (EDOs) do problema, utilizaremos o método de Runge-Kutta de 4ª Ordem. A implementação genérica do solver, que recebe uma EDO qualquer na forma `f(t,v)`, pode ser encontrada no script da tarefa.

## Parte 1: Baixo Reynolds (Arrasto de Stokes) - Questões 1 e 2

Primeiro, resolvemos o problema para o caso de baixo número de Reynolds (`Re ≈ 0`), onde o arrasto é puramente viscoso. Conforme a **Questão 1**, a equação adimensionalizada governante é:

$$ St \frac{dv^{*}}{dt^{*}} = -v^{*} + 1 $$

A solução analítica para essa equação é $v^{*}(t^{*}) = 1 - e^{-t^{*}/St}$. O código resolve numericamente esta EDO para diferentes passos de tempo (`Δt`) e compara os resultados, mostrando como a precisão da solução melhora com o refinamento do passo, respondendo à **Questão 2**.

## Parte 2: Efeito Inercial (Arrasto Quadrático) - Questões 3 e 4

Como pedido na **Questão 3**, introduzimos um termo de correção inercial (arrasto quadrático) na equação governante. Após a adimensionalização, a equação se torna:

$$ St \frac{dv_{z}^{*}}{dt^{*}} = -v_{z}^{*} - \frac{3}{8} Re \, v_{z}^{*2} + 1 $$

O código resolve esta EDO para diferentes valores de `Re`, mostrando como a solução se desvia do caso `Re = 0`, respondendo à **Questão 4**.

## Parte 3: Comparação Adicional - Questão 5

A **Questão 5** pede a comparação da solução numérica com a solução exata para o caso com efeito inercial, obtida no artigo lido em aula. O código também implementa esta comparação.

---

### 📈 Resultados (Visualização Rápida)

As imagens a seguir são os resultados finais gerados pelo código. **Não é necessário executar o script para visualizá-los.**

**Figura 1: Comparação de Passos de Tempo (Arrasto de Stokes)**
![Gráfico de Stokes](./grafico_stokes_comparacao_dt.png)

**Figura 2: Efeito do Arrasto Quadrático (Variação de Reynolds)**
![Gráfico Quadrático](./grafico_quadratico_comparacao_re.png)

---

### ▶️ Como Executar o Código

Existem duas opções para executar a análise e regenerar os gráficos.

#### Opção A: Ambiente Local (Sem usar Git)

1.  Acesse a página principal do repositório no GitHub.
2.  Clique no botão verde **`< > Code`** e selecione **`Download ZIP`**.
3.  Extraia o arquivo `.zip` em sua máquina.
4.  Abra o terminal Julia, navegue até a pasta extraída `NOME-DO-SEU-REPOSITORIO-main/tarefa_1`.
5.  Ative o ambiente do projeto e instale as dependências:
    ```julia
    # Dentro do REPL do Julia
    using Pkg
    Pkg.activate(".")
    Pkg.instantiate()
    ```
6.  Execute o script:
    ```julia
    # Ainda no REPL
    include("tarefa_1.jl")
    ```

#### Opção B: Google Colab (Fácil, sem instalação)

Clique no botão abaixo para abrir um notebook no Google Colab. Este notebook irá configurar o ambiente Julia e executar o script `tarefa_1.jl` diretamente do repositório. Basta executar as células em ordem.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SEU_USUARIO/SEU_REPOSITORIO/blob/main/tarefa_1/executar_tarefa_1.ipynb)

# Repositório de Métodos Numéricos para Ciências Mecânicas
## Aluno: Pedro Henrique da Silva Costa | Matrícula: 231012639

Este repositório contém as soluções para as tarefas da disciplina de Métodos Numéricos para Ciências Mecânicas, ministrada pelo Professor Rafael Gabler.

---

### 📚 Índice de Tarefas

* **[Tarefa 1: Movimento de Partícula com Arrasto](#tarefa-1-movimento-de-partícula-com-arrasto)**
* `[Link para a Tarefa 2 quando ela existir]`
* `[Link para a Tarefa 3 quando ela existir]`

---

## Tarefa 1: Movimento de Partícula com Arrasto

Esta tarefa aborda a solução numérica de equações diferenciais que governam o movimento de uma partícula sob a influência de forças de arrasto em diferentes regimes de Reynolds.

### 📈 Resultados (Visualização Rápida)

As imagens a seguir são os resultados finais gerados pelo código. **Não é necessário executar o script para visualizá-los.**

**Figura 1: Comparação de Passos de Tempo (Arrasto de Stokes)**
![Gráfico de Stokes](caminho/para/grafico_stokes_comparacao_dt.png)

**Figura 2: Efeito do Arrasto Quadrático (Variação de Reynolds)**
![Gráfico Quadrático](caminho/para/grafico_quadratico_comparacao_re.png)

---

### 💻 O Código: `tarefa_1.jl`

Todo o código para esta tarefa está consolidado no arquivo [`tarefa_1.jl`](./tarefa_1.jl). A estrutura do arquivo é a seguinte:

* **Função do Solver RK4:** A implementação do Runge-Kutta de 4ª Ordem se encontra nas **[linhas X-Y](link-para-as-linhas-do-rk4)**.
* **Análise de Stokes (Questões 1 e 2):** A definição da EDO e a geração do primeiro gráfico estão localizadas nas **[linhas A-B](link-para-as-linhas-de-stokes)**.
* **Análise com Arrasto Quadrático (Questões 3 e 4):** A lógica para o segundo caso está definida nas **[linhas C-D](link-para-as-linhas-do-quadratico)**.

---

### ▶️ Como Executar o Código

Existem duas opções para executar a análise e regenerar os gráficos.

#### Opção A: Ambiente Local (Recomendado para melhor performance)



#### Opção B: Google Colab (Mais fácil, sem instalação)



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SEU_USUARIO/SEU_REPOSITORIO/blob/main/tarefa_1/executar_tarefa_1.ipynb)

Para isso funcionar, você precisa criar um arquivo chamado `executar_tarefa_1.ipynb` e colocar o seguinte conteúdo nele:

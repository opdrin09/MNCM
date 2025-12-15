# Programa 3: Zeros de Funções (Müller e Secante)

## 1. Pré-requisitos e Execução
Este programa requer **Python 3** com as bibliotecas `numpy` e `matplotlib` instaladas.

```bash
# Como executar
python muller_secante.py
```
O script exibirá a busca pelas raízes e salvará os gráficos de convergência na pasta `images/`.

## 2. Contextualização Matemática

Encontrar raízes de um polinômio $P(x) = 0$ é uma tarefa clássica. O problema teste abordado é encontrar as raízes do polinômio:
$$ P(x) = (x-1)(x-3)(x-5)(x-7)(x-9) $$
Cuje raízes conhecidas são obviamente 1, 3, 5, 7, 9. O desafio é calibrar métodos numéricos para encontrar essas raízes sem conhecimento prévio exato.

### A Técnica de Deflação
Após encontrar uma raiz $r_1$, para impedir que o método convirja novamente para a mesma raiz, utiliza-se a deflação. Modifica-se a função alvo dividindo-a pelo fator da raiz encontrada:
$$ P_{nova}(x) = \frac{P_{atual}(x)}{x - r_1} $$
Isso elimina a raiz $r_1$ da "paisagem" de busca, permitindo encontrar $r_2$, e assim por diante.

## 3. Metodologia Numérica

### Método de Müller
Uma generalização do método da Secante. Em vez de traçar uma reta por 2 pontos, o método de Müller traça uma **parábola por 3 pontos** $(x_0, x_1, x_2)$. A próxima aproximação $x_3$ é dada pela interseção dessa parábola com o eixo x.

*   **Vantagem**: Como envolve a fórmula quadrática (Bhaskara), o discriminante ($\sqrt{b^2-4ac}$) pode ser negativo. Isso permite que o método de Müller parta de chutes reais e encontre **raízes complexas**, algo impossível para o método de Newton ou Secante padrão.
*   **Convergência**: Superlinear, com ordem $\approx 1.84$.

### Método da Secante
Aproxima a derivada $f'(x)$ pela diferença finita entre dois pontos iterados:
$$ x_{k+1} = x_k - f(x_k) \frac{x_k - x_{k-1}}{f(x_k) - f(x_{k-1})} $$
*   **Vantagem**: Não necessita cálculo explícito da derivada analítica.
*   **Converência**: Superlinear, ordem $\phi \approx 1.618$ (Razão Áurea).

## 4. Análise dos Resultados

### Parte 1: Convergência para a Primeira Raiz
O gráfico abaixo compara a velocidade de convergência (Erro vs iterações) partindo de diferentes chutes iniciais. Note que o Método de Müller geralmente converge em menos iterações devido à sua ordem mais alta.
![Convergência Primeira Raiz](images/grafico_convergencia_primeira_raiz.png)

### Parte 2: Convergência Geral (Todas as Raízes)
Este gráfico mostra o processo completo usando a deflação.
![Convergência Geral](images/grafico_convergencia_geral.png)
*Observação importante: À medida que mais raízes são deflacionadas, erros numéricos de arredondamento se acumulam, podendo tornar a determinação das últimas raízes menos precisa.*

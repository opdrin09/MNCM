# Programa 3: Encontrando Raízes de Polinômios (Müller e Secante)

## Como Rodar
Precisa de Python 3 com `numpy` e `matplotlib`:

```bash
python muller_secante.py
```

Os gráficos de convergência serão salvos em `images/`.

## O Problema

Queremos encontrar todas as raízes (zeros) do polinômio:
$$ P(x) = (x-1)(x-3)(x-5)(x-7)(x-9) $$

Obviamente, as raízes são 1, 3, 5, 7 e 9. Mas o desafio aqui é: **como um método numérico consegue encontrar essas raízes sem saber delas de antemão?**

### A Técnica de Deflação

Depois de encontrar a primeira raiz (digamos, $r_1 = 1$), como fazemos pra encontrar as outras sem que o método fique "preso" sempre convergindo pra mesma raiz?

A solução é a **deflação**: dividimos o polinômio pelo fator $(x - r_1)$, criando um novo polinômio que não tem mais aquela raiz:
$$ P_{novo}(x) = \frac{P(x)}{x - r_1} $$

Aí aplicamos o método de novo no polinômio deflacionado pra achar $r_2$, e assim por diante.

**Problema da deflação:** Erros de arredondamento vão se acumulando. As últimas raízes costumam ser menos precisas que as primeiras.

## Os Métodos Numéricos

### Método de Müller
Usa **três pontos** pra traçar uma parábola e encontra onde ela cruza o eixo x. É uma generalização do método da Secante.

**Vantagem especial:** Como usa a fórmula de Bhaskara (que envolve $\sqrt{b^2-4ac}$), o método consegue encontrar **raízes complexas** mesmo partindo de chutes reais! Isso acontece quando o discriminante fica negativo.

**Convergência:** Ordem ~1.84 (superlinear).

### Método da Secante
Usa **dois pontos** pra traçar uma reta e encontra onde ela cruza o eixo x. É mais simples que o Müller.

**Vantagem:** Não precisa calcular derivadas analiticamente (ao contrário do Newton-Raphson).

**Convergência:** Ordem ~1.618 (a razão áurea φ!).

## Análise dos Resultados

### Gráfico 1: Convergência para a Primeira Raiz
![Convergência Primeira Raiz](images/grafico_convergencia_primeira_raiz.png)

**O que esse gráfico mostra:**
- Eixo X: Número de iterações.
- Eixo Y: Erro relativo (escala logarítmica).
- Cada linha representa uma tentativa partindo de um chute inicial diferente (0.5, 2.0, 4.1, 6.5, 8.4).

**Observações:**
- As linhas com círculos (○) são do Müller, as com x (×) são da Secante.
- Ambos os métodos convergem, mas o Müller geralmente precisa de **menos iterações** pra atingir a mesma precisão.
- Dependendo do chute inicial, os métodos podem convergir pra raízes diferentes. Por exemplo:
  - Chute 0.5 → Converge pra raiz 1.0
  - Chute 2.0 → Pode convergir pra 1.0 ou 3.0 (depende do método)
  - Chute 4.1 → Converge pra 3.0 ou 5.0

**Conclusão:** O Müller é mais eficiente (convergência mais rápida), mas ambos funcionam bem.

### Gráfico 2: Busca por Todas as Raízes (com Deflação)
![Convergência Geral](images/grafico_convergencia_geral.png)

**O que esse gráfico mostra:**
- Cada curva representa a busca por uma raiz diferente (1ª, 2ª, 3ª, 4ª, 5ª).
- As cores alternam entre Müller (linhas sólidas) e Secante (linhas tracejadas).

**Observações importantes:**
- A **primeira raiz** (azul) converge muito rápido e com alta precisão (erro cai pra $10^{-10}$ ou menos).
- A **segunda e terceira raízes** ainda convergem bem, mas já dá pra ver que o erro final não fica tão baixo quanto na primeira.
- A **quarta e quinta raízes** mostram um comportamento mais irregular. O erro pode até "oscilar" um pouco antes de convergir.

**Por que isso acontece?**
Cada vez que fazemos a deflação, introduzimos pequenos erros de arredondamento. Esses erros vão se acumulando. Quando chegamos na 5ª raiz, já fizemos 4 deflações, então o polinômio que estamos trabalhando não é mais exatamente o original - ele tem pequenas "contaminações" numéricas.

**Lição prática:** Se você precisa de alta precisão em todas as raízes, é melhor usar métodos mais sofisticados (como o método de Laguerre ou algoritmos que trabalham com polinômios companheiros). Mas para a maioria das aplicações de engenharia, essa precisão já é suficiente.

# Programa 3: Métodos de Müller e Secante

Este programa implementa os métodos numéricos de **Müller** e da **Secante** para encontrar as raízes de um polinômio. Ele demonstra a convergência para a primeira raiz e utiliza a técnica de deflação para encontrar todas as raízes do polinômio teste $f(x) = (x-1)(x-3)(x-5)(x-7)(x-9)$.

## Descrição

O script compara a eficiência e a robustez dos dois métodos.
- **Método de Müller**: Utiliza uma aproximação parabólica (3 pontos), convergindo mais rápido e capaz de encontrar raízes complexas.
- **Método da Secante**: Utiliza uma aproximação linear (2 pontos).

## Como Executar

```bash
python muller_secante.py
```

O script executará uma demonstração automática encontrando as raízes e gerando gráficos de convergência na pasta `images/`.

## Resultados

### Convergência para a Primeira Raiz
Comparativo do erro relativo vs. número de iterações para diferentes chutes iniciais.

![Convergência Primeira Raiz](images/grafico_convergencia_primeira_raiz.png)

### Convergência Geral (Todas as Raízes)
Mostra a busca sequencial por todas as raízes utilizando deflação polinomial. Observe como o erro pode variar para as raízes subsequentes devido ao acúmulo de erros de arredondamento na deflação.

![Convergência Geral](images/grafico_convergencia_geral.png)

## Dependências
- `numpy`
- `matplotlib`

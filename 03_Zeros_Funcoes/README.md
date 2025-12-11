# Programa 3: Métodos de Müller e Secante

## Contextualização do Problema
A determinação de raízes de polinômios e funções transcendentais é um problema fundamental em engenharia e ciências aplicadas. Este programa foca na resolução de raízes de polinômios de grau elevado utilizando dois métodos numéricos robustos:

1.  **Método de Müller:** Um método iterativo que utiliza três pontos iniciais para ajustar uma parábola (interpolação quadrática) a cada passo. Diferente do método da Secante, o método de Müller é capaz de encontrar raízes complexas pares a partir de chutes iniciais reais, devido à resolução da fórmula quadrática no domínio complexo.
2.  **Método da Secante:** Um método iterativo linear que aproxima a derivada da função por uma reta secante entre dois pontos. É mais simples que o método de Newton-Raphson pois não requer derivada analítica, mas pode convergir mais lentamente ou divergir se a função não for bem comportada.

O programa aplica esses métodos para encontrar todas as raízes de um polinômio teste, utilizando a técnica de **deflação polinomial** para encontrar raízes subsequentes após a primeira ser determinada. O objetivo é comparar a eficiência e a robustez de convergência de ambos os métodos.

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

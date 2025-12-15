# Tarefa 1: Introdução e Dinâmica de Partículas (Julia)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opdrin09/MNCM/blob/main/01_Tarefa_Intro/executar_tarefa_1.ipynb)

Esta pasta contém o estudo introdutório da disciplina, focado na simulação numérica da dinâmica de partículas em fluidos, utilizando a linguagem **Julia**.

## 1. Contextualização do Problema

O objetivo desta tarefa é simular o movimento de uma pequena partícula esférica caindo em um fluido viscoso sob a ação da gravidade. A dinâmica é governada pela Segunda Lei de Newton, onde as forças atuantes são o peso, o empuxo e a força de arrasto fluido.

A equação de movimento na forma adimensional é dada por:

$$ \frac{dv}{dt} = \frac{1 - v - \frac{3}{8} Re \cdot v^2}{St} $$

Onde:
- $v$: Velocidade adimensional da partícula.
- $t$: Tempo adimensional.
- $St$: **Número de Stokes**, que caracteriza a resposta inercial da partícula.
- $Re$: **Número de Reynolds e a particula**, que indica a importância das forças inerciais sobre as viscosas.

### Regimes de Escoamento Estudados
1.  **Regime de Stokes ($Re \approx 0$)**: O termo quadrático é desprezível. O arrasto é linear ($F_d \propto v$). A equação simplifica para uma EDO linear com solução analítica conhecida ($v(t) = 1 - e^{-t/St}$).
2.  **Regime Não-Linear ($Re > 0$)**: O arrasto quadrático torna-se relevante. A EDO torna-se não-linear e requer solução numérica.

## 2. Metodologia Numérica

Para resolver a equação diferencial ordinária (EDO), foi utilizado o método de **Runge-Kutta de 4ª Ordem (RK4)**. Este método é escolhido por sua alta precisão ($O(\Delta t^4)$), sendo superior ao método de Euler básico para passos de tempo equivalentes.

A implementação compara:
- A solução numérica vs. Solução analítica (para $Re=0$).
- A influência do passo de tempo ($\Delta t$) na convergência e estabilidade.
- O efeito do aumento do número de Reynolds na velocidade terminal da partícula.

## 3. Como Executar

Você tem duas opções para verificar os resultados e a resolução detalhada:

### Opção A: Google Colab (Recomendado)
Não requer instalação local. Basta clicar no badge abaixo para abrir o notebook interativo diretamente no navegador:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opdrin09/MNCM/blob/main/01_Tarefa_Intro/executar_tarefa_1.ipynb)

### Opção B: Execução Local (Julia)
Requer o ambiente Julia instalado.

```bash
# Executar o script puro
julia tarefa_1.jl

# Ou abrir o notebook (requer IJulia)
jupyter notebook executar_tarefa_1.ipynb
```

## 4. Resultados Esperados

Ao executar o código, você observará:
1.  **Convergência**: À medida que $\Delta t$ diminui, a solução numérica RK4 se sobrepõe perfeitamente à curva analítica.
2.  **Efeito do Reynolds**: Para $Re > 0$, a força de arrasto aumenta (incluindo o termo quadrático), fazendo com que a velocidade terminal da partícula seja **menor** do que no regime de Stokes puro.

---
*Este exercício serve como introdução tanto à física dos fluidos computacional quanto à sintaxe eficiente da linguagem Julia para cálculo numérico.*

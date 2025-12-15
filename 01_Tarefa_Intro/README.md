# Tarefa 1: Introdução e Dinâmica de Partículas (Julia)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opdrin09/MNCM/blob/main/01_Tarefa_Intro/executar_tarefa_1.ipynb)

Nesta primeira tarefa, a gente simula o movimento de uma partícula esférica caindo em um fluido viscoso. O objetivo é entender como diferentes forças de arrasto afetam a velocidade da partícula ao longo do tempo.

## O Problema Físico

Quando uma partícula cai em um fluido, ela sofre três forças principais: o peso (puxando pra baixo), o empuxo (empurrando pra cima) e o arrasto do fluido (resistindo ao movimento). A equação que descreve isso, na forma adimensional, é:

$$ \frac{dv}{dt} = \frac{1 - v - \frac{3}{8} Re \cdot v^2}{St} $$

Onde:
- **$v$**: velocidade da partícula (adimensional)
- **$St$** (Número de Stokes): mede a inércia da partícula
- **$Re$** (Número de Reynolds): indica se o escoamento é laminar ou turbulento

### Dois Regimes Diferentes

1. **Arrasto de Stokes ($Re \approx 0$)**: Quando a partícula é muito pequena ou o fluido muito viscoso, o arrasto é proporcional à velocidade ($F_d \propto v$). Nesse caso, a equação tem solução analítica exata: $v(t) = 1 - e^{-t/St}$.

2. **Arrasto Quadrático ($Re > 0$)**: Quando a partícula fica maior ou mais rápida, aparece um termo de arrasto proporcional a $v^2$. Isso torna a equação não-linear e só dá pra resolver numericamente.

## Como Rodar

### Opção 1: Google Colab (Mais Fácil)
Clique no badge abaixo e rode direto no navegador, sem instalar nada:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opdrin09/MNCM/blob/main/01_Tarefa_Intro/executar_tarefa_1.ipynb)

### Opção 2: Rodar Localmente
Se você tem Julia instalado:

```bash
julia tarefa_1.jl
```

## Resultados e Análise dos Gráficos

### Gráfico 1: Convergência do Método Numérico (Re = 0)
![Convergência Stokes](images/convergencia_stokes.png)

Neste gráfico, a linha tracejada preta é a solução analítica exata. As linhas coloridas são as soluções numéricas usando o método de Runge-Kutta de 4ª ordem (RK4) com diferentes passos de tempo ($\Delta t$).

**O que observar:**
- Quando $\Delta t$ é grande (ex: 2.0), a solução numérica fica "escadinha" e não acompanha bem a curva exata.
- Conforme $\Delta t$ diminui (1.33, 0.889, 0.593...), as curvas vão se aproximando cada vez mais da solução analítica.
- Para $\Delta t$ muito pequeno (< 0.2), as curvas praticamente se sobrepõem à solução exata, mostrando que o método RK4 é muito preciso quando bem configurado.

**Conclusão**: O método converge! Quanto menor o passo de tempo, mais precisa fica a solução.

### Gráfico 2: Efeito do Número de Reynolds
![Efeito Reynolds](images/efeito_reynolds.png)

Aqui a gente fixa $\Delta t = 0.01$ (bem pequeno) e varia o número de Reynolds de 0 até 5115. A linha tracejada preta continua sendo a solução analítica para $Re=0$ (arrasto linear).

**O que observar:**
- Para $Re = 0$ (azul), a curva numérica coincide perfeitamente com a analítica.
- Conforme $Re$ aumenta (5, 15, 35, 75...), a velocidade terminal (valor final que $v$ atinge) vai **diminuindo**.
- Para $Re = 5115$ (última curva), a partícula mal consegue acelerar, ficando com velocidade bem baixa.

**Por quê isso acontece?** Porque o termo de arrasto quadrático ($\propto v^2$) cresce muito rápido. Quanto maior o Reynolds, mais forte é esse arrasto extra, que "segura" a partícula e impede que ela atinja velocidades altas.

### Gráfico 3: Comparação com Solução Exata do Artigo
![Comparação Artigo](images/comparacao_artigo.png)

Este gráfico compara a nossa solução numérica (linha tracejada) com a solução analítica exata para o caso não-linear, obtida de um artigo científico (Equação 22 de Sobral et al.).

**O que observar:**
- As duas curvas estão praticamente sobrepostas, mostrando que a implementação do RK4 está correta.
- Mesmo para o caso não-linear (com o termo $v^2$), o método numérico consegue reproduzir a solução exata com alta precisão.

**Conclusão**: O código foi validado! Podemos confiar nos resultados numéricos para qualquer valor de Reynolds.

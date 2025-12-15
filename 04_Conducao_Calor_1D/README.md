# Programa 4: Condução de Calor 1D Transiente

## 1. Pré-requisitos e Execução
Requer **Python 3** com `numpy`, `matplotlib`.

```bash
# Como executar
python conducao_calor_1d.py
```
O script executará duas tarefas (Validação e Aplicação) e salvará perfis, heatmaps e animações (`.gif`) na pasta `images/`.

## 2. Contextualização Física

Este programa resolve a **Equação da Difusão de Calor** unidimensional em regime transiente. O problema físico considera uma parede plana (ou barra) sofrendo trocas térmicas com o ambiente e podendo ter geração interna de calor.

A Equação Diferencial Parcial (EDP) governante é:
$$ \rho c_p \frac{\partial T}{\partial t} = \frac{\partial}{\partial x}\left( k \frac{\partial T}{\partial x} \right) + \dot{q} $$

Dividindo por $\rho c_p$ e assumindo propriedades constantes, temos a forma clássica:
$$ \frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2} + S $$
Onde $\alpha = \frac{k}{\rho c_p}$ é a difusividade térmica e $S$ é o termo fonte.

## 3. Metodologia Numérica: Diferenças Finitas Implícitas

O domínio espacial é discretizado em nós $i$ e o tempo em passos $n$.
O script utiliza um **Esquema Totalmente Implícito** (Backward Time, Centered Space - BTCS). Diferente do método explícito, o método implícito é incondicionalmente estável (não limitado pelo número de Courant/Fourier), permitindo passos de tempo ($\Delta t$) maiores.

### Discretização
$$ \frac{T_i^{n+1} - T_i^n}{\Delta t} = \alpha \frac{T_{i+1}^{n+1} - 2T_i^{n+1} + T_{i-1}^{n+1}}{\Delta x^2} + S $$

Isso gera, para cada passo de tempo, um sistema linear tridiagonal da forma $\mathbf{A}\mathbf{T}^{n+1} = \mathbf{b}(\mathbf{T}^n)$.
Para resolver este sistema eficientemente (custo $O(N)$), utiliza-se o **Algoritmo de Thomas (TDMA)**.

## 4. Análise dos Resultados

### Tarefa A: Validação (Geração $\dot{q} = 0$)
Simula-se o resfriamento de uma placa. A solução numérica é comparada com a **Solução Analítica Exata** (Série de Fourier infinita).
Nota-se a perfeita sobreposição dos pontos (numérico) com a curva tracejada (analítica), validando o código.
![Validação Perfil](images/tarefa_1_validacao_perfil.png)

### Tarefa B: Aplicação (Geração $\dot{q} > 0$)
Simula-se o aquecimento devido a uma geração interna de calor (ex: reação química exotérmica ou aquecimento ôhmico).
O **Heatmap** abaixo mostra a evolução temporal (eixo X) da temperatura ao longo da espessura (eixo Y). Observe como o centro aquece mais rapidamente que a superfície.
![Heatmap Aplicação](images/tarefa_2_aplicacao_heatmap.png)

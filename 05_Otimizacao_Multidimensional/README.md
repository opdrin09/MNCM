# Programa 5: Otimização Multidimensional

## Instruções de Execução
Requer Python 3 com as bibliotecas `numpy`, `sympy` (cálculo simbólico) e `matplotlib`.

```bash
python otimizacao_multidimensional.py
```

## Contextualização do Problema

O problema de otimização irrestrita consiste em determinar o vetor de variáveis de projeto $\mathbf{x}^* = [x^*, y^*]^T$ que minimize (ou maximize) uma função objetivo escalar $f(x, y)$.

$$
\min_{x,y} f(x, y)
$$

O script explora superfícies de custo contendo "vales estreitos" (funções tipo Rosenbrock) e pontos de sela, cenários desafiadores para algoritmos de otimização convencionais.

## Metodologia Numérica

Implementaram-se quatro algoritmos clássicos para análise comparativa:

1.  **Aclive Máximo (Steepest Descent/Ascent):**
    *   Direção: $\mathbf{d}_k = -\nabla f(\mathbf{x}_k)$.
    *   **Características:** Método de primeira ordem. Estável longe do ótimo, porém apresenta convergência lenta ("zigue-zague") em vales estreitos.

2.  **Gradientes Conjugados (Fletcher-Reeves):**
    *   Direção: Combinação linear do gradiente atual e da direção anterior.
    *   **Características:** Utiliza direções "conjugadas" em relação à Hessiana, permitindo avançar de forma mais eficiente através de vales alongados.

3.  **Método de Newton Multidimensional:**
    *   Direção: $\mathbf{d}_k = -[\mathbf{H} f(\mathbf{x}_k)]^{-1} \nabla f(\mathbf{x}_k)$.
    *   **Características:** Método de segunda ordem (utiliza curvatura). Apresenta convergência quadrática (acelerada) nas proximidades do ótimo, mas é sensível à condição inicial e à definição positiva da Hessiana.

4.  **Levenberg-Marquardt:**
    *   Direção: Interpolação adaptativa: $\mathbf{d}_k = -[\mathbf{H} + \lambda \mathbf{I}]^{-1} \nabla f$.
    *   **Características:** Combina a estabilidade do Gradiente (longe do ótimo, $\lambda$ grande) com a velocidade de Newton (perto do ótimo, $\lambda$ pequeno).

## Análise dos Resultados

### Mapa de Contorno e Caminhos de Otimização
![Comparação de Otimização](images/result_plot.png)

**Descrição:**
- As curvas de nível representam a topografia da função objetivo.
- O marcador vermelho indica o ponto inicial comum a todos os métodos.
- As linhas traçam a trajetória iterativa de cada algoritmo.

**Análise Detalhada:**
1.  **Aclive Máximo (Azul, Círculos):** Exibe o característico padrão em zigue-zague (passos ortogonais), resultando em convergência lenta.
2.  **Gradientes Conjugados (Rosa, X):** Apresenta uma trajetória mais direta, corrigindo a ineficiência do gradiente puro.
3.  **Newton (Vermelho, Triângulos):** Quando converge, segue uma trajetória quase direta ao ótimo em poucas iterações.
4.  **Levenberg-Marquardt (Roxo, Quadrados):** Demonstra comportamento consistente e eficiente, atuando como um intermediário entre Newton e Gradiente.

### Tabela de Desempenho (Console)

O script exibe métricas quantitativas (número de passos, tempo de execução e erro final) para avaliação de eficiência.

**Nota sobre Estabilidade (Failover):** O algoritmo possui uma lógica de detecção de divergência. Caso a busca por um ponto de **mínimo** falhe (métodos divergindo para infinito, indicando concavidade), o sistema reinicia automaticamente o processo buscando por um **máximo**.

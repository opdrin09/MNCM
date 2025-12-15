# Programa 2: Reator CSTR com Newton-Raphson

## Como Rodar
Precisa de Python 3 com `numpy` e `matplotlib`:

```bash
python reator_newton_raphson.py
```

Os mapas de calor serão salvos automaticamente em `images/`.

## O Problema

Imagine um reator químico onde acontece uma reação exotérmica (que libera calor) do tipo $A \to B$. O reator é do tipo CSTR (Continuous Stirred-Tank Reactor), ou seja, tem entrada e saída contínuas de material e é bem misturado.

A gente quer saber: **em que condições de concentração e temperatura o reator vai operar no estado estacionário** (quando tudo para de mudar com o tempo)?

### As Equações

No equilíbrio, dois balanços precisam ser satisfeitos simultaneamente:

1. **Balanço de Massa** (quanto de reagente A sobra):
   $$ f_1(C_A, T) = \frac{C_{A,in} - C_A}{\tau} - k(T)C_A = 0 $$

2. **Balanço de Energia** (quanto de calor entra e sai):
   $$ f_2(C_A, T) = \frac{\rho c_p (T_e - T)}{\tau} + (-\Delta H)k(T)C_A - \frac{UA}{V}(T - T_c) = 0 $$

A taxa de reação $k(T)$ segue a **Lei de Arrhenius**, que faz ela crescer exponencialmente com a temperatura:
$$ k(T) = k_0 \exp\left(-\frac{E}{RT}\right) $$

Isso cria uma não-linearidade forte: quanto mais quente, mais rápida a reação, que libera mais calor, que aquece mais o reator... Pode virar um ciclo!

### O Fenômeno da Multiplicidade

Por causa dessa não-linearidade, o reator pode ter **mais de um estado de equilíbrio possível**:

1. **Estado "Apagado"**: Temperatura baixa, reação lenta, pouca conversão de A.
2. **Estado "Aceso"**: Temperatura alta, reação rápida, muita conversão de A.
3. **Estado Intermediário**: Matematicamente existe, mas é instável (qualquer perturbação faz o sistema ir pro estado 1 ou 2).

## O Método Numérico

Para achar esses pontos de equilíbrio, usamos o **Método de Newton-Raphson para sistemas**. A ideia é:

1. Chuta um valor inicial para $(C_A, T)$.
2. Calcula a matriz Jacobiana (derivadas parciais de $f_1$ e $f_2$).
3. Atualiza o chute usando: $\mathbf{x}_{novo} = \mathbf{x}_{velho} - \mathbf{J}^{-1} \mathbf{F}$.
4. Repete até convergir.

O interessante é que **dependendo do chute inicial, o método converge para estados diferentes**!

## Análise dos Resultados

O programa varre uma grade de condições iniciais $(C_{A0}, T_0)$ e vê pra onde cada uma converge.

### Mapa de Concentração Final
![Mapa de Concentração](images/mapa_concentracao.png)

**O que esse mapa mostra:**
- Cada pixel representa uma condição inicial diferente ($C_{A0}, T_0$).
- A cor indica a concentração final de equilíbrio encontrada.
- **Interpretação das Cores (escala Viridis):**
   - **Roxo/Azul (Valores baixos):** Indica baixa concentração final de A. Isso significa que a reação ocorreu e consumiu o reagente. $\to$ **Estado ACESO**.
   - **Amarelo/Verde (Valores altos):** Indica alta concentração final de A. O reagente sobrou quase todo. $\to$ **Estado APAGADO**.
- Vimos claramente as bacias de atração: dependendo de onde você começa, o reator "cai" para o estado aceso ou apagado.

### Mapa de Temperatura Final
![Mapa de Temperaturas](images/mapa_temperaturas.png)

**O que esse mapa mostra:**
- A cor indica a temperatura final de equilíbrio.
- **Interpretação das Cores (escala Plasma):**
   - **Amarelo (Valores altos):** Temperatura alta. $\to$ **Estado ACESO** (Exotérmico).
   - **Roxo (Valores baixos):** Temperatura baixa (próxima da entrada). $\to$ **Estado APAGADO**.

**Conclusão Visual:**
Os dois mapas são complementares (onde um é amarelo, o outro tende a ser roxo, e vice-versa). Eles mostram a alta não-linearidade do sistema: uma pequena mudança na temperatura inicial (eixo X) pode fazer o sistema cruzar a fronteira abruptamente de "apagado" para "aceso" (fenômeno de ignição).

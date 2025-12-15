# Programa 2: Reator CSTR com Newton-Raphson

## Instruções de Execução
Requer Python 3 com as bibliotecas `numpy` e `matplotlib`.

```bash
python reator_newton_raphson.py
```

Os mapas de calor gerados serão salvos automaticamente no diretório `images/`.

## Contextualização do Problema

Considere um reator químico do tipo CSTR (Continuous Stirred-Tank Reactor) onde ocorre uma reação exotérmica irreversível $A \to B$. O sistema opera com fluxo contínuo de entrada e saída.

O objetivo é determinar as **condições de operação em estado estacionário** (concentração e temperatura de equilíbrio) para o reator.

### Modelo Matemático

No equilíbrio, os balanços de massa e energia devem ser satisfeitos simultaneamente:

1.  **Balanço de Massa:**
    $$
    f_1(C_A, T) = \frac{C_{A,in} - C_A}{\tau} - k(T)C_A = 0
    $$

2.  **Balanço de Energia:**
    $$
    f_2(C_A, T) = \frac{\rho c_p (T_e - T)}{\tau} + (-\Delta H)k(T)C_A - \frac{UA}{V}(T - T_c) = 0
    $$

A constante cinética $k(T)$ segue a **Lei de Arrhenius**:
$$
k(T) = k_0 \exp\left(-\frac{E}{RT}\right)
$$

A dependência exponencial com a temperatura introduz uma forte não-linearidade no sistema.

### Multiplicidade de Estados Estacionários

Devido à não-linearidade, o sistema pode apresentar múltiplos pontos de equilíbrio para os mesmos parâmetros operacionais:

1.  **Estado "Apagado":** Baixa temperatura, baixa conversão.
2.  **Estado "Aceso":** Alta temperatura, alta conversão.
3.  **Estado Instável:** Ponto intermediário (sela), fisicamente difícil de manter sem controle ativo.

## Metodologia Numérica

Para solucionar o sistema não-linear acoplado, utiliza-se o **Método de Newton-Raphson Multidimensional**:

1.  Define-se uma estimativa inicial $(C_{A0}, T_0)$.
2.  Calcula-se a Matriz Jacobiana ($\mathbf{J}$) contendo as derivadas parciais.
3.  Atualiza-se a solução iterativamente:
    $$
    \mathbf{x}_{k+1} = \mathbf{x}_k - \mathbf{J}^{-1}(\mathbf{x}_k) \mathbf{F}(\mathbf{x}_k)
    $$
4.  O processo repete-se até a convergência.

Nota-se que a solução final depende fortemente da estimativa inicial fornecida.

## Análise dos Resultados

O algoritmo explora uma malha de condições iniciais $(C_{A0}, T_0)$ para mapear as bacias de atração de cada estado estacionário.

### Mapa de Concentração Final
![Mapa de Concentração](images/mapa_concentracao.png)

**Interpretação:**
- Cada ponto do mapa corresponde a uma condição inicial distinta.
- A escala de cores indica a concentração final de equilíbrio ($C_A$).
- **Legenda de Cores (Viridis):**
    - **Roxo/Azul (Valores baixos):** Baixa concentração final de reagente. Indica alta conversão. $\to$ **Estado ACESO**.
    - **Amarelo/Verde (Valores altos):** Alta concentração final. Pouca reação ocorreu. $\to$ **Estado APAGADO**.
- Observam-se fronteiras nítidas separando as regiões, delimitando as bacias de atração.

### Mapa de Temperatura Final
![Mapa de Temperaturas](images/mapa_temperaturas.png)

**Interpretação:**
- Representa a temperatura final de equilíbrio para cada condição inicial.
- **Legenda de Cores (Plasma):**
    - **Amarelo (Valores altos):** Alta temperatura final. $\to$ **Estado ACESO** (Reação exotérmica intensa).
    - **Roxo (Valores baixos):** Temperatura próxima à de entrada. $\to$ **Estado APAGADO**.

**Conclusão:**
Os mapas evidenciam a bistabilidade do sistema. Pequenas perturbações nas condições iniciais, quando próximas às fronteiras das bacias de atração, podem levar o reator a migrar abruptamente de um estado operacional para outro (ignition/extinction).

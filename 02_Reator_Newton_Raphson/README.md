# Programa 2: Reator CSTR com Newton-Raphson

## 1. Pré-requisitos e Execução
Este programa requer **Python 3** com as bibliotecas `numpy` e `matplotlib` instaladas.

```bash
# Como executar
python reator_newton_raphson.py
```
O script gerará automaticamente os mapas de convergência na pasta `images/`.

## 2. Contextualização Física e Matemática

O problema consiste na análise de operação estacionária de um **Reator de Tanque Agitado Continuamente (CSTR)** onde ocorre uma reação exotérmica de primeira ordem $A \to B$. 

### As Equações Governantes
O sistema é regido pelos balanços de massa e energia. No estado estacionário (derivadas temporais nulas), temos um sistema de equações não-lineares acopladas:

1.  **Balanço de Massa:**
    $$ f_1(C_A, T) = \frac{C_{A,in} - C_A}{\tau} - k(T)C_A = 0 $$

2.  **Balanço de Energia:**
    $$ f_2(C_A, T) = \frac{\rho c_p (T_e - T)}{\tau} + (-\Delta H)k(T)C_A - \frac{UA}{V}(T - T_c) = 0 $$

Onde a constante de velocidade segue a **Lei de Arrhenius**, introduzindo a forte não-linearidade exponencial:
$$ k(T) = k_0 \exp\left(-\frac{E}{RT}\right) $$

**Variáveis e Parâmetros:**
*   $C_A, T$: Concentração e Temperatura do reator (Incógnitas).
*   $\tau$: Tempo de residência.
*   $(-\Delta H)$: Calor de reação (Exotérmico).
*   $UA$: Coeficiente global de troca térmica.

### O Fenômeno da Multiplicidade
Devido à não-linearidade do termo de Arrhenius (geração de calor) versus a linearidade da remoção de calor, este sistema pode apresentar **multiplicidade de estados estacionários**:
1.  **Estado Baixo (Extinção)**: Baixa conversão, baixa temperatura (Reação lenta).
2.  **Estado Alto (Ignição)**: Alta conversão, alta temperatura (Reação rápida).
3.  **Estado Intermediário**: Instável matematicamente (ponto de sela).

## 3. Metodologia Numérica: Newton-Raphson Multidimensional

Para encontrar as raízes simultâneas $\mathbf{x} = [C_A, T]^T$ tal que $\mathbf{F}(\mathbf{x}) = 0$, utilizamos o método iterativo de Newton-Raphson:

$$ \mathbf{x}_{k+1} = \mathbf{x}_k - \mathbf{J}^{-1}(\mathbf{x}_k) \mathbf{F}(\mathbf{x}_k) $$

Onde $\mathbf{J}$ é a matriz Jacobiana das derivadas parciais:
$$ \mathbf{J} = \begin{bmatrix} \frac{\partial f_1}{\partial C_A} & \frac{\partial f_1}{\partial T} \\ \frac{\partial f_2}{\partial C_A} & \frac{\partial f_2}{\partial T} \end{bmatrix} $$

## 4. Análise dos Resultados

O programa varre uma matriz de condições iniciais $(C_{A0}, T_0)$ e determina para qual estado estacionário o método converge.

### Mapas de Atração (Heatmaps)
As imagens geradas mostram as "Bacias de Atração". Dependendo de onde o processo começa (condição inicial), ele pode convergir para o estado de "Ignição" ou "Extinção".

1.  **Mapa de Concentração Final**:
    ![Mapa de Concentração](images/mapa_concentracao.png)
    *Cores diferentes indicam convergência para concentrações finais distintas (ex: zero para reação completa/alta temperatura, ou alta para reação lenta).*

2.  **Mapa de Temperatura Final**:
    ![Mapa de Temperaturas](images/mapa_temperaturas.png)
    *Mostra claramente as regiões quentes (estado ignição) e frias (estado extinção).*

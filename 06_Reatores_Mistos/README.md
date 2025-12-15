# Programa 6: Dinâmica de Reatores (EDOs)

## Instruções de Execução
Requer Python 3 com as bibliotecas `numpy` e `matplotlib`:

```bash
python reatores_mistos.py
```

## Contextualização do Problema

Diferentemente da análise de estado estacionário (Programa 2), este estudo foca na **Dinâmica Transiente** do reator CSTR. Busca-se simular a evolução temporal das variáveis de estado (concentração e temperatura) partindo de uma condição inicial arbitrária até o atingimento do equilíbrio.

O sistema é governado por um sistema de EDOs acopladas:

1.  **Variação da Concentração ($dC_A/dt$):**

   $$\frac{dC_A}{dt} = \frac{1}{\tau}(C_{A,in} - C_A) - k(T)C_A$$

2.  **Variação da Temperatura ($dT/dt$):**

   $$\frac{dT}{dt} = \frac{1}{\rho c_p} \left[ \frac{\rho c_p}{\tau}(T_e - T) + (-\Delta H)k(T)C_A - \frac{UA}{V}(T - T_c) \right]$$
   

Estas equações descrevem a taxa instantânea de variação do sistema. A integração temporal permite reconstruir a trajetória completa ($C_A(t), T(t)$).

## Metodologia Numérica

### RK4 (Runge-Kutta de 4ª Ordem)
Método de referência para integração numérica de EDOs. Em cada passo de tempo $\Delta t$:
1.  Avaliam-se as derivadas em quatro pontos intermediários.
2.  Calcula-se uma média ponderada para estimar o próximo estado.

Possui erro global de ordem $O(\Delta t^4)$, conferindo alta precisão para a maioria das aplicações de engenharia.

### RK45 (Runge-Kutta-Fehlberg / Embedded)
Método adaptativo que calcula simultaneamente soluções de 4ª e 5ª ordem. A discrepância entre as soluções fornece uma estimativa do erro local, permitindo o ajuste automático do passo de tempo em implementações avançadas. Neste trabalho, utiliza-se o RK45 para validação comparativa.

## Análise dos Resultados

### Resposta Transiente do Reator (Comparação RK4 vs RK45)
![Gráfico de Reatores Mistos](images/reatores_mistos_plot.png)

**Descrição:**
O gráfico apresenta a evolução temporal de **5 concentrações distintas** (C1 a C5), ilustrando a dinâmica de múltiplas espécies ou condições.

-   **Linhas Variadas (RK4):** Solução via RK4 Clássico. Utilizaram-se estilos distintos (sólido, tracejado, etc.) para diferenciar as curvas, pois **C1, C2 e C5 convergem para o mesmo valor**, causando sobreposição.
-   **Marcadores Circulares (RKF45):** Solução via RKF45 (Embedded).

**Análise:**
1.  **Sobreposição Física:** Observa-se que $C_1$, $C_2$ e $C_5$ tendem ao mesmo estado estacionário (~11.5), o que explica a sobreposição visual das curvas.
2.  **Validação Numérica:** Observa-se uma sobreposição perfeita entre os marcadores (RKF45) e as linhas do RK4. Isso confirma a precisão da implementação.
2.  **Regime Transiente:** Partindo da condição inicial (ex: $t=0$), as concentrações elevam-se rapidamente, caracterizando o período de ajuste dinâmico do reator.
3.  **Estado Estacionário:** Após aproximadamente 3 segundos (tempo de estabilização), as curvas atingem patamares constantes. Esses valores finais correspondem aos pontos de equilíbrio estático que seriam encontrados resolvendo o sistema algébrico (como no Programa 2).

**Interpretação Física:**
O gráfico simula, por exemplo, o comportamento de partida (start-up) do reator. Inicialmente, a reação e o acúmulo de massa provocam variações rápidas. Eventualmente, o sistema alcança o equilíbrio onde as taxas de entrada, saída e reação se balanceiam.

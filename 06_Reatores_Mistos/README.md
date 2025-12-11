# Programa 6: Reatores Mistos (EDOs)

## Contextualização do Problema
Este programa simula o comportamento dinâmico (transiente) de um sistema de reatores químicos, modelado por um sistema de Equações Diferenciais Ordinárias (EDOs). O problema físico consiste em determinar como a concentração de reagentes ($C_A$) e a temperatura ($T$) evoluem no tempo dentro do reator até atingirem o estado estacionário.

Matematicamente, temos um Problema de Valor Inicial (PVI) da forma:
$$ \frac{d\mathbf{y}}{dt} = f(t, \mathbf{y}), \quad \mathbf{y}(0) = \mathbf{y}_0 $$
onde $\mathbf{y} = [C_A, T]^T$.

Para resolver este sistema, o programa implementa métodos numéricos de integração temporal da família Runge-Kutta:
1.  **Runge-Kutta de 4ª Ordem (RK4):** Um método clássico de passo fixo que oferece um excelente balanço entre precisão e custo computacional.
2.  **Runge-Kutta-Fehlberg (RK45/Embedded):** Um método adaptativo que estima o erro de truncamento local comparando soluções de 4ª e 5ª ordem, permitindo (teoricamente) ajustar o passo de tempo. Neste script, ele é usado principalmente para fins comparativos de precisão em relação ao RK4 clássico.

O resultado é a trajetória temporal das variáveis de estado, permitindo visualizar a resposta dinâmica e a estabilidade do processo.

## Descrição

O código simula a evolução da concentração ou temperatura ao longo do tempo e plota a comparação entre os métodos implementados para validar a precisão.

## Como Executar

```bash
python reatores_mistos.py
```

O gráfico resultante será salvo automaticamente na pasta `images/`.

## Resultados

### Comparação dos Métodos Numéricos
O gráfico abaixo apresenta a solução transiente obtida.

![Gráfico de Reatores Mistos](images/reatores_mistos_plot.png)

## Dependências
- `numpy`
- `matplotlib`

# Programa 6: Reatores Mistos (EDO)

Este programa resolve um problema de resposta transiente em reatores químicos modelado por Equações Diferenciais Ordinárias (EDOs). Ele compara a solução obtida por diferentes métodos de integração numérica, como Runge-Kutta de 4ª ordem (RK4) e métodos Runge-Kutta embutidos.

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

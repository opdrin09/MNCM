# Programa 2: Reator CSTR com Newton-Raphson

Este programa resolve o sistema de equações não-lineares que modela um reator CSTR (Continuous Stirred-Tank Reactor) utilizando o método de Newton-Raphson. O objetivo é encontrar os pontos de operação estacionária (concentração e temperatura) e analisar a multiplicidade de estados estacionários.

## Descrição

O código implementa o método de Newton-Raphson para resolver o sistema de balanço de massa e energia acoplado. Ele também gera mapas de calor (heatmaps) para visualizar como a convergência para diferentes estados estacionários depende das condições iniciais (Concetração inicial $Ca_0$ e Temperatura inicial $T_0$).

## Como Executar

Certifique-se de ter Python instalado com as bibliotecas `numpy` e `matplotlib`.

```bash
python reator_newton_raphson.py
```

O script rodará automaticamente, resolvendo para casos específicos e gerando os mapas de calor na pasta `images/`.

## Resultados

### Mapa de Concentração Final
Este mapa mostra a concentração final alcançada pelo reator para diferentes combinações de condições iniciais. Regiões de cores diferentes indicam convergência para estados estacionários distintos (multiplicidade).

![Mapa de Concentração](images/mapa_concentracao.png)

### Mapa de Temperatura Final
Analogo ao mapa de concentração, mostra a temperatura final de equilíbrio.

![Mapa de Temperaturas](images/mapa_temperaturas.png)

## Dependências
- `numpy`
- `matplotlib`

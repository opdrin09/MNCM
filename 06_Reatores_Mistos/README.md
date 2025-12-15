# Programa 6: Dinâmica de Reatores (EDOs)

## Como Rodar
Precisa de Python 3 com `numpy` e `matplotlib`:

```bash
python reatores_mistos.py
```

## O Problema

Ao contrário do Programa 2 (que buscava o equilíbrio), aqui a gente simula **como o reator evolui no tempo** partindo de uma condição inicial até chegar no estado estacionário.

O sistema é descrito por duas equações diferenciais ordinárias (EDOs) acopladas:

1. **Variação da Concentração:**
   $$ \frac{dC_A}{dt} = \frac{1}{\tau}(C_{A,in} - C_A) - k(T)C_A $$

2. **Variação da Temperatura:**
   $$ \frac{dT}{dt} = \frac{1}{\rho c_p} \left[ \frac{\rho c_p}{\tau}(T_e - T) + (-\Delta H)k(T)C_A - \frac{UA}{V}(T - T_c) \right] $$

Essas equações dizem: "a cada instante, como $C_A$ e $T$ estão mudando?". Integrando no tempo, descobrimos a trajetória completa.

## Os Métodos Numéricos

### RK4 (Runge-Kutta de 4ª Ordem)
O "padrão ouro" da integração numérica. A cada passo de tempo, ele:
1. Avalia a derivada em 4 pontos intermediários.
2. Faz uma média ponderada dessas derivadas.
3. Usa essa média pra atualizar a solução.

**Precisão:** Erro global de $O(\Delta t^4)$ - muito bom!

### RK45 (Runge-Kutta-Fehlberg / Embedded)
Uma versão mais sofisticada que calcula simultaneamente uma solução de 4ª e outra de 5ª ordem. A diferença entre elas dá uma estimativa do erro, permitindo (em implementações completas) ajustar o passo de tempo automaticamente.

Neste script, usamos o RK45 principalmente pra **validar** que o RK4 está funcionando bem (as duas soluções devem ser quase idênticas).

## Análise dos Resultados

### Resposta Transiente do Reator
![Gráfico de Reatores Mistos](images/reatores_mistos_plot.png)

**O que o gráfico mostra:**
- Eixo X: Tempo (0 a 100 segundos).
- Eixo Y: Concentração de reagente A (adimensional).
- Linha tracejada azul: Solução usando RK4.
- Linha sólida vermelha (semi-transparente): Solução usando RK45.

**Observações:**

1. **Regime Transiente (t = 0 a ~50s):**
   - A concentração cai rapidamente no início.
   - Isso acontece porque o reator está "se ajustando" à condição inicial.
   - A taxa de variação ($dC_A/dt$) é grande nessa fase.

2. **Aproximação do Equilíbrio (t = 50 a 100s):**
   - A curva vai ficando cada vez mais "horizontal".
   - A concentração está se aproximando de um valor final constante.
   - Esse valor final deve coincidir com uma das raízes encontradas no Programa 2!

3. **Comparação RK4 vs RK45:**
   - As duas linhas estão praticamente sobrepostas (você mal consegue ver a diferença).
   - Isso valida que:
     - O passo de tempo escolhido ($\Delta t = 0.5$s) é adequado.
     - A implementação do RK4 está correta.
   - Se as linhas estivessem muito separadas, seria sinal de que precisamos diminuir $\Delta t$.

**Interpretação física:**

Imagine que você liga um reator químico que estava desligado. Nos primeiros minutos, muita coisa está acontecendo:
- A temperatura está subindo (reação exotérmica).
- O reagente A está sendo consumido rapidamente.
- O sistema está "procurando" seu ponto de operação estável.

Depois de um tempo, as coisas se acalmam e o reator entra num ritmo constante - é o **estado estacionário**. A partir daí, se você não mexer em nada (vazão, temperatura de entrada, etc.), o reator vai ficar operando naquele ponto indefinidamente.

**Conexão com o Programa 2:**

- **Programa 2:** Encontrou os possíveis estados de equilíbrio (onde o reator pode operar).
- **Programa 6:** Mostra como o reator chega até um desses estados partindo de uma condição inicial.

Se você mudar a condição inicial (valores de $C_{A0}$ e $T_0$), o reator pode convergir pra um estado de equilíbrio diferente - isso é a multiplicidade de estados que vimos no Programa 2!

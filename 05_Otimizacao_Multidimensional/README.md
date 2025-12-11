# Programa 5: Otimização Multidimensional

Este programa implementa e compara quatro métodos clássicos de otimização multidimensional para encontrar mínimos (ou máximos) de funções de duas variáveis $f(x, y)$.

## Métodos Implementados
1.  **Aclive Máximo (Steepest Descent/Ascent)**: Segue a direção do gradiente.
2.  **Gradientes Conjugados (Fletcher-Reeves)**: Usa direções conjugadas para convergência mais rápida em vales estreitos.
3.  **Método de Newton Multidimensional**: Usa a Hessiana para encontrar pontos críticos diretamente (quadrático).
4.  **Levenberg-Marquardt**: Híbrido entre Gradiente e Newton, robusto para regiões distantes do ótimo.

## Funcionalidades
- **Detecção Automática de Máx/Mín**: O script tenta encontrar um mínimo; se divergir (indicando função côncava ou ponto de sela instável para descida), ele inverte a busca para encontrar um máximo.
- **Busca de Linha Otimizada**: Utiliza Newton-Raphson 1D para determinar o passo ótimo $h$ em cada iteração.

## Como Executar

```bash
python otimizacao_multidimensional.py
```

O script está configurado (via variável `MODO_TESTE`) para testar uma função específica. Ele gerará um relatório no terminal e salvará o gráfico do caminho de otimização em `images/`.

## Resultados

### Caminho de Otimização
O gráfico abaixo mostra as curvas de nível da função objetivo e o caminho percorrido por cada método partindo de um ponto inicial até o ótimo.

![Comparação de Otimização](images/result_plot.png)

## Dependências
- `numpy`
- `sympy` (para diferenciação simbólica do gradiente e hessiana)
- `matplotlib`

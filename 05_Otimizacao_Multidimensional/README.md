# Programa 5: Otimização Multidimensional

## Contextualização do Problema
Este programa aborda o problema de encontrar pontos ótimos (mínimos, máximos ou pontos de sela) em superfícies multidimensionais descritas por funções de duas variáveis $f(x, y)$. Problemas de otimização como este são cruciais em design de engenharia, economia e aprendizado de máquina, onde se deseja minimizar custos ou maximizar eficiência.

O script implementa e compara quatro métodos clássicos de otimização:
1.  **Método do Aclive Máximo (Steepest Descent/Ascent):** Segue a direção do gradiente negativo (para mínimo) ou positivo (para máximo). É robusto, mas pode ser lento em regiões de "vales" estreitos.
2.  **Método dos Gradientes Conjugados:** Melhora a eficiência do gradiente utilizando direções conjugadas, evitando o comportamento de "zigue-zague" em vales estreitos.
3.  **Método de Newton Multidimensional:** Utiliza informações de segunda ordem (Hessiana) para convergir quadraticamente (muito rápido) para o ponto crítico, mas é sensível a pontos iniciais distantes e custoso computacionalmente.
4.  **Método de Levenberg-Marquardt:** Uma abordagem híbrida que interpola entre o método do gradiente e o método de Gauss-Newton, oferecendo robustez longe do mínimo e velocidade perto dele.

O programa testa esses métodos em diferentes cenários ("Vales", "Selas", Funções arbitrárias) para demonstrar suas características de convergência.

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

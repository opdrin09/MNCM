# Programa 4: Condução de Calor 1D Transiente

Este programa resolve a equação da difusão de calor unidimensional em regime transiente utilizando o método de Diferenças Finitas (FDM) com esquema implícito e o algoritmo TDMA (Thomas) para inversão da matriz tridiagonal.

## Descrição

O código é dividido em duas partes:
1.  **Validação**: Simula o resfriamento de uma placa sem geração de calor e compara o resultado numérico com a solução analítica exata (série infinita).
2.  **Aplicação**: Simula o aquecimento de uma placa com geração interna de calor (ex: reação química ou aquecimento elétrico).

## Como Executar

```bash
python conducao_calor_1d.py
```

O script gerará perfis de temperatura estáticos, mapas de calor (tempo x posição) e animações `.gif` na pasta `images/`.

## Resultados

### 1. Validação (Solução Numérica vs. Analítica)
Comparação entre o método de diferenças finitas e a solução exata.
![Validação Perfil](images/tarefa_1_validacao_perfil.png)

Animação do resfriamento:
![Animação Validação](images/tarefa_1_validacao_animacao.gif)

### 2. Aplicação com Geração de Calor
Perfil final de temperatura:
![Aplicação Perfil](images/tarefa_2_aplicacao_perfil.png)

Evolução temporal da temperatura (Heatmap):
![Heatmap Aplicação](images/tarefa_2_aplicacao_heatmap.png)

Animação do aquecimento:
![Animação Aplicação](images/tarefa_2_aplicacao_animacao.gif)

## Dependências
- `numpy`
- `matplotlib` (com `pillow` para salvar GIFs)

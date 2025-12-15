# Métodos Numéricos para Ciências Mecânicas (MNCM)

Este repositório reúne os programas desenvolvidos ao longo da disciplina de **Métodos Numéricos**, cobrindo desde dinâmica de fluidos até otimização e resolução de EDPs.

## 📚 Índice de Projetos

Cada pasta tem um README detalhado explicando a física do problema, as equações e os resultados.

| Pasta | Tópico | Linguagem | Descrição |
| :--- | :--- | :---: | :--- |
| **[01_Tarefa_Intro](./01_Tarefa_Intro)** | Dinâmica de Partículas | **Julia** | Simulação de partícula caindo em fluido com arrasto de Stokes e quadrático. **Link para Google Colab disponível!** |
| **[02_Reator_Newton_Raphson](./02_Reator_Newton_Raphson)** | Sistemas Não-Lineares | **Python** | Análise de equilíbrio de reator CSTR (multiplicidade de estados) usando Newton-Raphson. |
| **[03_Zeros_Funcoes](./03_Zeros_Funcoes)** | Raízes de Polinômios | **Python** | Comparação dos métodos de Müller e Secante com deflação polinomial. |
| **[04_Conducao_Calor_1D](./04_Conducao_Calor_1D)** | EDPs e Difusão | **Python** | Solução numérica da Equação do Calor por Diferenças Finitas (Método Implícito/TDMA). |
| **[05_Otimizacao_Multidimensional](./05_Otimizacao_Multidimensional)** | Otimização | **Python** | Comparação de Gradient Descent, Conjugate Gradient, Newton e Levenberg-Marquardt. |
| **[06_Reatores_Mistos](./06_Reatores_Mistos)** | Sistemas de EDOs | **Python** | Simulação transiente de reatores químicos usando Runge-Kutta (RK4 e RK45). |

## 🛠️ Como Usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/opdrin09/MNCM
   ```

2. **Navegue até a pasta do projeto:**
   ```bash
   cd MNCM_Refactored/04_Conducao_Calor_1D  # Exemplo
   ```

3. **Instale as dependências (Python):**
   ```bash
   pip install numpy matplotlib sympy
   ```

4. **Execute:**
   ```bash
   python conducao_calor_1d.py
   ```

Os resultados (gráficos e animações) são salvos automaticamente na subpasta `images/` de cada projeto.

## 📝 Sobre este Repositório

**Autor:** Pedro Henrique da Silva Costa  
**Instituição:** Universidade de Brasília (UnB)  
**Matrícula:** 231012639

### Nota sobre Organização e Uso de IA

Este repositório foi organizado e documentado com auxílio de ferramentas de IA (Large Language Models) para:
- Estruturar a documentação de forma clara e didática.
- Padronizar os nomes de arquivos e pastas.
- Adicionar funcionalidades de salvamento automático de imagens nos scripts.

**Importante:** Os códigos aqui apresentados estão **levemente diferentes** das versões originalmente entregues ao professor da disciplina. As modificações foram feitas exclusivamente para melhorar a organização do repositório (criação de pastas `images/`, remoção de `input()` interativos, etc.). A lógica numérica e os resultados permanecem os mesmos.

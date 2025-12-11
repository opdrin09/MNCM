"""
===========================================================================
     Universidade de Brasília
     Disciplina: Métodos Numéricos de Ciências Mecânicas
     Professor: Rafael Gabler
     Aluno: Pedro Henrique da Silva Costa | Matrícula: 231012639

     COMPARAÇÃO DE MÉTODOS DE OTIMIZAÇÃO MULTIDIMENSIONAL

    Descrição:
    Este script implementa e compara quatro métodos de otimização.
    Ele primeiro tenta encontrar um PONTO DE MÍNIMO. Se os métodos
    de gradiente divergirem (indicando uma função côncava), ele
    automaticamente tentará encontrar um PONTO DE MÁXIMO.

    Métodos Implementados:
    1. Aclive Máximo (com modo Mín/Máx)
    2. Gradientes Conjugados (com modo Mín/Máx)
    3. Método de Newton (Agnóstico a Mín/Máx)
    4. Método de Levenberg-Marquardt (com modo Mín/Máx)

    Disclaimer de Autoria e Ferramentas:
    - A lógica de busca de linha 1D (newton_raphson) e o uso da
      biblioteca 'sympy' para diferenciação simbólica foram
      baseados na abordagem original solicitada.
    - As implementações de estruturação de comentários, a geração de
      funções, o sistema de plotagem e a lógica de "failover"
      (que aumentam bastante o tamanho do código)
      foram estruturados e corrigidos por IA (Gemini).
    - Nenhuma biblioteca de otimização (ex: scipy.optimize)
      foi utilizada para "resolver" o problema.
===========================================================================
"""

### --------------------------------------------------------------------------
### SEÇÃO 0: IMPORTAÇÕES E JUSTIFICATIVA DE USO
### --------------------------------------------------------------------------

import numpy as np # Para operações matemáticas eficientes com vetores e matrizes.
import sympy as sym # APENAS para calcular Gradiente e Hessiana simbolicamente.
import matplotlib.pyplot as plt # APENAS para a plotagem final do gráfico.
import time # APENAS para medir o tempo de execução (benchmark).
import random # APENAS para gerar funções e pontos iniciais aleatórios.


### --------------------------------------------------------------------------
### SEÇÃO 1: CONFIGURAÇÃO DO PROFESSOR (EDITAR AQUI)
### --------------------------------------------------------------------------

# MODO_TESTE:
# Escolha o modo de execução do script:
#   1 = Vale Estreito (Padrão, MÍNIMO) -> Script encontrará o MÍNIMO.
#   2 = Vale Estreito Aleatório (MÍNIMO) -> Script encontrará o MÍNIMO.
#   3 = Ponto de Sela (Aleatório) -> Métodos de descida podem falhar.
#   4 = Função Manual (Professor) -> Ex: a do PDF ("2*x*y+...") é um MÁXIMO.
#
MODO_TESTE = 4


# FUNCAO_PROFESSOR_STRING:
# Esta variável SÓ é usada se MODO_TESTE = 4.
# A função do PDF (2*x*y+2*x-x**2-2*y**2) é um MÁXIMO.
# O script tentará achar o MÍNIMO, falhará (divergirá), e então achará o MÁXIMO.
#
FUNCAO_PROFESSOR_STRING = "2*x*y+2*x-x**2-2*y**2"

### --------------------------------------------------------------------------
### SEÇÃO 2: FUNÇÕES DE BASE (HELPER)
### --------------------------------------------------------------------------

# Timer global para rastrear o tempo gasto especificamente na busca de linha 1D
global_timers = {
    'newton_time': 0.0
}

def newton_raphson(funcao_simbolica, variavel):
    """
    Resolve f(h) = 0 usando Newton-Raphson 1D.
    Usado para encontrar o passo ótimo 'h' na busca de linha.
    """
    start_time_nr = time.time()
    tol = 1e-5
    h_k = 1.0 
    
    try:
        dfdh = sym.diff(funcao_simbolica, variavel)
        f_num = sym.lambdify(variavel, funcao_simbolica, "numpy")
        dfdh_num = sym.lambdify(variavel, dfdh, "numpy")
    except Exception as e:
        global_timers['newton_time'] += (time.time() - start_time_nr)
        return 0.01, 1 

    cont = 0
    while abs(f_num(h_k)) > tol:
        df_val = dfdh_num(h_k)
        
        if abs(df_val) < 1e-8: 
            h_k = 1e-4 
            break
        
        h_k = h_k - f_num(h_k) / df_val
        cont += 1
        
        if cont > 100: 
            h_k = 0.01 
            break
    
    global_timers['newton_time'] += (time.time() - start_time_nr)
    return abs(h_k), cont

### --------------------------------------------------------------------------
### SEÇÃO 3: CONFIGURAÇÃO DO PROBLEMA (LÊ VARIÁVEIS GLOBAIS)
### --------------------------------------------------------------------------

def configurar_funcao_teste(modo, funcao_string):
    """
    Lê as variáveis globais da SEÇÃO 1 e prepara a expressão simbólica.
    """
    x, y = sym.symbols('x y')
    ponto_otimo_conhecido = "N/A"
    expressao = None

    print("\n" + "-"*50)
    print("Configuração da Função de Teste de Otimização")
    print("-"*50)

    if modo == 1:
        print("Modo selecionado: [1] Vale Estreito (Padrão - MÍNIMO)")
        expressao = (x - 2)**2 + 50 * (y - 1)**2 
        ponto_otimo_conhecido = "Mínimo em (2.0, 1.0)"

    elif modo == 2:
        print("Modo selecionado: [2] Vale Estreito (Aleatório - MÍNIMO)")
        x_opt = random.uniform(-5, 5)
        y_opt = random.uniform(-5, 5)
        a = random.uniform(1, 10)
        b = random.uniform(a + 20, a + 100) 
        expressao = a * (x - x_opt)**2 + b * (y - y_opt)**2
        ponto_otimo_conhecido = f"Mínimo em ({x_opt:.2f}, {y_opt:.2f})"

    elif modo == 3:
        print("Modo selecionado: [3] Ponto de Sela (Aleatório)")
        x_opt = random.uniform(-5, 5)
        y_opt = random.uniform(-5, 5)
        a = random.uniform(1, 10)
        b = random.uniform(1, 10)
        expressao = a * (x - x_opt)**2 - b * (y - y_opt)**2
        ponto_otimo_conhecido = f"Ponto de Sela em ({x_opt:.2f}, {y_opt:.2f})"

    elif modo == 4:
        print(f"Modo selecionado: [4] Função Manual (Professor): {funcao_string}")
        try:
            expressao = sym.sympify(funcao_string)
            ponto_otimo_conhecido = "Definido manualmente"
        except Exception as e:
            print(f"\n!!! ERRO NA FUNÇÃO INSERIDA: {e}. Revertendo para Padrão [1].")
            modo = 1 
            expressao = (x - 2)**2 + 50 * (y - 1)**2 
            ponto_otimo_conhecido = "Mínimo em (2.0, 1.0)"
    
    else:
        print(f"\n!!! MODO_TESTE = {modo} é inválido. Revertendo para Padrão [1].")
        modo = 1
        expressao = (x - 2)**2 + 50 * (y - 1)**2 
        ponto_otimo_conhecido = "Mínimo em (2.0, 1.0)"

    fnum = sym.lambdify((x,y), expressao, "numpy")
    
    print(f"\nFunção de Teste Definida: {expressao}")
    print(f"Ponto Crítico Conhecido: {ponto_otimo_conhecido}\n")
    
    return expressao, fnum, (x, y)

### --------------------------------------------------------------------------
### SEÇÃO 4: MÉTODOS DE OTIMIZAÇÃO (com parâmetro 'mode')
### --------------------------------------------------------------------------

def maxaclive(funcao, x, y, vetor_inicial, tolerancia, mode='descent', max_iter=1000):
    """
    Método de Aclive (ascent) ou Descida (descent) de Gradiente.
    """
    if mode == 'ascent':
        print("Executando: Aclive Máximo (Busca de Máximo)")
        signal = 1.0
    else:
        print("Executando: Aclive Máximo [Descida] (Busca de Mínimo)")
        signal = -1.0
        
    h = sym.symbols('h')
    x_k, y_k = vetor_inicial
    
    dfdx = sym.diff(funcao, x)
    dfdy = sym.diff(funcao, y)
    dfdx_num = sym.lambdify((x,y), dfdx, "numpy")
    dfdy_num = sym.lambdify((x,y), dfdy, "numpy")

    caminho = [(x_k, y_k)] 
    cont = 0
    
    for i in range(max_iter):
        cont += 1
        gradx = dfdx_num(x_k, y_k)
        grady = dfdy_num(x_k, y_k)
        
        grad_norm = (gradx**2 + grady**2)**0.5
        if grad_norm < tolerancia:
            break 

        # signal = +1 para Aclive, -1 para Descida
        p_x = signal * gradx
        p_y = signal * grady

        try:
            funcaoh = funcao.subs({x: x_k + h*p_x, y: y_k + h*p_y})
            dfuncaopdh = sym.diff(funcaoh, h)
            h_otimo, _ = newton_raphson(dfuncaopdh, h)
        except Exception as e:
            print(f"!!! Erro na busca de linha (provável divergência). Parando. {e}")
            break

        x_k = float(x_k + h_otimo * p_x)
        y_k = float(y_k + h_otimo * p_y)
        caminho.append((x_k, y_k))
        
        if np.isnan(x_k) or np.isnan(y_k):
            print("!!! Divergiu para NaN. Parando.")
            break

    erro_total = (dfdx_num(x_k, y_k)**2 + dfdy_num(x_k, y_k)**2)**0.5
    return (x_k, y_k), erro_total, cont, np.array(caminho)

def gradientes_conjugados(funcao, x, y, vetor_inicial, tolerancia, mode='descent', max_iter=1000):
    """
    Método de Gradientes Conjugados (Fletcher-Reeves) para Aclive ou Descida.
    """
    if mode == 'ascent':
        print("Executando: Grad. Conjugados (Busca de Máximo)")
        signal = 1.0
    else:
        print("Executando: Grad. Conjugados (Busca de Mínimo)")
        signal = -1.0
        
    h = sym.symbols('h') 
    x_k, y_k = vetor_inicial

    dfdx = sym.diff(funcao, x)
    dfdy = sym.diff(funcao, y)
    grad_num = sym.lambdify((x,y), [dfdx, dfdy], "numpy")

    caminho = [(x_k, y_k)] 
    
    g_k = np.array(grad_num(x_k, y_k), dtype=float)
    p_k = signal * g_k  # Direção inicial (Aclive ou Descida)
    g_dot_g_old = np.dot(g_k, g_k)
    cont = 0

    for i in range(max_iter):
        cont += 1
        
        if np.linalg.norm(g_k) < tolerancia:
            break

        p_x, p_y = p_k[0], p_k[1]
        try:
            funcaoh = funcao.subs({x: x_k + h*p_x, y: y_k + h*p_y})
            dfuncaopdh = sym.diff(funcaoh, h)
            h_otimo, _ = newton_raphson(dfuncaopdh, h)
        except Exception as e:
            print(f"!!! Erro na busca de linha (provável divergência). Parando. {e}")
            break
            
        x_k = float(x_k + h_otimo * p_x)
        y_k = float(y_k + h_otimo * p_y)
        caminho.append((x_k, y_k))
        
        if np.isnan(x_k) or np.isnan(y_k):
            print("!!! Divergiu para NaN. Parando.")
            break

        g_k_new = np.array(grad_num(x_k, y_k), dtype=float)

        g_dot_g_new = np.dot(g_k_new, g_k_new)
        if g_dot_g_old == 0: 
            break
        beta = g_dot_g_new / g_dot_g_old

        # Atualização da direção p_k para Aclive ou Descida
        p_k = (signal * g_k_new) + (beta * p_k)
        
        g_k = g_k_new
        g_dot_g_old = g_dot_g_new
        
    erro_total = np.linalg.norm(g_k)
    return (x_k, y_k), erro_total, cont, np.array(caminho)

def newton_multidimensional(funcao, x, y, vetor_inicial, tolerancia, max_iter=100):
    """
    Método de Newton Multidimensional puro.
    Encontra pontos críticos (máx, mín, ou sela).
    """
    print("Executando: Newton Multidimensional (Busca de Ponto Crítico)")
    grad = [sym.diff(funcao, x), sym.diff(funcao, y)]
    hess = sym.hessian(funcao, (x,y))

    grad_num = sym.lambdify((x,y), grad, "numpy")
    hess_num = sym.lambdify((x,y), hess, "numpy")

    x_k, y_k = vetor_inicial
    caminho = [(x_k, y_k)]
    cont = 0
    
    for i in range(max_iter):
        cont += 1
        
        g = np.array(grad_num(x_k, y_k), dtype=float)
        H = np.array(hess_num(x_k, y_k), dtype=float)
        
        if np.linalg.norm(g) < tolerancia:
            break
            
        try:
            delta = np.linalg.solve(H, -g) 
        except np.linalg.LinAlgError:
            print("!!! Hessiana singular! Método de Newton puro falhou.")
            break
            
        x_k, y_k = np.array([x_k, y_k]) + delta
        caminho.append((x_k, y_k))
        
        if np.isnan(x_k) or np.isnan(y_k):
            print("!!! Divergiu para NaN. Parando.")
            break
        
    erro_total = np.linalg.norm(grad_num(x_k, y_k))
    return (x_k, y_k), erro_total, cont, np.array(caminho)

def levenberg_marquardt(funcao, x, y, vetor_inicial, tolerancia, mode='descent', max_iter=100):
    """
    Método de Levenberg-Marquardt.
    'descent' (MÍNIMO): H_mod = H + alpha*I (garante H pos-def)
    'ascent' (MÁXIMO): H_mod = H - alpha*I (garante H neg-def)
    """
    if mode == 'ascent':
        print("Executando: Levenberg-Marquardt (Busca de Máximo)")
        signal = -1.0 # H - a*I
    else:
        print("Executando: Levenberg-Marquardt (Busca de Mínimo)")
        signal = 1.0  # H + a*I

    grad = [sym.diff(funcao, x), sym.diff(funcao, y)]
    hess = sym.hessian(funcao, (x,y))

    grad_num = sym.lambdify((x,y), grad, "numpy")
    hess_num = sym.lambdify((x,y), hess, "numpy")

    x_k, y_k = vetor_inicial
    caminho = [(x_k, y_k)]
    cont = 0
    alpha = 1.0
    decay = 0.5 

    for i in range(max_iter):
        cont += 1
        
        g = np.array(grad_num(x_k, y_k), dtype=float)
        H = np.array(hess_num(x_k, y_k), dtype=float)
        
        if np.linalg.norm(g) < tolerancia:
            break
        
        # Modifica a Hessiana baseado no modo (Mínimo ou Máximo)
        H_mod = H + (signal * alpha * np.eye(2))
        
        try:
            # O passo de Newton (-H^{-1}*g) é o mesmo para ambos
            delta = np.linalg.solve(H_mod, -g)
        except np.linalg.LinAlgError:
            alpha *= 10 
            continue
            
        x_k, y_k = np.array([x_k, y_k]) + delta
        caminho.append((x_k, y_k))
        
        if np.isnan(x_k) or np.isnan(y_k):
            print("!!! Divergiu para NaN. Parando.")
            break
        
        alpha *= decay 
        
    erro_total = np.linalg.norm(grad_num(x_k, y_k))
    return (x_k, y_k), erro_total, cont, np.array(caminho)

### --------------------------------------------------------------------------
### SEÇÃO 5: FUNÇÃO DE PLOTAGEM
### --------------------------------------------------------------------------

def plotar_comparacao(fnum, caminhos, nomes, vetor_inicial, expr_str, plot_title_prefix):
    """
    Plota o gráfico de contorno 2D.
    Ignora caminhos que resultaram em NaN (divergência).
    """
    if not caminhos: 
        print("\nNenhum caminho foi gerado. Gráfico cancelado.")
        return

    # Filtra caminhos vazios ou que contenham NaN
    caminhos_validos = []
    nomes_validos = []
    for cam, nome in zip(caminhos, nomes):
        if cam.size > 0 and not np.isnan(cam).any():
            caminhos_validos.append(cam)
            nomes_validos.append(nome)
        else:
            print(f"INFO: Caminho '{nome}' divergiu ou falhou, não será plotado.")
            
    if not caminhos_validos:
        print("\nTodos os métodos falharam ou divergiram. Gráfico cancelado.")
        return

    todos_x = np.concatenate([c[:,0] for c in caminhos_validos])
    todos_y = np.concatenate([c[:,1] for c in caminhos_validos])
    
    x_min, x_max = min(todos_x.min(), vetor_inicial[0]), max(todos_x.max(), vetor_inicial[0])
    y_min, y_max = min(todos_y.min(), vetor_inicial[1]), max(todos_y.max(), vetor_inicial[1])
    
    x_range = x_max - x_min if x_max > x_min else 1.0
    y_range = y_max - y_min if y_max > y_min else 1.0
    
    x_min -= x_range * 0.1
    x_max += x_range * 0.1
    y_min -= y_range * 0.1
    y_max += y_range * 0.1

    x_vals = np.linspace(x_min, x_max, 100)
    y_vals = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = fnum(X, Y)

    plt.figure(figsize=(14, 9))
    
    z_min, z_max = np.nanmin(Z), np.nanmax(Z)
    levels = np.linspace(z_min, z_max, 30) if z_min != z_max else 30

    plt.contour(X, Y, Z, levels=levels, cmap='viridis')
    plt.title(f"Comparação de Métodos ({plot_title_prefix})\nFunção: {expr_str}\nPonto Inicial: ({vetor_inicial[0]:.2f}, {vetor_inicial[1]:.2f})")
    plt.xlabel("x")
    plt.ylabel("y")
    
    plt.plot(vetor_inicial[0], vetor_inicial[1], 'rs', markersize=10, label=f'Ponto Inicial ({vetor_inicial[0]:.1f}, {vetor_inicial[1]:.1f})')
    
    cores = ['blue', 'pink', 'red', 'purple']
    estilos = ['-o', '--x', '--^', '-s']
    
    for i, (caminho, nome) in enumerate(zip(caminhos_validos, nomes_validos)):
        plt.plot(caminho[:, 0], caminho[:, 1], estilos[i % len(estilos)], 
                 label=f"{nome} ({len(caminho)-1} passos)", 
                 color=cores[i % len(cores)], markersize=5, alpha=0.7, markevery=5)

    plt.legend(loc='best')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    if 0.1 < (x_range / y_range) < 10.0:
        plt.axis('equal') 
    
    if 0.1 < (x_range / y_range) < 10.0:
        plt.axis('equal') 
    
    import os
    output_dir = "05_Otimizacao_Multidimensional/images"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    save_path = os.path.join(output_dir, 'result_plot.png')
    print(f"Salvando imagem do gráfico em {save_path}...")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    # plt.show()

### --------------------------------------------------------------------------
### SEÇÃO 6: EXECUÇÃO PRINCIPAL (MAIN com Lógica de Failover)
### --------------------------------------------------------------------------

def rodar_simulacao(mode):
    """
    Função helper para rodar um conjunto de simulações
    (seja 'descent' para MÍNIMO ou 'ascent' para MÁXIMO).
    """
    if mode == 'descent':
        prefix = "(Mínimo)"
        lm_mode = 'descent'
    else:
        prefix = "(Máximo)"
        lm_mode = 'ascent'
        
    resultados = {}
    caminhos = []
    nomes = []

    # --- 1. Aclive Máximo (Seu nome original) ---
    try:
        global_timers['newton_time'] = 0.0 # Zera o timer
        inicio = time.time()
        res, erro, cont, cam = maxaclive(expr, x, y, vetor_inicial, tolerancia, mode=mode)
        tempo_total = time.time() - inicio
        nr_time = global_timers['newton_time']
        nome_metodo = f'Aclive {prefix}'
        resultados[nome_metodo] = (res, erro, cont, tempo_total, nr_time)
        caminhos.append(cam)
        nomes.append(nome_metodo)
    except Exception as e:
        print(f"!!! Falha no Aclive {prefix}: {e}")

    # --- 2. Gradientes Conjugados ---
    try:
        global_timers['newton_time'] = 0.0 # Zera o timer
        inicio = time.time()
        res, erro, cont, cam = gradientes_conjugados(expr, x, y, vetor_inicial, tolerancia, mode=mode)
        tempo_total = time.time() - inicio
        nr_time = global_timers['newton_time']
        nome_metodo = f'Grad. Conj. {prefix}'
        resultados[nome_metodo] = (res, erro, cont, tempo_total, nr_time)
        caminhos.append(cam)
        nomes.append(nome_metodo)
    except Exception as e:
        print(f"!!! Falha nos Grad. Conj. {prefix}: {e}")

    # --- 3. Newton Multidimensional (Sempre chamado, é agnóstico) ---
    try:
        global_timers['newton_time'] = 0.0 # Zera o timer (NR time será 0.0)
        inicio = time.time()
        res, erro, cont, cam = newton_multidimensional(expr, x, y, vetor_inicial, tolerancia)
        tempo_total = time.time() - inicio
        nr_time = global_timers['newton_time']
        nome_metodo = 'Newton (Ponto Crítico)'
        resultados[nome_metodo] = (res, erro, cont, tempo_total, nr_time)
        caminhos.append(cam)
        nomes.append(nome_metodo)
    except Exception as e:
        print(f"!!! Falha no Newton: {e}")

    # --- 4. Levenberg-Marquardt ---
    try:
        global_timers['newton_time'] = 0.0 # Zera o timer (NR time será 0.0)
        inicio = time.time()
        res, erro, cont, cam = levenberg_marquardt(expr, x, y, vetor_inicial, tolerancia, mode=lm_mode)
        tempo_total = time.time() - inicio
        nr_time = global_timers['newton_time']
        nome_metodo = f'Levenberg {prefix}'
        resultados[nome_metodo] = (res, erro, cont, tempo_total, nr_time)
        caminhos.append(cam)
        nomes.append(nome_metodo)
    except Exception as e:
        print(f"!!! Falha no Levenberg {prefix}: {e}")
        
    return resultados, caminhos, nomes

# --- Início da Execução ---
if __name__ == "__main__":
    
    # 1. Configurar o problema (agora passando os globais como args)
    expr, fnum, (x, y) = configurar_funcao_teste(MODO_TESTE, FUNCAO_PROFESSOR_STRING)
    
    tolerancia = 1e-6
    vetor_inicial = (random.uniform(-10, 10), random.uniform(-10, 10)) 
    print(f"Iniciando otimização do ponto: ({vetor_inicial[0]:.2f}, {vetor_inicial[1]:.2f})\n")

    # 2. TENTATIVA 1: Buscando PONTO DE MÍNIMO
    print("\n" + "="*80)
    print("--- TENTATIVA 1: Buscando PONTO DE MÍNIMO ---")
    print("="*80 + "\n")
    plot_title_prefix = "Busca de MÍNIMO"
    
    resultados, caminhos, nomes = rodar_simulacao(mode='descent')
    
    # 3. CHECAGEM DE FALHA (FAILOVER)
    # A falha é definida se os métodos de gradiente (que DEVEM achar um mínimo)
    # divergiram para NaN.
    
    res_grad = resultados.get('Aclive (Mínimo)', ([np.nan],0,0,0,0))
    res_cg = resultados.get('Grad. Conj. (Mínimo)', ([np.nan],0,0,0,0))
    
    # Checa se o resultado de CADA UM dos métodos de gradiente é NaN
    grad_failed = np.isnan(res_grad[0]).any()
    cg_failed = np.isnan(res_cg[0]).any()

    if grad_failed and cg_failed:
        print("\n" + "="*80)
        print("--- Busca por MÍNIMO falhou (divergência detectada). ---")
        print("--- TENTATIVA 2: Buscando PONTO DE MÁXIMO. ---")
        print("="*80 + "\n")
        
        plot_title_prefix = "Busca de MÁXIMO"
        
        # Roda a simulação novamente, mas caçando o MÁXIMO
        resultados, caminhos, nomes = rodar_simulacao(mode='ascent')


    # 4. Imprimir resumo em tabela
    print("\n" + "="*90)
    print(f"--- Resumo da Execução Final ({plot_title_prefix}) ---")
    print("="*90)
    print(f"{'Método':<28} | {'Passos':<6} | {'Erro Final':<10} | {'Tempo (Total / N-R 1D)':<22} | Ponto Final (x, y)")
    print("-"*90)
    for nome, (ponto, erro, passos, tempo, nr_time) in resultados.items():
        tempo_str = f"{tempo:<6.4f}s (NR: {nr_time:.4f}s)"
        
        if np.isnan(ponto).any():
            ponto_str = "(DIVERGIU)"
            erro_str = "NaN"
        else:
            ponto_str = f"({ponto[0]:.4f}, {ponto[1]:.4f})"
            erro_str = f"{erro:<10.2e}"
            
        print(f"{nome:<28} | {passos:<6} | {erro_str:<10} | {tempo_str:<22} | {ponto_str}")
    print("="*90)

    # 5. Plotar a comparação
    plotar_comparacao(fnum, caminhos, nomes, vetor_inicial, str(expr), plot_title_prefix)
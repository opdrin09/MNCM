
#%%
# Programa 4 - Solução Numérica da Equação de Condução de Calor 1D Transiente
# Autoria: Pedro Henrique da Silva Costa
# Data: 27 de Outubro de 2025
#### Disclaimer: LLM foram utilizadas para organizar, comentar e #####
#     implementar melhorias (como a troca da cotangente
#     por cosseno/seno no solver de raízes e na parte
#     da animação, principalmente).


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time 
from pathlib import Path

# ======================================================================================
# PARTE A: AS FERRAMENTAS NUMÉRICAS
# ======================================================================================

# --- Definindo o Diretório Base para Salvar os Arquivos ---
BASE_DIR = Path(__file__).resolve().parent
print(f"Salvando todos os arquivos em: {BASE_DIR}")
images_dir = BASE_DIR / "images"
if not images_dir.exists():
    images_dir.mkdir()

# --- Ferramenta 1: O Solver Tridiagonal (Tradução do FORTRAN) ---
def thomas_sol(e, f, g, r):
    """
    Solucionador Tridiagonal (TDMA) traduzido do pseudocódigo do PDF da aula.
    e: diagonal inferior
    f: diagonal principal
    g: diagonal superior
    r: vetor do lado direito
    """
    n = len(f)
    e_prime = np.copy(e)
    f_prime = np.copy(f)
    r_prime = np.copy(r)
    x = np.zeros(n)

    # Bloco 1: Decomposição L.U 
    for k in range(1, n):
        e_prime[k] = e_prime[k] / f_prime[k-1]
        f_prime[k] = f_prime[k] - e_prime[k] * g[k-1]

    # Bloco 2: Substituição progressiva 
    for k in range(1, n):
        r_prime[k] = r_prime[k] - e_prime[k] * r_prime[k-1]

    # Bloco 3: Substituição regressiva
    x[n-1] = r_prime[n-1] / f_prime[n-1]
    for k in range(n-2, -1, -1):
        x[k] = (r_prime[k] - g[k] * x[k+1]) / f_prime[k]
        
    return x

# --------------------------------------------------------------------------------------
# Ferramenta 2: Solver de Raízes (Newton-Raphson)
# --------------------------------------------------------------------------------------
def find_roots_newton(Bi, n_termos):
    """
    Encontra as 'n_termos' primeiras raízes da equação transcendental
    λ = Bi * cot(λ) 
    
    Para evitar problemas de divisão por zero com a cotangente,
    reescreve-se como λ = Bi * cos(λ) / sin(λ),
    que se torna a função f(λ) = 0 onde:
    f(λ) = Bi * cos(λ) - λ * sin(λ)
    
    Este código implementa o método de Newton-Raphson para encontrar
    as raízes desta função f(λ).
    """
    lambdas = []
    
    # --- Definição da Função e sua Derivada ---
    
    def f_lambda(l, Bi_val):
        """ A função a ter a raiz encontrada: f(λ) = Bi*cos(λ) - λ*sin(λ) """
        return Bi_val * np.cos(l) - l * np.sin(l)

    def f_prime_lambda(l, Bi_val):
        """ A derivada da função: f'(λ) = -(Bi+1)sin(λ) - λ*cos(λ) """
        # Derivada de (Bi*cos(l)): -Bi*sin(l)
        # Derivada de (-l*sin(l)): -(1*sin(l) + l*cos(l)) [Regra do Produto]
        return -(Bi_val + 1) * np.sin(l) - l * np.cos(l)

    # --- Loop para Encontrar as N Raízes ---
    for n in range(1, n_termos + 1):
        # Chute inicial para a n-ésima raiz.
        lambda_n = (n - 1) * np.pi + 0.5 
        
        # Inicia o processo iterativo de Newton-Raphson
        for _ in range(10): # 10 iterações é mais que suficiente
            f_val = f_lambda(lambda_n, Bi)
            f_prime_val = f_prime_lambda(lambda_n, Bi)
            
            # Evita divisão por zero
            if np.abs(f_prime_val) < 1e-10: 
                break
                
            delta_l = f_val / f_prime_val
            lambda_n = lambda_n - delta_l
            
            # Critério de convergência
            if np.abs(delta_l) < 1e-10:
                break
                
        lambdas.append(lambda_n)
        
    return np.array(lambdas)

# --------------------------------------------------------------------------------------
# Ferramenta 3: Solução Analítica Exata
# --------------------------------------------------------------------------------------
def solucao_analitica(x_pos, t, L, alpha, Bi_geo, T_i, T_inf, n_termos=100):
    """
    Calcula a solução analítica exata da série.
    Esta função CHAMA o solver de raízes (find_roots_newton).
    
    Argumentos:
    Bi_geo: É o Número de Biot da geometria (h*L/k), que é o 'Bi'
            usado na equação da cotangente.
    """
    
    # 1. Encontra os autovalores (λn) usando o método de Newton
    lambdas = find_roots_newton(Bi_geo, n_termos)
    
    # 2. Calcula o somatório da série
    theta = 0.0 # theta é a temperatura adimensional (T-Tinf)/(Ti-Tinf)
    x_star = x_pos / L # Posição adimensional x/L
    Fo_geo = alpha * t / L**2 # Fourier adimensional

    for ln in lambdas:
        # Esta é a fórmula do coeficiente C_n da série
        C_n = (4 * np.sin(ln)) / (2*ln + np.sin(2*ln))
        
        # Termo do somatório
        termo_soma = C_n * np.cos(ln * x_star) * np.exp(-ln**2 * Fo_geo)
        
        # Acumula o somatório
        theta += termo_soma
    
    # 3. Converte theta de volta para Temperatura
    T = theta * (T_i - T_inf) + T_inf
    return T

# ======================================================================================
# PARTE B: O "MOTOR" DA SIMULAÇÃO NUMÉRICA
# ======================================================================================
def run_simulation(L, k, rho, Cp, h, T_inf, T_initial, q_dot, nx, tempo_total, dt):
    """
    Função principal que roda a simulação numérica transiente.
    """
    nt = int(tempo_total / dt) # Número de passos no tempo
    
    # --- Constantes Derivadas (Numéricas) ---
    alpha = k / (rho * Cp)          # Difusividade
    dx = L / (nx - 1)               # Espaçamento
    Fo_num = (alpha * dt) / (dx**2) # Fourier numérico 
    Bi_num = (h * dx) / k           # Biot numérico 
    A = (q_dot / (rho * Cp)) * dt   # Termo fonte 

    # --- Montagem dos vetores da Matriz [A] (baseado no PDF, pág. 17) ---
    # f: diagonal principal 
    f = np.full(nx, 1 + 2*Fo_num) # Cria um vetor cheio de 1+2*Fo_num
    f[nx-1] = 1 + 2*Fo_num + 2*Fo_num*Bi_num # Converte a última coordenada do vetor
    
    # e: diagonal inferior 
    e = np.full(nx, -Fo_num)
    e[nx-1] = -2*Fo_num # Contorno nó 7 (índice nx-1)
    e[0] = 0.0          # Não usado

    # g: diagonal superior 
    g = np.full(nx, -Fo_num)
    g[0] = -2*Fo_num    # Contorno nó 1 (índice 0)
    g[nx-1] = 0.0       # Não usado
    
    # --- Inicialização ---
    T = np.full(nx, T_initial) #Vetor de temperaturas no estado inicial 
    posicoes = np.linspace(0, L, nx)
    tempos = np.linspace(0, tempo_total, nt + 1)
    
    historico_T = np.zeros((nt + 1, nx)) #Cria o histórico de temperaturas
    historico_T[0] = T #Armazena o estado inicial

    # --- Loop Principal no Tempo ---
    for i in range(nt):
        T_p = np.copy(T)  # Temperaturas no passo anterior
        
        # Monta o vetor 'r' (lado direito)
        r = T_p + A # Fórmula base para nós internos
        # Corrige o último nó (convecção)
        r[nx-1] = T_p[nx-1] + 2*Fo_num*Bi_num*T_inf + A
        
        # Resolve o sistema!
        T = thomas_sol(e, f, g, r)
        
        historico_T[i+1] = T
        
    return posicoes, tempos, historico_T

# ======================================================================================
# PARTE C: VALIDAÇÃO (q_dot = 0)
# ======================================================================================
print("Iniciando Tarefa 1: VALIDAÇÃO (sem geração de calor)...")
start_time = time.time()

# --- Parâmetros Físicos e Numéricos (Validação) ---
L_val = 0.005;   k_val = 2.5; rho_val = 10500;
Cp_val = 320; h_val = 20000; T_inf_val = 300.0
T_initial_val = 500.0 # Começa quente para ver o resfriamento
q_dot_val = 0.0       # GERAÇÃO ZERO PARA VALIDAR
nx_val = 21           
t_total_val = 7
dt_val = 0.1

# --- Roda a simulação de validação ---
pos_val, tempos_val, hist_T_val = run_simulation(
    L_val, k_val, rho_val, Cp_val, h_val, T_inf_val, T_initial_val, 
    q_dot_val, nx_val, t_total_val, dt_val
)
T_numerico_final = hist_T_val[-1] # Pega o último perfil de T

# --- Roda a solução analítica ---
Bi_geometria = (h_val * L_val) / k_val # Biot da geometria (para a série)
alpha_val = k_val / (rho_val * Cp_val)
T_analitico_final = solucao_analitica(pos_val, t_total_val, L_val, alpha_val, Bi_geometria, T_initial_val, T_inf_val)

# --- Plotagem da Validação (Estático) ---
plt.figure("TAREFA 1: VALIDAÇÃO", figsize=(10, 6))
plt.plot(pos_val * 1000, T_numerico_final, 'o', label='Solução Numérica (Thomas)', color='red', markersize=5)
plt.plot(pos_val * 1000, T_analitico_final, '--', label='Solução Analítica Exata', color='black', linewidth=2.5)
plt.title('Validação da Solução Numérica (q̇ = 0)')
plt.xlabel('Posição (mm) - 0 é o centro')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout() # Ajusta o layout antes de salvar
print("Salvando gráfico estático de validação...")
plt.savefig(images_dir / "tarefa_1_validacao_perfil.png", dpi=300)

erro_max = np.max(np.abs(T_numerico_final - T_analitico_final))
print(f"Validação concluída em {time.time() - start_time:.2f}s. Erro máximo: {erro_max:.3f} °C")

# --- Plotagem da Validação (Animação) ---
fig_anim_val, ax_anim_val = plt.subplots(num="TAREFA 1: Animação de Validação", figsize=(10, 6))
ax_anim_val.set_xlim(L_val * 1000, 0) # Eixo x de 5mm a 0mm
ax_anim_val.set_ylim(T_inf_val - 20, T_initial_val + 20) # Limites para resfriamento
ax_anim_val.set_xlabel('Posição (mm)')
ax_anim_val.set_ylabel('Temperatura (°C)')
ax_anim_val.grid(True)
plt.tight_layout() # Ajusta o layout

linha_val, = ax_anim_val.plot(pos_val * 1000, hist_T_val[0], 'o-', color='blue')
titulo_tempo_val = ax_anim_val.set_title('Tempo = 0.0 s')

def update_anim_val(frame):
    perfil_T_val = hist_T_val[frame]
    linha_val.set_ydata(perfil_T_val)
    titulo_tempo_val.set_text(f'Tempo = {tempos_val[frame]:.1f} s')
    return linha_val, titulo_tempo_val

ani_val = FuncAnimation(fig_anim_val, update_anim_val, frames=len(tempos_val), 
                        interval=50, blit=True, repeat=False)
print("Salvando animação de validação... (isso pode demorar)")
try:
    ani_val.save(images_dir / "tarefa_1_validacao_animacao.gif", writer='pillow', fps=20)
    print(f"Animação de validação salva como '{images_dir / 'tarefa_1_validacao_animacao.gif'}'")
except Exception as e:
    print(f"Erro ao salvar animação de validação: {e}. Verifique se 'pillow' está instalado.")


# ======================================================================================
# PARTE D: APLICAÇÃO (q_dot > 0)
# ======================================================================================
print("\nIniciando Tarefa 2: APLICAÇÃO (com geração de calor)...")
start_time = time.time()

# --- Parâmetros Físicos e Numéricos (Aplicação) ---
L_app = 0.005; k_app = 2.5; rho_app = 10500; Cp_app = 320; h_app = 20000; T_inf_app = 300.0
T_initial_app = 300.0 # Começa frio (igual ao refrigerante)
q_dot_app = 1.5e8     # GERAÇÃO DE CALOR LIGADA
nx_app = 21           # (Usando o mesmo nx da validação)
t_total_app = 8.0
dt_app = 0.1

# --- Roda a simulação de aplicação ---
pos_app, tempos_app, hist_T_app = run_simulation(
    L_app, k_app, rho_app, Cp_app, h_app, T_inf_app, T_initial_app, 
    q_dot_app, nx_app, t_total_app, dt_app
)
T_final_app = hist_T_app[-1]

print(f"Aplicação concluída em {time.time() - start_time:.2f}s.")
print(f"Temperatura final no centro: {T_final_app[0]:.2f} °C")
print(f"Temperatura final na superfície: {T_final_app[-1]:.2f} °C")

# --- Visualização 1: Perfil de Temperatura ---
plt.figure("TAREFA 2: Gráfico 1 - Perfil Final", figsize=(10, 6))
plt.plot(pos_app * 1000, T_final_app, 'o-', color='red', label='Perfil Final (com q̇)')
plt.plot(pos_app * 1000, hist_T_app[0], '--', color='blue', label='Perfil Inicial')
plt.title(f'Perfil de Temperatura Final (após {t_total_app} s)')
plt.xlabel('Posição (mm) - 0 é o centro')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.gca().invert_xaxis()
plt.tight_layout()
print("Salvando gráfico de perfil da aplicação...")
plt.savefig(images_dir / "tarefa_2_aplicacao_perfil.png", dpi=300)

# --- Visualização 2: Campo de Cores (Heatmap) ---
plt.figure("TAREFA 2: Gráfico 2 - Heatmap", figsize=(10, 6))
T_transposto = hist_T_app.T # Transpõe para (posição, tempo)
X_mesh, Y_mesh = np.meshgrid(tempos_app, pos_app * 1000)
mapa_calor = plt.pcolormesh(X_mesh, Y_mesh, T_transposto, shading='auto', cmap='inferno')
plt.colorbar(mapa_calor, label='Temperatura (°C)')
plt.title('Campo de Cores: Temperatura vs. Posição e Tempo')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (mm)')
plt.gca().invert_yaxis() # Coloca o centro (0mm) no topo
plt.tight_layout()
print("Salvando gráfico de heatmap da aplicação...")
plt.savefig(images_dir / "tarefa_2_aplicacao_heatmap.png", dpi=300)

# --- Visualização 3: Animação ---
fig_anim, ax_anim = plt.subplots(num="TAREFA 2: Gráfico 3 - Animação", figsize=(10, 6))
ax_anim.set_xlim(L_app * 1000, 0)
ax_anim.set_ylim(T_initial_app - 10, T_final_app[0] + 50)
ax_anim.set_xlabel('Posição (mm)')
ax_anim.set_ylabel('Temperatura (°C)')
ax_anim.grid(True)
plt.tight_layout() # Ajusta o layout

linha, = ax_anim.plot(pos_app * 1000, hist_T_app[0], 'o-', color='red')
titulo_tempo = ax_anim.set_title('Tempo = 0.0 s')

def update_anim(frame):
    perfil_T = hist_T_app[frame]
    linha.set_ydata(perfil_T)
    titulo_tempo.set_text(f'Tempo = {tempos_app[frame]:.1f} s')
    return linha, titulo_tempo

# Intervalo = 1000ms / 20fps = 50ms
ani = FuncAnimation(fig_anim, update_anim, frames=len(tempos_app), 
                    interval=50, blit=True, repeat=False)

print("Salvando animação da aplicação... (isso pode demorar)")
try:
    ani.save(images_dir / "tarefa_2_aplicacao_animacao.gif", writer='pillow', fps=20)
    print("Animação da aplicação salva como 'tarefa_2_aplicacao_animacao.gif'")
except Exception as e:
    print(f"Erro ao salvar animação da aplicação: {e}. Verifique se 'pillow' está instalado.")


# ======================================================================================
# PARTE E: EXIBIR TODOS OS GRÁFICOS
# ======================================================================================
print("\nScript finalizado.")
# plt.show()
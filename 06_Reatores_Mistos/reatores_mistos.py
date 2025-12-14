# -----------------------------------------------------------------------------
# Aluno: Pedro Henrique da Silva Costa
# Engenharia Mecânica - UnB
# Matrícula: 231012639
# Repositório: https://github.com/opdrin09/MNCM/tree/main
# Solução do problema da resposta transiente de um sistema de reatores mistos.
# Data: 11/12/2025

# --------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import os
output_dir = "06_Reatores_Mistos/images"

if os.path.isfile(output_dir):
    os.remove(output_dir)

if not os.path.exists(output_dir):
     os.makedirs(output_dir)
# --- Parâmetros do Sistema ---
# Vazões (Q) 
Q = {
    '01': 5, '03': 8, '12': 3, '15': 3,
    '23': 1, '24': 1, '25': 1,
    '31': 1, '34': 8,
    '44': 11,
    '54': 2, '55': 2
}
# Concentrações de entrada
c_in = {'01': 10, '03': 20}

# Volumes (V)
# OBS: O problema original trata de regime permanente, onde V é irrelevante.
# Para análise transiente, assumiu-se V = 1 m³ para todos os reatores.
V = np.ones(5) 

# --- Definição das EDOs (dc/dt) ---
def F(c):
    dc = np.zeros(5)
    # Balanço de massa: V * dc/dt = Q_in*c_in - Q_out*c_out
    dc[0] = (Q['01']*c_in['01'] + Q['31']*c[2] - Q['12']*c[0] - Q['15']*c[0]) / V[0]
    dc[1] = (Q['12']*c[0] - Q['23']*c[1] - Q['24']*c[1] - Q['25']*c[1]) / V[1]
    dc[2] = (Q['03']*c_in['03'] + Q['23']*c[1] - Q['31']*c[2] - Q['34']*c[2]) / V[2]
    dc[3] = (Q['24']*c[1] + Q['34']*c[2] + Q['54']*c[4] - Q['44']*c[3]) / V[3]
    dc[4] = (Q['15']*c[0] + Q['25']*c[1] - Q['54']*c[4] - Q['55']*c[4]) / V[4]
    return dc

# --- Métodos Numéricos ---

def RK4_classico(vetor_inicial, h, t_final):
    t = 0
    c = np.array(vetor_inicial, dtype=float)
    results = [(t, *c)]
    n_steps = int(t_final / h)
    
    for _ in range(n_steps):
        k1 = F(c)
        k2 = F(c + h*k1/2)
        k3 = F(c + h*k2/2)
        k4 = F(c + h*k3)
        c = c + h*(k1 + 2*k2 + 2*k3 + k4)/6
        t += h
        results.append((t, *c))
    return np.array(results)

def RK_embutido(vetor_inicial, h_inicial, t_final, tol=1e-5):
    t = 0
    h = h_inicial
    c = np.array(vetor_inicial, dtype=float)
    results = [(t, *c)]

    while t < t_final:
        if t + h > t_final: h = t_final - t

        # Coeficientes Cash-Karp
        k1 = F(c)
        k2 = F(c + h * k1 / 5)
        k3 = F(c + h * (3/40 * k1 + 9/40 * k2))
        k4 = F(c + h * (3/10 * k1 - 9/10 * k2 + 6/5 * k3))
        k5 = F(c + h * (-11/54 * k1 + 5/2 * k2 - 70/27 * k3 + 35/27 * k4))
        k6 = F(c + h * (1631/55296 * k1 + 175/512 * k2 + 575/13824 * k3 + 44275/110592 * k4 + 253/4096 * k5))

        y5 = c + h * (37/378 * k1 + 250/621 * k3 + 125/594 * k4 + 512/1771 * k6)
        y4 = c + h * (2825/27648 * k1 + 18575/48384 * k3 + 13525/55296 * k4 + 277/14336 * k5 + 1/4 * k6)

        erro = np.max(np.abs(y5 - y4))
        escala = np.max(np.abs(c)) + 1e-3 
        delta = tol * escala

        if erro <= delta:
            t += h
            c = y5
            results.append((t, *c))
            if erro < delta/10: h = h * 2
        else:
            h = 0.9 * h * (delta / (erro + 1e-10))**0.2 
            
    return np.array(results)

# --- Execução ---

c0 = [0, 0, 0, 0, 0]   
h = 0.01
t_final = 10

sol_classica = RK4_classico(c0, h, t_final)
sol_embutido = RK_embutido(c0, h, t_final)

# --- Plotagem ---
plt.figure(figsize=(10, 6))

colors = ['b', 'g', 'r', 'c', 'm']
labels = ['C1', 'C2', 'C3', 'C4', 'C5']

# Plot RK4 Clássico
for i in range(5):
    plt.plot(sol_classica[:,0], sol_classica[:,i+1], 
             color=colors[i], linestyle='-', linewidth=1.5, alpha=0.6,
             label=f'{labels[i]} (RK4)')

# Plot RK Embutido
skip = 5 
for i in range(5):
    plt.scatter(sol_embutido[::skip,0], sol_embutido[::skip,i+1], 
                color=colors[i], marker='o', s=25, facecolors='none', 
                label=f'{labels[i]} (RKF45)')

plt.title('Dinâmica de Concentração: Comparação RK4 vs RKF45')
plt.xlabel('Tempo (s)')
plt.ylabel('Concentração (mg/m³)') # Unidade corrigida conforme PDF Pag 1
plt.grid(True, linestyle='--', alpha=0.6)

# Legenda com todas as 10 entradas, posicionada fora da área de dados se possível
plt.legend(loc='lower right', ncol=2, fontsize='small')

plt.tight_layout()
save_path = os.path.join(output_dir, 'reatores_mistos_plot.png')
plt.savefig(save_path, dpi=300)
plt.show()
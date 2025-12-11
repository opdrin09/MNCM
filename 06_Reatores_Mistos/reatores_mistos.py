
import numpy as np
import matplotlib.pyplot as plt
import os

# Definição das EDOs
def fluid_reactor_ode(t, Y):
    Ca, T = Y
    
    # Parâmetros
    Ca_in = 2000
    VOL = 10
    tau = 50
    k0 = 1.0e8
    E = 7.04e4
    R = 8.314
    DH = 2e5
    rho = 1e3
    cp = 4.18e3
    UA = 1.5e3
    Te = 330
    Tc = 280

    k = k0 * np.exp(-E / (R * T))
    
    dCadt = (1/tau) * (Ca_in - Ca) - k * Ca
    dTdt = (1/rho/cp) * ( (rho*cp/tau)*(Te - T) + (-DH)*k*Ca - (UA/VOL)*(T - Tc) )
    
    return np.array([dCadt, dTdt])

# Runge-Kutta de 4ª Ordem (RK4)
def rk4_step(func, t, y, dt):
    k1 = func(t, y)
    k2 = func(t + 0.5*dt, y + 0.5*dt*k1)
    k3 = func(t + 0.5*dt, y + 0.5*dt*k2)
    k4 = func(t + dt, y + dt*k3)
    return y + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

# Runge-Kutta-Fehlberg (RK45 - Embedded)
def rk45_step(func, t, y, dt):
    # Coeficientes Butcher para RKF45
    c2 = 1/4;   a21 = 1/4
    c3 = 3/8;   a31 = 3/32;    a32 = 9/32
    c4 = 12/13; a41 = 1932/2197; a42 = -7200/2197; a43 = 7296/2197
    c5 = 1;     a51 = 439/216;   a52 = -8;         a53 = 3680/513;   a54 = -845/4104
    c6 = 1/2;   a61 = -8/27;     a62 = 2;          a63 = -3544/2565; a64 = 1859/4104; a65 = -11/40

    b1 = 16/135; b3 = 6656/12825; b4 = 28561/56430; b5 = -9/50; b6 = 2/55
    b1_star = 25/216; b3_star = 1408/2565; b4_star = 2197/4104; b5_star = -1/5

    k1 = dt * func(t, y)
    k2 = dt * func(t + c2*dt, y + a21*k1)
    k3 = dt * func(t + c3*dt, y + a31*k1 + a32*k2)
    k4 = dt * func(t + c4*dt, y + a41*k1 + a42*k2 + a43*k3)
    k5 = dt * func(t + c5*dt, y + a51*k1 + a52*k2 + a53*k3 + a54*k4)
    k6 = dt * func(t + c6*dt, y + a61*k1 + a62*k2 + a63*k3 + a64*k4 + a65*k5)

    y_next_4th = y + b1*k1 + b3*k3 + b4*k4 + b5*k5 + b6*k6
    y_next_5th = y + b1_star*k1 + b3_star*k3 + b4_star*k4 + b5_star*k5 
    
    return y_next_4th

# Configuração da Simulação
t_start = 0.0
t_end = 100.0 # Tempo suficiente para atingir estacionário
dt = 0.5      # Passo de tempo
N_steps = int((t_end - t_start) / dt)

# Condições Iniciais
Ca0 = 1200.0 
T0 = 350.0   
Y0 = np.array([Ca0, T0])

# Arrays para armazenar solução
t_vals = np.linspace(t_start, t_end, N_steps+1)
sol_RK4_conc = np.zeros(N_steps+1)
sol_RK4_temp = np.zeros(N_steps+1)
sol_RK4_conc_embedded = np.zeros(N_steps+1) # Para comparação visual

sol_RK4_conc[0] = Ca0
sol_RK4_temp[0] = T0
sol_RK4_conc_embedded[0] = Ca0

curr_Y_RK4 = Y0.copy()
curr_Y_RK45 = Y0.copy()

print("Iniciando simulação...")
for i in range(N_steps):
    t = t_vals[i]
    
    # Método RK4 Clássico
    curr_Y_RK4 = rk4_step(fluid_reactor_ode, t, curr_Y_RK4, dt)
    sol_RK4_conc[i+1] = curr_Y_RK4[0]
    sol_RK4_temp[i+1] = curr_Y_RK4[1]
    
    # Método RK "Embedded" (Usando RK45 simplificado)
    curr_Y_RK45 = rk45_step(fluid_reactor_ode, t, curr_Y_RK45, dt)
    sol_RK4_conc_embedded[i+1] = curr_Y_RK45[0]

print("Simulação concluída.")

# Plotagem
plt.figure(figsize=(10, 6))
output_dir = "06_Reatores_Mistos/images"

if os.path.isfile(output_dir):
    os.remove(output_dir)

if not os.path.exists(output_dir):
     os.makedirs(output_dir)

plt.plot(t_vals, sol_RK4_conc, label='RK4 (Implementado)', color='blue', linestyle='--')
plt.plot(t_vals, sol_RK4_conc_embedded, label='RK45 (Embedded)', color='red', alpha=0.6)
plt.title(f'Resposta Transiente - Concentração (N={N_steps})')
plt.xlabel('Tempo (t)')
plt.ylabel('Concentração (Ca)')
plt.legend()
plt.grid(True)
plt.tight_layout()

save_path = os.path.join(output_dir, 'reatores_mistos_plot.png')
plt.savefig(save_path, dpi=300)
print(f"Gráfico salvo em {save_path}")
# plt.show()
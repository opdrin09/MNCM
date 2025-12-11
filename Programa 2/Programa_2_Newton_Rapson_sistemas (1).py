#Instale numpy, numba e matplotlib para a visualização do código
#%%
import time
from numpy import exp, sqrt
import matplotlib.pyplot as plt
import numpy as np
import numba
start_time = time.time()

########### VALORES DAS VARIÁVEIS FIXAS ##########
ca_in = 2000
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
###################################################


@numba.jit(nopython=True, cache=True) # Usa-se numba para uma compilação mais rápida
def xy_system(x, y): # sistema de equações dado no enunciado

    
    f1 = 0.0005 * x + (50000 * exp(-9622 / y)) * x - 1
    f2 = (2526 * exp(-9622 / y)) * x - 0.00312 * y + 1
    
    df1dx = 0.0005 + 50000 * exp(-9622 / y)
    df1dy = (4.811e8 * x * exp(-9622 / y)) / y**2
    df2dx = 2526 * exp(-9622 / y)
    df2dy = (2.431e7 * x * exp(-9622 / y)) / y**2 - 0.00312

    return f1, f2, df1dx, df1dy, df2dx, df2dy

@numba.jit(nopython=True, cache=True)
def caT_system(ca, T): #sistema de equações usando-se os valores de referência
    k_T = k0 * exp(-E / (R * T))
    dk_T = (E / (R * T**2)) * k_T
    nan_package = (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)
    if T < 0:
       #Verfica se T não é negativo (fisicamente impossível)
        return nan_package

    k_T = k0 * exp(-E / (R * T))
    if k_T > 1e12: # Verifica se k_T não explodiu para infinito (máquina)
        return nan_package
    
    f1 = ca_in - ca - tau * k_T * ca
    f2 = rho * cp * VOL / tau * (Te - T) - UA * (T - Tc) + DH * VOL * k_T * ca
    
    df1dca = -k_T * tau - 1
    df1dT = -tau * ca * dk_T
    df2dca = DH * VOL * k_T
    df2dT = -rho * cp * VOL / tau - UA + DH * VOL * ca * dk_T
    
    return f1, f2, df1dca, df1dT, df2dca, df2dT

@numba.jit(nopython=True, cache=True)

def resolver(x0, y0, system_funcs, p): #função que aplica o método numérico
    contador = 0
    dif = float('inf')
    xi = float(x0)
    yi = float(y0)
    
    while dif > 1e-8:
        f1, f2, d1dx, d1dy, d2dx, d2dy = system_funcs(xi, yi)
        
        J = [[d1dx, d1dy], 
             [d2dx, d2dy]]
        
        detJ = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if sqrt(detJ**2) < 1e-12:
            detJ = np.nan

        xm1 = xi - (1 / detJ) * (f1 * d2dy - f2 * d1dy)
        ym1 = yi - (1 / detJ) * (f2 * d1dx - f1 * d2dx)
        
        difx = np.sqrt((xm1 - xi)**2)
        dify = np.sqrt((ym1 - yi)**2)
        
        if difx > dify:
            dif = difx
        else:
            dif = dify
            
        xi = xm1
        yi = ym1
        contador += 1
        if contador > 1e3: 
            return np.nan, np.nan #verifica se a convergência não travou por falha do método
        
    if p == 1:   
        with numba.objmode():
            # Este código roda no interpretador Python normal
            print(f'x{contador} = {xi}, | y{contador} = {yi}, | dif = {dif}')
    return xi, yi
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print('A letra a) é resolvida em:')
resolver(1, 1, xy_system, 1)
print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
print()
print()
print()
Vetortesteca = [600, 1200, 2000] #Valores sugeridos no enunciado
VetortesteT = [305, 350, 420]


for c in range(0,3):#teste para os valores sugeridos
        print()
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(f'Para a combinação ca = {Vetortesteca[c]} e  T_0 = {VetortesteT[c]}:')
       
        resolver(Vetortesteca[c], VetortesteT[c], caT_system, 1)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print()





a = input('Você deseja escolher seus próprios valores \n para visualizar no mapa de calor? [S/N]:    ')
print()
if a in 'SssimSimSIM':
  T0menor = T0maior = ca0maior = ca0menor = -1
  while T0menor <= 0 or T0maior <= 0 or ca0menor < 0 or ca0maior < 0:
    print('Por favor digite valores reais positivos para os limites e valores inteiros positivos para os passos!')
    print()
    print('Altos valores para o número de passos pode fazer o código demorar muito a rodar! ')
    print()
    ca0menor = float(input('Qual o menor valor de Ca_0 você deseja no mapa?   '))
    print()
    ca0maior = float(input('Qual o maior valor de Ca_0 você deseja no mapa?   '))
    print()
    passosca = int(input('Quantos passos você deseja entre esses valores?   '))
    print()

    T0menor = float(input('Qual o menor valor de T_0 você deseja no mapa?    '))
    print()
    T0maior = float(input('Qual o maior valor de T_0 você deseja no mapa?    '))
    print()
    passosT = int(input('Quantos passos você deseja entre esses valores?   '))
    print()

else:
    ca0menor = 0
    ca0maior = 3000
    passosca = 1000
   

    T0menor = 0.1
    T0maior = 4000
    passosT = 1000
ca0_vals = np.arange(ca0menor, ca0maior+1, (ca0maior-ca0menor)/passosca)    
T0_vals = np.arange(T0menor, T0maior+1, (T0maior-T0menor)/passosT)

ca_final = np.zeros((len(ca0_vals), len(T0_vals)))
T_final = np.zeros((len(ca0_vals), len(T0_vals)))

for i, ca0 in enumerate(ca0_vals):
     for j, T0 in enumerate(T0_vals):
         xi, yi = resolver(ca0, T0, caT_system, 0)
         ca_final[i, j] = xi
         T_final[i, j] = yi

fig, ax = plt.subplots()
# A matriz já tem T0 nas colunas (eixo X) e ca0 nas linhas (eixo Y)
im = ax.imshow(ca_final, aspect='auto', origin='lower', cmap='viridis',
               extent=[T0_vals.min(), T0_vals.max(), ca0_vals.min(), ca0_vals.max()]) 
ax.set_title('Mapa de concentração')
ax.set_xlabel('Temperatura inicial (T0)') 
ax.set_ylabel('Concentração inicial (ca0)') 
fig.colorbar(im, ax=ax)
plt.show()

fig2, ax2 = plt.subplots()
im2 = ax2.imshow(T_final, aspect='auto', origin='lower', cmap='plasma',
                 extent=[T0_vals.min(), T0_vals.max(), ca0_vals.min(), ca0_vals.max()])
ax2.set_title('Mapa de temperaturas')
ax2.set_ylabel('Concentração inicial (ca0)')
ax2.set_xlabel('Temperatura inicial (T0)')
fig2.colorbar(im2, ax=ax2)
plt.show()

end_time = time.time()
print(f"\nTempo de execução total: {end_time - start_time:.4f} segundos")
# %%

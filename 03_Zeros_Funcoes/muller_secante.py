# -*- coding: utf-8 -*-
# Programa 3: Implementação dos métodos de Müller e da Secante para encontrar raízes de um polinômio.
# Autor: Pedro Henrique da Silva Costa | Matrícula: 231012639
# =================================================================================
# │                                                                               │
# │                            1. BIBLIOTECAS E MÓDULOS                             │
# │                                                                               │
# =================================================================================
# Descrição: Importa as ferramentas necessárias para o funcionamento do script.
# ---------------------------------------------------------------------------------
import math         # Para funções matemáticas básicas (como 'nan').
import cmath        # Para matemática com números complexos (essencial para o sqrt de negativos).
import time         # Para controlar o tempo de input do usuário.
import glob         # Para encontrar arquivos no diretório (ler os resultados salvos).
import matplotlib.pyplot as plt # Para gerar os gráficos de convergência.
import os

# =================================================================================
# │                                                                               │
# │                  2. VARIÁVEIS GLOBAIS E ESTADO DO PROGRAMA                      │
# │                                                                               │
# =================================================================================
# Descrição: Define as variáveis que controlam o estado dos métodos.
#
# ---------------------------------------------------------------------------------
contmuller = 0      # Contador de iterações para o método de Müller.
contsecante = 0     # Contador de iterações para o método da Secante.
maxiter = 800       # Limite de iterações para evitar loops infinitos.

# Listas para armazenar o histórico de convergência de cada método.
muller_raiz_local, muller_raiz_final, muller_iter, muller_erro_rel = [], [], [], []
secante_raiz_local, secante_raiz_final, secante_iter, secante_erro_rel = [], [], [], []


# =================================================================================
# │                                                                               │
# │                         3. IMPLEMENTAÇÃO DOS MÉTODOS                          │
# │                                                                               │
# =================================================================================
# Descrição: Contém as funções que implementam os métodos de Müller e da Secante,
# bem como as funções "gerais" que buscam por múltiplas raízes.
# ---------------------------------------------------------------------------------

# ----------------------------------
# 3.1 Método de Müller
# ----------------------------------
def muller(Pontos_iniciais, funcao, tolerancia, verbose=False):
    """
    Função principal do método de Müller.
    Usa 3 pontos para criar uma parábola e estima a próxima raiz.
    É recursiva e depende de variáveis globais.
    """
    global contmuller, muller_raiz_local, muller_iter, muller_erro_rel, muller_raiz_final
    
    # Calcula os coeficientes da parábola que aproxima a função.
    h0 = Pontos_iniciais[1] - Pontos_iniciais[0]
    h1 = Pontos_iniciais[2] - Pontos_iniciais[1]
    if h0 == 0 or h1 == 0 or (h1 + h0) == 0: return [math.nan, [], [], []]
    delta0 = (funcao(Pontos_iniciais[1]) - funcao(Pontos_iniciais[0])) / h0
    delta1 = (funcao(Pontos_iniciais[2]) - funcao(Pontos_iniciais[1])) / h1
    a = (delta1 - delta0) / (h1 + h0)
    b = a*h1 + delta1
    c = funcao(Pontos_iniciais[2])

    # Calcula a próxima aproximação (xi) usando a fórmula quadrática.
    # Usa cmath.sqrt para lidar com discriminantes negativos (resto numérico).
    discriminante_complexo = cmath.sqrt(b**2 - 4*a*c)
    if b + discriminante_complexo == 0:
        return [math.nan, [], [], []]
    xi = (Pontos_iniciais[2] - (2*c)/(b + discriminante_complexo)).real # Pega só a parte real.

    # Calcula o erro e armazena o histórico da iteração.
    erro = funcao(xi)
    erro_relativo = abs(erro / xi) if xi != 0 else 0
    muller_raiz_local.append(xi)
    muller_erro_rel.append(erro_relativo)
    muller_iter.append(contmuller)

    # Printa a iteração atual se o modo 'verbose' estiver ativo.
    if verbose:
        print(f"  [Iteração {contmuller}]: xi = {xi:<23} | Erro (f(xi)) = {erro}")

    # Atualiza os pontos para a próxima chamada recursiva.
    Pontos_iniciais[0], Pontos_iniciais[1], Pontos_iniciais[2] = Pontos_iniciais[1], Pontos_iniciais[2], xi
    
    # Condições de parada.
    if abs(erro) < tolerancia:
        muller_raiz_final.append(xi)
        return [xi, muller_raiz_local, muller_iter, muller_erro_rel]
    elif contmuller >= maxiter:
        return [math.nan, [], [], []]
    else:
        contmuller += 1
        return muller(Pontos_iniciais, funcao, tolerancia, verbose=verbose)


def mullergeral(Pontos_iniciais, funcao, tolerancia, grau_pol, verbose_geral=False):
    """
    Função que usa Müller para encontrar múltiplas raízes através da deflação.
    A cada raiz encontrada, "divide" o polinômio por ela.
    Salva os resultados em arquivos .txt de forma tabular.
    """
    global contmuller, muller_raiz_local, muller_erro_rel, muller_iter
    funcao_atual = funcao
    for i in range(grau_pol):
        contmuller, muller_raiz_local, muller_erro_rel, muller_iter = 0, [], [], []
        raiz = muller(list(Pontos_iniciais), funcao_atual, tolerancia)
        # Output directory is hardcoded relative to repo root
        output_dir = "03_Zeros_Funcoes"
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        fname = os.path.join(output_dir, f'muller_resultados_{i+1}°_Raiz_encontrada.txt')
        with open(fname, 'w') as f:
            f.write(f'# Raiz final encontrada: {raiz[0]}\n')
            f.write('Iteracao,Raiz_Aproximada,Erro_Relativo\n')
            for j in range(len(raiz[2])):
                f.write(f"{raiz[2][j]},{raiz[1][j]},{raiz[3][j]}\n")
        if verbose_geral and not math.isnan(raiz[0]):
            print(f"Müller [Geral] - Raiz {i+1}: {raiz[0]:.7f} encontrada em {len(raiz[2])} iterações.")
        if not math.isnan(raiz[0]):
            r = raiz[0]
            funcao_atual = (lambda f, r_val: lambda x: f(x)/(x - r_val if x != r_val else 1e-12))(funcao_atual, r)

# ----------------------------------
# 3.2 Método da Secante
# ----------------------------------
def secante(Pontos_iniciais, funcao, tolerancia, verbose=False):
    """
    Função principal do método da Secante.
    Usa 2 pontos para criar uma reta (secante) e estima a próxima raiz.
    É recursiva e depende de variáveis globais.
    """
    global contsecante, secante_raiz_local, secante_iter, secante_erro_rel
    if funcao(Pontos_iniciais[1]) - funcao(Pontos_iniciais[0]) == 0:
        return [math.nan, [], [], []]
    xi = (Pontos_iniciais[1] - (funcao(Pontos_iniciais[1]) * (Pontos_iniciais[1] - Pontos_iniciais[0])) / (funcao(Pontos_iniciais[1]) - funcao(Pontos_iniciais[0]))).real
    erro = funcao(xi)
    erro_relativo = abs(erro / xi) if xi != 0 else 0
    secante_raiz_local.append(xi)
    secante_erro_rel.append(erro_relativo)
    secante_iter.append(contsecante)
    if verbose:
        print(f"  [Iteração {contsecante}]: xi = {xi:<23} | Erro (f(xi)) = {erro}")
    Pontos_iniciais[0], Pontos_iniciais[1] = Pontos_iniciais[1], xi
    if abs(erro) < tolerancia:
        return [xi, secante_raiz_local, secante_iter, secante_erro_rel]
    elif contsecante >= maxiter:
        return [math.nan, [], [], []]
    else:
        contsecante += 1
        return secante(Pontos_iniciais, funcao, tolerancia, verbose=verbose)


def secantegeral(Pontos_iniciais, funcao, tolerancia, grau_pol, verbose_geral=False):
    """
    Função que usa Secante para encontrar múltiplas raízes através da deflação.
    Salva os resultados em arquivos .txt de forma tabular.
    """
    global contsecante, secante_raiz_local, secante_iter, secante_erro_rel
    funcao_atual = funcao
    for i in range(grau_pol):
        contsecante, secante_raiz_local, secante_iter, secante_erro_rel = 0, [], [], []
        raiz = secante(list(Pontos_iniciais), funcao_atual, tolerancia)
        output_dir = "03_Zeros_Funcoes"
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        fname = os.path.join(output_dir, f'secante_resultados_{i+1}°_Raiz_encontrada.txt')
        with open(fname, 'w') as f:
            f.write(f'# Raiz final encontrada: {raiz[0]}\n')
            f.write('Iteracao,Raiz_Aproximada,Erro_Relativo\n')
            for j in range(len(raiz[2])):
                f.write(f"{raiz[2][j]},{raiz[1][j]},{raiz[3][j]}\n")
        if verbose_geral and not math.isnan(raiz[0]):
            print(f"Secante [Geral] - Raiz {i+1}: {raiz[0]:.7f} encontrada em {len(raiz[2])} iterações.")
        if not math.isnan(raiz[0]):
            r = raiz[0]
            funcao_atual = (lambda f, r_val: lambda x: f(x)/(x - r_val if x != r_val else 1e-12))(funcao_atual, r)

# ----------------------------------
# 3.3 Função a ser Analisada
# ----------------------------------
def f(x):
    """
    Define o polinômio cujas raízes queremos encontrar.
    As raízes exatas são: 1, 3, 5, 7, 9.
    """
    return (x-1)*(x-3)*(x-5)*(x-7)*(x-9)


# =================================================================================
# │                                                                               │
# │                          4. FUNÇÕES DE PLOTAGEM                               │
# │                                                                               │
# =================================================================================
# Descrição: Funções responsáveis por ler os dados (salvos ou em memória) e
# gerar os gráficos de convergência.
# ---------------------------------------------------------------------------------

def plotar_convergencia_primeira_raiz(resultados):
    """
    Gera o gráfico da Parte 1, mostrando a convergência para a primeira raiz
    a partir de diferentes chutes iniciais.
    """
    output_dir = "03_Zeros_Funcoes/images"
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))
    for res in resultados:
        if res['iter'] and not math.isnan(res['raiz']):
            estilo = {'marker': 'o', 'linestyle': '-'} if res['metodo'] == 'Müller' else {'marker': 'x', 'linestyle': '--'}
            ax.plot(res['iter'], res['erro'], **estilo, label=f"{res['metodo']} (Chute: {res['chute']}) -> Raiz: {res['raiz']:.4f}")
    ax.set_yscale('log')
    ax.set_xlabel('Número de Iteração')
    ax.set_ylabel('Erro Relativo (Escala Logarítmica)')
    ax.set_title('Convergência para a Primeira Raiz com Diferentes Chutes Iniciais')
    ax.legend(loc='best')
    ax.grid(True, which='both', linestyle=':')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grafico_convergencia_primeira_raiz.png'), dpi=300)
    print(f"\nGráfico da Parte 1 salvo como '{os.path.join(output_dir, 'grafico_convergencia_primeira_raiz.png')}'")
    # plt.show()


def plotar_comparacao_geral(ponto_inicial):
    """
    Gera o gráfico da Parte 2, lendo os arquivos .txt tabulares para mostrar
    a convergência para todas as raízes.
    """
    output_dir = "03_Zeros_Funcoes/images"
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 8))
    for metodo in ['muller', 'secante']:
        # Busca arquivos no diretório especificado
        search_dir = "03_Zeros_Funcoes"
        padrao = os.path.join(search_dir, f"{metodo}_resultados_*_Raiz_encontrada.txt")
        arquivos = sorted(glob.glob(padrao))
        for i, fname in enumerate(arquivos):
            try:
                with open(fname, 'r') as f:
                    header = f.readline()
                    raiz_valor = float(header.split(': ')[1])
                    f.readline() # Pula cabeçalho das colunas
                    iter_list, erro_list = [], []
                    for linha in f:
                        partes = linha.strip().split(',')
                        iter_list.append(int(partes[0]))
                        erro_list.append(float(partes[2]))
                    if iter_list and erro_list and not math.isnan(raiz_valor):
                        estilo = {'marker': 'o', 'linestyle': '-'} if metodo == 'muller' else {'marker': 'x', 'linestyle': '--'}
                        ax.plot(iter_list, erro_list, **estilo, label=f"{metodo.capitalize()} - Raiz {i+1} ({raiz_valor:.4f})")
            except Exception: pass
    ax.set_yscale('log')
    ax.set_title(f'Convergência Geral com Deflação (Chute Inicial Base: {ponto_inicial})')
    ax.set_xlabel('Número de Iteração')
    ax.set_ylabel('Erro Relativo (Log)')
    if ax.get_legend_handles_labels()[0]:
        ax.legend(loc='best')
    ax.grid(True, which='both', linestyle=':')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'grafico_convergencia_geral.png'), dpi=300)
    print(f"\nGráfico da Parte 2 salvo como '{os.path.join(output_dir, 'grafico_convergencia_geral.png')}'")
    # plt.show()


# =================================================================================
# │                                                                               │
# │                     5. EXECUÇÃO PRINCIPAL DO SCRIPT                           │
# │                                                                               │
# =================================================================================
# Descrição: Ponto de entrada do programa. Executa a demonstração em duas partes
# e, em seguida, inicia a seção interativa para o usuário.
# ---------------------------------------------------------------------------------
if __name__ == "__main__":
    
    # ---------------------------------------------------------------------
    # PARTE 1: DEMONSTRAÇÃO - ANÁLISE DETALHADA DA PRIMEIRA RAIZ
    # ---------------------------------------------------------------------
    print("="*80)
    print("PARTE 1: DEMONSTRAÇÃO - ANÁLISE DA PRIMEIRA RAIZ")
    print("="*80)
    chutes_iniciais = [0.5, 2.0, 4.1, 6.5, 8.4]
    tolerancia_demo = 1e-7
    resultados_primeira_raiz = []
    
    for chute in chutes_iniciais:
        print(f"\n--- Chute inicial base: {chute} ---")
        
        print("\n  --- Método de Müller ---")
        contmuller, muller_raiz_local, muller_iter, muller_erro_rel = 0, [], [], []
        resultado_muller = muller([chute, chute + 0.05, chute + 0.10], f, tolerancia_demo, verbose=True)
        if not math.isnan(resultado_muller[0]):
            resultados_primeira_raiz.append({'metodo': 'Müller', 'chute': chute, 'raiz': resultado_muller[0], 'iter': resultado_muller[2], 'erro': resultado_muller[3]})
        
        print("\n  --- Método da Secante ---")
        contsecante, secante_raiz_local, secante_iter, secante_erro_rel = 0, [], [], []
        resultado_secante = secante([chute, chute + 0.05], f, tolerancia_demo, verbose=True)
        if not math.isnan(resultado_secante[0]):
            resultados_primeira_raiz.append({'metodo': 'Secante', 'chute': chute, 'raiz': resultado_secante[0], 'iter': resultado_secante[2], 'erro': resultado_secante[3]})
    
    plotar_convergencia_primeira_raiz(resultados_primeira_raiz)

    # ---------------------------------------------------------------------
    # PARTE 2: DEMONSTRAÇÃO - BUSCA GERAL POR TODAS AS RAÍZES
    # ---------------------------------------------------------------------
    print("\n" + "="*80)
    print("PARTE 2: DEMONSTRAÇÃO - BUSCA GERAL POR TODAS AS RAÍZES")
    print("="*80)
    print("\n### ATENÇÃO: Os métodos numéricos são mais precisos para a primeira raiz. ###")
    print("A busca pelas raízes subsequentes usa deflação, uma técnica que pode")
    print("acumular erros e levar a resultados menos precisos.\n")
    ponto_inicial_geral = 0.5
    mullergeral([ponto_inicial_geral, ponto_inicial_geral + 0.05, ponto_inicial_geral + 0.10], f, tolerancia_demo, 5, verbose_geral=True)
    print("-" * 30)
    secantegeral([ponto_inicial_geral, ponto_inicial_geral + 0.05], f, tolerancia_demo, 5, verbose_geral=True)
    plotar_comparacao_geral(ponto_inicial_geral)
    
    # ---------------------------------------------------------------------
    # PARTE 3: SESSÃO INTERATIVA COM O USUÁRIO (DESABILITADA)
    # ---------------------------------------------------------------------
    print("\n" + "="*80)
    print("Sessão interativa desabilitada para automação.")
    print("="*80)

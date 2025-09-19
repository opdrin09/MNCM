# Tarefa 1: Movimento de Partícula com Arrasto

Este documento apresenta a análise e a solução numérica para o movimento de uma partícula sujeito a diferentes regimes de arrasto. O problema é resolvido utilizando o método de Runge-Kutta de 4ª Ordem implementado em Julia.

---

## O Método Numérico: Runge-Kutta de 4ª Ordem (RK4)

Para resolver as equações diferenciais ordinárias (EDOs) do problema, utilizaremos o método de Runge-Kutta de 4ª Ordem. A implementação genérica do solver, que recebe uma EDO qualquer na forma `f(t,v)`, pode ser encontrada no script da tarefa.

## Parte 1: Baixo Reynolds (Arrasto de Stokes) - Questões 1 e 2

Primeiro, resolvemos o problema para o caso de baixo número de Reynolds (`Re ≈ 0`), onde o arrasto é puramente viscoso. Conforme a **Questão 1**, a equação adimensionalizada governante é:

$$St \frac{dv^{\*}}{dt^{\*}} = -v^{\*} + 1$$

A solução analítica para essa equação é $v^{\*}(t^{\*}) = 1 - e^{-t^{\*}/St}$. O código resolve numericamente esta EDO para diferentes passos de tempo (`Δt`) e compara os resultados, mostrando como a precisão da solução melhora com o refinamento do passo, respondendo à **Questão 2**.

## Parte 2: Efeito Inercial (Arrasto Quadrático) - Questões 3 e 4

Agora, como pedido na **Questão 3**, introduzimos um termo de correção inercial (arrasto quadrático) na equação governante. A demonstração da adimensionalização segue abaixo.

A equação com dimensão é:
$$m_p \frac{dv_z}{dt} = -6\pi\eta a v_z - \frac{9}{4} \pi \rho_f a^2 v_z^2 + \frac{4}{3} \pi a^3 \Delta \rho g$$

Para adimensionalizar a equação, utilizamos as seguintes definições:

* **Velocidade Adimensional:** $v_{z}^{\*} = \frac{v_z}{v_s} \implies v_z = v_s v_{z}^{\*}$
* **Tempo Adimensional:** $t^{\*} = \frac{t v_s}{a} \implies t = \frac{t^{\*} a}{v_s}$
* **Relação das Derivadas (Regra da Cadeia):** $\frac{d}{dt} = \frac{dt^{\*}}{dt} \frac{d}{dt^{\*}} = \frac{v_s}{a} \frac{d}{dt^{\*}}$
* **Número de Stokes:** $St = \frac{m_p v_s}{6 \pi \eta a^2}$
* **Velocidade Terminal de Stokes:** $6\pi\eta a v_s = \frac{4}{3} \pi a^3 \Delta \rho g$
* **Número de Reynolds:** $Re = \frac{\rho_f a v_s}{\eta}$

Realizando as substituições e a normalização, chegamos na seguinte sequência de equações:
$$m_p \left( \frac{v_s}{a} \frac{d(v_s v_{z}^{\*})}{dt^{\*}} \right) = m_p \frac{v_s^2}{a} \frac{dv_{z}^{\*}}{dt^{\*}}$$
$$m_p \frac{v_s^2}{a} \frac{dv_{z}^{\*}}{dt^{\*}} = -6\pi\eta a (v_s v_{z}^{\*}) - \frac{9}{4} \pi \rho_f a^2 (v_s v_{z}^{\*})^2 + \frac{4}{3} \pi a^3 \Delta \rho g$$
$$\frac{m_p v_s^2 / a}{6\pi\eta a v_s} \frac{dv_{z}^{\*}}{dt^{\*}} = -\frac{6\pi\eta a v_s v_{z}^{\*}}{6\pi\eta a v_s} - \frac{\frac{9}{4} \pi \rho_f a^2 v_s^2 v_{z}^{\*2}}{6\pi\eta a v_s} + \frac{\frac{4}{3} \pi a^3 \Delta \rho g}{6\pi\eta a v_s}$$

Analisando termo a termo:
* **Termo da Esquerda:** $\left( \frac{m_p v_s}{6\pi\eta a^2} \right) \frac{dv_{z}^{\*}}{dt^{\*}} \implies St \frac{dv_{z}^{\*}}{dt^{\*}}$
* **Primeiro Termo da Direita:** $-v_{z}^{\*}$
* **Segundo Termo da Direita:** $-\left( \frac{3}{8} \right) \left( \frac{\rho_f a v_s}{\eta} \right) v_{z}^{\*2} \implies -\frac{3}{8} Re \, v_{z}^{\*2}$
* **Terceiro Termo da Direita:** O termo é igual a 1 pela definição da velocidade terminal de Stokes.

Juntando tudo, a equação adimensionalizada final se torna:
$$St \frac{dv_{z}^{\*}}{dt^{\*}} = -v_{z}^{\*} - \frac{3}{8} Re \, v_{z}^{\*2} + 1$$

O código resolve esta EDO para diferentes valores de `Re`, mostrando como a solução se desvia do caso `Re = 0`, respondendo à **Questão 4**.

## Parte 3: Comparação Adicional - Questão 5

A **Questão 5** pede a comparação da solução numérica com a solução exata para o caso com efeito inercial, obtida no artigo lido em aula. O código também implementa esta comparação.

---

### 📈 Resultados (Visualização Rápida)

As imagens a seguir são os resultados finais gerados pelo código. **Não é necessário executar o script para visualizá-los.**

**Figura 1: Comparação de Passos de Tempo (Arrasto de Stokes)**
<p align="center">
<img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/1f36f674-9902-4d77-ad2f-8ec6154dc809" />
</p>

**Figura 2: Efeito do Arrasto Quadrático (Variação de Reynolds)**

<p align="center"> <img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/b5966509-be79-4798-8fa6-dff305e69f93" /> </p>

**Figura 3 :Comparação da solução considerando a variação de Reynolds e a solução apresentada no artigo**

<p align="center"> <img width="600" height="400" alt="image" src="https://github.com/user-attachments/assets/0f757296-9a1b-4f17-9b64-9998aeee7578" /> </p>    

---
### 📢 Discussão dos resultados

#### Parte 1

Aqui nota-se que para valores de $\Delta t>1$  ainda é notável a diferença da solução numérica para com a solução analítica, abaixo de 1, as soluções tendem a ficar cada vez mais próximas, $\Delta t = 0.117$ as soluções numéricas e analíticas já são quase indistinguíveis na resolução da imagem, confirmando que a solução numérica tende a convergir quando o passo $\Delta t$ é menor.

#### Parte 2 

Na parte 2 faz-se a verificação do equacionamento por meio da comparação com a solução analítica quando $Re = 0$ que é 
conhecida e verifica-se que as soluções se sobrepõe, valindando-se o modelo. A partir disso pode-se visualizar como a velocidade adimensional muda a medidia que o número de Reynolds aumenta.

#### Parte 3

Aqui, faz-se a comparação da solução com método numérico, validado anteriormente, com a solução proposta no artigo mostrado na aula e nota-se que inicialmente a solução diverge, mas após um curto período de tempo, as soluções se igualam. É importante ressaltar que isso só ocorre para $Re$ baixo, para valores mais altos, as soluções já se igualam no começo, *Execute o código para melhor visualização*, o que sugere que nosso modelo físico não é completamente adequado para esses valores.




### ▶️ Como Executar o Código

Existem duas opções para executar a análise e regenerar os gráficos.

#### Opção A: Ambiente Local (Sem usar Git)

1.  Acesse a página principal do repositório no GitHub.
2.  Clique no botão verde **`< > Code`** e selecione **`Download ZIP`**.
3.  Extraia o arquivo `.zip` em sua máquina.
4.  Abra o terminal Julia, navegue até a pasta extraída `https://github.com/opdrin09/MNCM/tree/main/Tarefa_1`.
5.  Ative o ambiente do projeto e instale as dependências:
    ```julia
    # Dentro do REPL do Julia
    using Pkg
    Pkg.activate(".")
    Pkg.instantiate()
    ```
6.  Execute o script:
    ```julia
    # Ainda no REPL
    include("tarefa1.jl")
    ```

#### Opção B: Google Colab (Fácil, sem instalação)

Clique no botão abaixo para abrir um notebook no Google Colab. Este notebook irá configurar o ambiente Julia e executar o script `tarefa1.jl` diretamente do repositório. Basta executar as células em ordem
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opdrin09/MNCM/blob/main/Tarefa_1/executar_tarefa_1.ipynb)

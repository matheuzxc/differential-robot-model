# Título do Repositório

[Uma linha com uma descrição curta e direta do que é o projeto]

## Objetivo

Este projeto visa detalhar a dedução matemática das equações cinemáticas de um robô móvel com tração diferencial e, posteriormente, validar o modelo através de uma simulação computacional desenvolvida em Python.

## Índice

* [Pré-requisitos](#pré-requisitos)
* [Estrutura do Repositório](#estrutura-do-repositório)
* [Dedução do Modelo Cinemático](#dedução-do-modelo-cinemático)
* [Simulação em Python](#simulação-em-python)
* [Como Executar](#como-executar)
* [Autor](#autor)

## Pré-requisitos

[Liste aqui o que a pessoa precisa ter instalado na máquina para rodar o seu código]
* Python 3.x
* NumPy
* Matplotlib (caso tenha gerado gráficos da trajetória)

## Estrutura do Repositório

[Explique rapidamente o que tem em cada pasta, se houver]
* `src/`: Códigos da simulação.
* `img/`: Imagens utilizadas neste README.

## Dedução do Modelo Cinemático

### Visão Geral 
<p align="justify">
O esquema geral do robô diferencial pode ser visto na Figura 1, onde o ponto central $(x, y)$ define a posição do veículo no referencial global bidimensional, formado pelos eixos $\hat{x}$ e $\hat{y}$. A orientação atual do robô é representada pelo ângulo $\phi$ em relação à horizontal. O parâmetro $d$ indica a distância transversal do ponto central até cada uma das rodas de tração, determinando que a distância total entre as rodas (a bitola do robô) é igual a $2d$. É a partir dessa configuração geométrica que o modelo cinemático relaciona as velocidades angulares individuais da roda esquerda e da roda direita com as taxas de deslocamento linear e de rotação do sistema.
</p>

<div align="center">
  <em>Figura 1: Esquema de parâmetros do robô diferencial.</em>
  <br>
  <img src="./imagens/robot_esquema.svg" alt="Diagrama do robô diferencial">
  <br>
  <em>Fonte: Próprio autor.</em>
</div>

O vetor de estados que representa a cinemática do robô diferencial pode ser observado na [Equação 1](#eq1).

<a id="eq1"></a>
$$
\dot{q} = [\dot{x}, \dot{y}, \dot{\phi}]^T \tag{1}
$$

Onde:
- $\dot{x}:$ Velocidade linear instantânea do ponto de referência no eixo X global.
- $\dot{y}:$ Velocidade linear instantânea do ponto de referência no eixo Y global.
- $\dot{\phi}:$ Velocidade angular instantânea (taxa de guinada) do chassi do robô.

<p align="justify">
O comportamento desse vetor é definido pela função de cinemática direta $f(\omega_L, \omega_R)$. Essa função atua como um mapeamento matemático que recebe como entrada o giro dos motores nas juntas e entrega como resultado as velocidades do chassi no espaço operacional, onde:
</p>

- $\omega_L:$ Velocidade angular da roda esquerda.
- $\omega_R:$ Velocidade angular da roda direita.

### Dedução das Velocidades Locais

A modelagem cinemática tem início relacionando o giro independente dos motores com o movimento local do chassi do robô. 

Assumindo condição de rolamento sem deslizamento, as velocidades lineares individuais da roda esquerda ($v_L$) e da roda direita ($v_R$) são apresentadas, respectivamente, na [Equação 2](#eq2) e na [Equação 3](#eq3), dadas pela multiplicação de suas velocidades angulares pelo raio $r$ do pneu:

<a id="eq2"></a>
$$v_L = \omega_L \cdot r \tag{2}$$

<a id="eq3"></a>
$$v_R = \omega_R \cdot r \tag{3}$$

Como as rodas estão alinhadas em um eixo rígido de comprimento $2d$ (bitola), qualquer diferença de velocidade entre elas faz o robô orbitar em torno de um Centro Instantâneo de Rotação (ICR). A partir da geometria desse movimento orbital, ilustrada na Figura 2, calculam-se as velocidades resultantes no ponto médio do eixo do robô.

<div align="center">
  <em>Figura 2: Esquema de parâmetros do robô diferencial e o ICR.</em>
  <br>
  <img src="./imagens/robot_esquema_icr.svg" alt="Diagrama do ICR do robô diferencial">
  <br>
  <em>Fonte: Próprio autor.</em>
</div>

A velocidade linear resultante $v$, que translada o chassi, é expressa pela média aritmética das velocidades das rodas, conforme a [Equação 4](#eq4):

<a id="eq4"></a>
$$v = \frac{v_R + v_L}{2} = \frac{r(\omega_R + \omega_L)}{2} \tag{4}$$

A velocidade angular $\omega$, que rotaciona o chassi em torno do próprio eixo, é descrita na [Equação 5](#eq5), sendo gerada pela diferença de velocidade entre as rodas dividida pela distância $2d$:

<a id="eq5"></a>
$$\omega = \frac{v_R - v_L}{2d} = \frac{r(\omega_R - \omega_L)}{2d} \tag{5}$$

O comportamento cinemático resultante é apresentado na Figura 3.

<div align="center">
  <em>Figura 3: Esquema de movimento do robô diferencial.</em>
  <br>
  <img src="./imagens/robot_esquema_mov.svg" alt="Diagrama de movimento do robô diferencial">
  <br>
  <em>Fonte: Próprio autor.</em>
</div>

### Projeção no Referencial Global

As variáveis $v$ e $\omega$ descrevem o movimento apenas no referencial local do robô. A projeção desse movimento no referencial global $\{X, Y\}$ é realizada utilizando a orientação atual $\phi$. 

A decomposição trigonométrica da velocidade linear gera as taxas de variação nas coordenadas cartesianas, mostradas na [Equação 6](#eq6) e na [Equação 7](#eq7), enquanto a velocidade angular local corresponde à taxa de variação da orientação global indicada na [Equação 8](#eq8):


<a id="eq6"></a>
$$
\dot{x} = v \cdot \cos(\phi) \qquad (6)
$$

<a id="eq7"></a>
$$
\dot{y} = v \cdot \sin(\phi) \qquad (7)
$$

<a id="eq8"></a>
$$
\dot{\phi} = \omega \qquad (8)
$$

A substituição das expressões deduzidas de $v$ e $\omega$ nestas equações globais resulta no sistema linear que compõe a matriz Jacobiana, apresentada na [Equação 9](#eq9).

<a id="eq9"></a>
\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\phi} \end{bmatrix} = \begin{bmatrix} \frac{r}{2}\cos(\phi) & \frac{r}{2}\cos(\phi) \\ \frac{r}{2}\sin(\phi) & \frac{r}{2}\sin(\phi) \\ \frac{r}{2d} & -\frac{r}{2d} \end{bmatrix} \begin{bmatrix} \omega_R \\ \omega_L \end{bmatrix} \tag{9}

Onde:
- $r$: Raio das rodas motrizes.
- $d$: Distância do centro do eixo até cada roda (sendo $2d$ a bitola total do robô).
- $\omega_R$ e $\omega_L$: Velocidades angulares das rodas direita e esquerda, respectivamente.
## Simulação em Python

[Descreva como a matemática foi traduzida para o código. Fale rapidamente sobre a lógica de atualização dos estados x, y e phi ao longo do tempo (integração numérica)]

## Como Executar

[Coloque o passo a passo de comandos para o usuário rodar o seu script no terminal, tipo clonar o repo e rodar o python main.py]

## Autor

Matheus Nunes Franco (Sapo)
Engenharia Mecatrônica - UFSC Joinville
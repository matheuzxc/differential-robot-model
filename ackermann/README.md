# Modelo Cinemático de Robô Ackermann

Simulação cinemática e geração de trajetórias animadas para um robô móvel com direção tipo Ackermann (como carros), validando o modelo matemático através de animações desenvolvidas em Python.

## Objetivo

Este projeto visa detalhar a dedução matemática das equações cinemáticas de um robô móvel com direção Ackermann e, posteriormente, validar o modelo através de uma simulação computacional desenvolvida em Python.

## Dedução do Modelo Cinemático

### Visão Geral 
<p align="justify">
O modelo de direção Ackermann é amplamente utilizado em veículos de quatro rodas, como automóveis. O ponto de referência $(x, y)$ define a posição do centro do eixo traseiro do veículo no referencial global bidimensional. A orientação atual do robô é representada pelo ângulo $\theta$ em relação à horizontal. O parâmetro $L$ indica a distância entre o eixo traseiro e o eixo dianteiro (distância entre eixos ou wheelbase). O controle do veículo é feito ajustando a velocidade linear $v$ nas rodas traseiras e o ângulo de esterçamento $\psi$ das rodas dianteiras.
</p>


<div align="center">
  <em>Figura 2: Esquema de parâmetros do robô Ackermann e o ICR.</em>
  <br>
  <img src="./imagens/arckeman_esquema.svg" alt="Diagrama do ICR do robô Ackermann">
  <br>
  <em>Fonte: Adaptado de Lynch e Park (2017).</em>
</div>


O vetor de estados que representa a cinemática do robô Ackermann pode ser observado na [Equação 1](#eq1).

<a id="eq1"></a>

$$
\dot{q} = [\dot{x}, \dot{y}, \dot{\theta}]^T \qquad (1)
$$

Onde:
- $\dot{x}:$ Velocidade linear instantânea do ponto de referência no eixo X global.
- $\dot{y}:$ Velocidade linear instantânea do ponto de referência no eixo Y global.
- $\dot{\theta}:$ Velocidade angular instantânea (taxa de guinada) do chassi do robô.

<p align="justify">
O comportamento desse vetor é definido pelo mapeamento matemático que recebe como entrada a velocidade linear e o ângulo de esterçamento, onde:
</p>

- $v:$ Velocidade linear no centro do eixo traseiro.
- $\psi:$ Ângulo de esterçamento (direção) das rodas dianteiras.
- $L:$ Distância entre eixos (wheelbase).

### Dedução das Velocidades e Modelo de Bicicleta

A modelagem cinemática de um veículo com direção Ackermann de quatro rodas é frequentemente simplificada pelo **Modelo de Bicicleta (Bicycle Model)**. Neste modelo, assumimos que as duas rodas dianteiras e as duas rodas traseiras podem ser representadas por uma única roda virtual no centro de cada eixo, conectadas por um chassi rígido de comprimento $L$.

Assumindo a condição de rolamento puro (sem deslizamento lateral), a velocidade das rodas traseiras deve apontar estritamente na direção longitudinal do veículo. Como o ponto de referência $(x,y)$ está localizado no centro do eixo traseiro, o deslocamento no referencial global $\{X, Y\}$ é obtido decompondo a velocidade linear $v$ pela orientação $\theta$, gerando as taxas de variação nas coordenadas cartesianas expressas na [Equação 2](#eq2) e na [Equação 3](#eq3):

<a id="eq2"></a>

$$
\dot{x} = v \cdot \cos(\theta) \qquad (2)
$$

<a id="eq3"></a>

$$
\dot{y} = v \cdot \sin(\theta) \qquad (3)
$$

Para determinar a taxa de rotação do chassi ($\dot{\theta}$), precisamos analisar o Centro Instantâneo de Rotação (ICR). Durante uma curva, o veículo rotaciona em torno desse ponto (ICR). 
Geometricamente, o ICR é encontrado na interseção de duas retas perpendiculares aos vetores de velocidade das rodas:
1. Uma reta perpendicular à roda traseira (que se estende ao longo do eixo traseiro).
2. Uma reta perpendicular à roda dianteira, que está esterçada em um ângulo $\psi$.

Isso forma um triângulo retângulo cuja base é a distância entre eixos $L$ e o cateto adjacente ao ângulo $\psi$ (no ICR) é o raio de curvatura $R$, medido do centro do eixo traseiro até o ICR. Pela relação trigonométrica desse triângulo, temos:

$$
\tan(\psi) = \frac{L}{R} \implies R = \frac{L}{\tan(\psi)}
$$

A velocidade angular $\dot{\theta}$ do veículo é dada pela relação entre a velocidade linear $v$ e o raio de curvatura $R$ ($v = \dot{\theta} \cdot R$). Substituindo $R$, obtemos a [Equação 4](#eq4):

<a id="eq4"></a>

$$
\dot{\theta} = \frac{v}{R} = \frac{v \cdot \tan(\psi)}{L} \qquad (4)
$$

A substituição destas expressões resulta no sistema matricial não-linear (Jacobiana) que governa a cinemática do robô, apresentado na [Equação 5](#eq5).

<a id="eq5"></a>

$$
\begin{bmatrix} \dot{x} \\ \dot{y} \\ \dot{\theta} \end{bmatrix} = \begin{bmatrix} \cos(\theta) \\ \sin(\theta) \\ \frac{\tan(\psi)}{L} \end{bmatrix} v \qquad (5)
$$

Onde:
- $v$: Velocidade linear aplicada no centro do eixo traseiro (m/s).
- $\psi$: Ângulo de esterçamento da direção (rad).
- $L$: Distância entre eixos traseiro e dianteiro (m).

## Simulação em Python

A transição da modelagem matemática para o ambiente de simulação em Python foi realizada mapeando diretamente as equações da cinemática para uma estrutura de laço de repetição. Utilizando a biblioteca NumPy, as taxas de variação espaciais puderam ser calculadas a cada incremento de tempo através da matriz Jacobiana.

Como o modelo matemático descreve um sistema de tempo contínuo e o computador processa dados de forma discreta, a simulação utiliza o método de integração numérica de Euler de primeira ordem. Para isso, define-se um intervalo de amostragem constante, representado no código por $\Delta t$ (ou $dt$).

A cada passo iterativo, o algoritmo calcula as velocidades instantâneas no referencial global ($\dot{x}$, $\dot{y}$ e $\dot{\theta}$) utilizando a orientação $\theta$ do instante anterior. O estado atualizado do robô é então obtido somando o estado passado com o deslocamento calculado para aquele pequeno intervalo de tempo, resultando na seguinte lógica de atualização:

$$x[i]=x[i-1]+\dot{x}\cdot dt$$

$$y[i]=y[i-1]+\dot{y}\cdot dt$$

$$\theta[i]=\theta[i-1]+\dot{\theta}\cdot dt$$

Através dessa acumulação iterativa, a simulação consegue projetar a evolução temporal completa da postura do robô.

### Estrutura e Funcionamento do Código

Para garantir a máxima clareza pedagógica e alinhar a simulação com a teoria, a implementação no script **`ackerman_kinematics.py`** foi rigorosamente dividida em duas funções centrais. É fundamental compreender a diferença exata entre os **dados de entrada (Inputs)** e os **resultados calculados (Outputs)** em cada uma delas:

#### 1. Cinemática Inversa (`simular_ackermann_inversa(v, omega)`)
A cinemática inversa responde à pergunta: *"Se eu quero que o carro faça um determinado movimento e curva no espaço, quanto eu devo esterçar (virar) o volante?"* É utilizada para **controle e planejamento de trajetória**.
- **Entradas (Inputs):** O movimento espacial **desejado** para o chassi do carro. Consiste na velocidade linear ($v$) em metros por segundo, e na velocidade angular ($\omega$) em radianos por segundo.
- **Saídas (Outputs):** O comando mecânico necessário para atingir esse objetivo. O algoritmo calcula e retorna o **ângulo de esterçamento** ($\psi$) estritamente necessário para as rodas dianteiras.
- **Matemática Aplicada:** Primeiro, descobre-se o raio da curva $R = \frac{v}{\omega}$. Em seguida, calcula-se o esterçamento pela geometria do chassi: $\psi = \arctan\left(\frac{L}{R}\right)$.

#### 2. Cinemática Direta (`simular_ackermann(v, psi)`)
A cinemática direta responde à pergunta: *"Se eu acelerar a uma certa velocidade e virar o volante fisicamente nesse ângulo, qual será o caminho que o carro vai percorrer?"* É utilizada para **odometria e simulação**.
- **Entradas (Inputs):** A ação mecânica **real** no sistema de direção. Consiste unicamente na velocidade linear ($v$) e no ângulo físico de esterçamento das rodas dianteiras ($\psi$).
- **Saídas (Outputs):** O estado resultante no referencial global bidimensional. O algoritmo integra numericamente o movimento e devolve a postura contínua do veículo ao longo do tempo: Posição $x(t)$, Posição $y(t)$ e Orientação $\theta(t)$.

Ao final da simulação, o código utiliza funções auxiliares de rotação para desenhar iterativamente o veículo (chassi retangular e quatro rodas com esterçamento visível) percorrendo o caminho, gerando as figuras estáticas (SVG) e as animações (GIF) apresentadas neste repositório.

### Resultados da Simulação e Análise dos Painéis

Para refletir com exatidão a diferença entre a Cinemática Inversa e a Cinemática Direta, os resultados visuais gerados pelas simulações foram estruturados em dois painéis analíticos com comportamentos distintos:

- **Painel Esquerdo (Trajetória X-Y):** Em todos os testes, exibe o plano espacial bidimensional, plotando o caminho físico percorrido pelo veículo. A sobreposição da geometria do chassi auxilia na visualização imediata da orientação instantânea e do esterçamento das rodas dianteiras.
- **Painel Direito (Evolução Temporal Focada no Tipo de Cinemática):** 
  - Nos testes de **Cinemática Inversa** (Figuras 1 a 4), o foco da análise é a obtenção do ângulo do volante. Portanto, os gráficos plotam as **Entradas Alvo** ($v$ e $\omega$ constantes definidas pelo usuário) e a **Saída Calculada** (o ângulo de esterçamento $\psi$ resultante da matemática).
  - Nos testes de **Cinemática Direta** (Figuras 5 a 8), o foco da análise é a evolução no espaço. Portanto, os gráficos apresentam as variáveis de estado de postura resultantes da integração passo a passo: Posição $x$, Posição $y$ e Orientação $\theta$.

## Simulação da Cinemática Inversa (Comandos de Movimentação)

Para validar o comportamento cinemático a partir de comandos de movimentação, foram definidas velocidades-alvo para o chassi ($v$, $\omega$). A função de cinemática inversa calcula o ângulo de esterçamento $\psi$ necessário nas rodas dianteiras para atingir o movimento desejado. Em seguida, esse ângulo é aplicado na simulação da cinemática direta para gerar a trajetória resultante.

### Movimentação para Frente

Neste cenário, o comando de entrada é uma velocidade linear positiva ($v = 0.4$ m/s) com velocidade angular nula ($\omega = 0$). A cinemática inversa determina que o ângulo de esterçamento deve ser nulo ($\psi = 0$). O resultado é um deslocamento puramente translacional em linha reta.

<div align="center">
  <em>Figura 1: Animação do movimento para frente.</em>
  <br>
  <img src="./imagens/animacao_ackermann_Frente.gif" alt="Animação - Movimento para Frente">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Movimentação para Trás

De forma análoga, o comando de entrada é uma velocidade linear negativa ($v = -0.4$ m/s) com velocidade angular nula. A cinemática inversa retorna esterçamento nulo, resultando em um deslocamento retilíneo em marcha à ré.

<div align="center">
  <em>Figura 2: Animação do movimento para trás.</em>
  <br>
  <img src="./imagens/animacao_ackermann_Tras.gif" alt="Animação - Movimento para Trás">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Curva à Esquerda

Para realizar uma curva à esquerda, o comando de entrada combina velocidade linear ($v = 0.4$ m/s) com velocidade angular positiva ($\omega = 0.6$ rad/s). A cinemática inversa calcula o ângulo de esterçamento positivo correspondente, direcionando as rodas dianteiras para a esquerda.

<div align="center">
  <em>Figura 3: Animação da curva à esquerda.</em>
  <br>
  <img src="./imagens/animacao_ackermann_Curva_Esquerda.gif" alt="Animação - Curva à Esquerda">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Curva à Direita

O comando de entrada combina velocidade linear ($v = 0.4$ m/s) com velocidade angular negativa ($\omega = -0.6$ rad/s). A cinemática inversa calcula o ângulo de esterçamento negativo, direcionando as rodas dianteiras para a direita.

<div align="center">
  <em>Figura 4: Animação da curva à direita.</em>
  <br>
  <img src="./imagens/animacao_ackermann_Curva_Direita.gif" alt="Animação - Curva à Direita">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

## Simulação da Cinemática Direta via Integração Numérica

Nesta etapa, a velocidade linear $v$ e o ângulo de esterçamento $\psi$ são fornecidos diretamente como entrada, sem passar pela cinemática inversa. O algoritmo de integração de Euler calcula a postura contínua do veículo $(x(t), y(t), \theta(t))$ ao longo do tempo.

### Movimentação para Frente

O veículo recebe uma velocidade linear positiva ($v = 0.4$ m/s) com ângulo de esterçamento nulo ($\psi = 0$). A integração numérica produz um deslocamento retilíneo para frente, sem alteração na orientação.

<div align="center">
  <em>Figura 5: Animação do movimento para frente (Cinemática Direta).</em>
  <br>
  <img src="./imagens/animacao_ackermann_direta_Direta_Frente.gif" alt="Animação - Movimento para Frente (Direta)">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Movimentação para Trás

O veículo recebe uma velocidade linear negativa ($v = -0.4$ m/s) com ângulo de esterçamento nulo. A integração resulta em um deslocamento retilíneo em marcha à ré.

<div align="center">
  <em>Figura 6: Animação do movimento para trás (Cinemática Direta).</em>
  <br>
  <img src="./imagens/animacao_ackermann_direta_Direta_Tras.gif" alt="Animação - Movimento para Trás (Direta)">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Curva à Esquerda

O veículo recebe velocidade linear ($v = 0.4$ m/s) com ângulo de esterçamento positivo ($\psi = 0.3$ rad). A integração numérica produz uma trajetória curvilínea com rotação no sentido anti-horário.

<div align="center">
  <em>Figura 7: Animação da curva à esquerda (Cinemática Direta).</em>
  <br>
  <img src="./imagens/animacao_ackermann_direta_Direta_Curva_Esquerda.gif" alt="Animação - Curva à Esquerda (Direta)">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

### Curva à Direita

O veículo recebe velocidade linear ($v = 0.4$ m/s) com ângulo de esterçamento negativo ($\psi = -0.3$ rad). A integração numérica produz uma trajetória curvilínea com rotação no sentido horário.

<div align="center">
  <em>Figura 8: Animação da curva à direita (Cinemática Direta).</em>
  <br>
  <img src="./imagens/animacao_ackermann_direta_Direta_Curva_Direita.gif" alt="Animação - Curva à Direita (Direta)">
  <br>
  <em>Fonte: Elaborado pelo autor.</em>
</div>

## Como Executar

1. Clone este repositório para a sua máquina local:
   ```bash
   git clone https://github.com/matheuzxc/Ackermann_robot_model.git
   ```
2. Acesse o diretório do projeto:
   ```bash
   cd Ackermann_robot_model
   ```
3. (Opcional) Ative o ambiente virtual já incluso (ou crie um novo):
   ```bash
   # No Windows:
   .\venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install numpy matplotlib seaborn pillow
   ```
5. Execute a simulação:
   ```bash
   python ackerman_kinematics.py
   ```
6. Aguarde a finalização do script. Os arquivos `.gif` e `.svg` referentes aos movimentos executados serão salvos no diretório raiz.

## Autor

Matheus Nunes Franco - 
Engenharia Mecatrônica - UFSC Joinville

## Referências

Para mais detalhes teóricos sobre esses mecanismos de tração e a modelagem apresentada, consulte:
* LYNCH, Kevin M.; PARK, Frank C. **Modern Robotics - Mechanics, Planning, and Control**. Capítulo 13. Cambridge University Press. Uma playlist em vídeo com as aulas correspondentes a este capítulo também é disponibilizada online pelos autores.
* MathWorks. **Mobile Robot Kinematics Equations**. Disponível em: https://www.mathworks.com/help/robotics/ug/mobile-robot-kinematics-equations.html
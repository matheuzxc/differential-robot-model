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


<p align="justify">
O esquema geral do robô diferencial pode ser visto na Figura 1, onde o ponto central $(x, y)$ define a posição do veículo no referencial global bidimensional, formado pelos eixos $\hat{x}$ e $\hat{y}$. A orientação atual do robô é representada pelo ângulo $\phi$ em relação à horizontal. O parâmetro $d$ indica a distância transversal do ponto central até cada uma das rodas de tração, determinando que a distância total entre as rodas (a bitola do robô) é igual a $2d$. É a partir dessa configuração geométrica espacial que o modelo cinemático relaciona as velocidades angulares individuais da roda esquerda e da roda direita com as taxas de deslocamento linear e de rotação do sistema.
</p>

<div align="center">
  <em>Figura 1: Esquema de parâmetros do robô diferencial.</em>
  <br>
  <img src="./imagens/robot_esquema.svg" alt="Diagrama do robô diferencial">
  <br>
  <em>Fonte: Próprio autor.</em>
</div>


## Simulação em Python

[Descreva como a matemática foi traduzida para o código. Fale rapidamente sobre a lógica de atualização dos estados x, y e phi ao longo do tempo (integração numérica)]

## Como Executar

[Coloque o passo a passo de comandos para o usuário rodar o seu script no terminal, tipo clonar o repo e rodar o python main.py]

## Autor

Matheus Nunes Franco (Sapo)
Engenharia Mecatrônica - UFSC Joinville
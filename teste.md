# Roteiro de Apresentação: Modelos Cinemáticos de Robôs Móveis (5 Minutos)

**Tempo total estimado:** 5 minutos  
**Objetivo:** Apresentar a dedução teórica e a simulação computacional comparando os modelos de Robô Diferencial e Ackermann.

---

### 1. Introdução (0:00 - 0:45) - *A Base da Robótica Móvel*
- **Abertura:** "Olá a todos. Hoje vou apresentar o desenvolvimento e a modelagem cinemática de dois dos mecanismos de locomoção mais clássicos da robótica: a Tração Diferencial e a Direção de Ackermann."
- **Contexto:** "O objetivo desse projeto não foi apenas demonstrar a teoria, mas validar a matemática de restrições não-holonômicas transformando as equações diferenciais em simulações visuais em Python."
- **Por que dois modelos?** "Eles resolvem o mesmo problema — mover-se pelo plano bidimensional — mas com mecânicas totalmente diferentes."

### 2. O Robô de Tração Diferencial (0:45 - 2:15) - *Simplicidade e Agilidade*
- **O Conceito:** "Começando pelo Robô Diferencial. O modelo é simples e super ágil: duas rodas motrizes independentes no mesmo eixo."
- **A Cinemática:** "Todo o movimento do robô depende de uma única coisa: a diferença de velocidade entre as rodas. Se ambas giram igual, o robô translada reto. Se giram em sentidos opostos, ele rotaciona no próprio eixo em uma rotação pura (giro de tanque)."
- **A Matemática:** "Aplicando as restrições de que as rodas rolam sem deslizar, deduzimos que a velocidade linear do robô é a média das rodas, e a rotação é gerada pela diferença entre elas dividida pela bitola. Construímos a matriz Jacobiana que mapeia o giro dos motores para as velocidades globais (X, Y e Ângulo)."

### 3. O Robô Ackermann (2:15 - 3:45) - *A Mecânica Automotiva*
- **O Conceito:** "Em seguida, temos o modelo de Ackermann, que é o padrão utilizado em carros de passeio. Ao contrário do diferencial, ele não consegue girar no próprio eixo."
- **Modelo de Bicicleta:** "Para simplificar o equacionamento das quatro rodas, usamos o 'Modelo de Bicicleta'. Assumimos um eixo traseiro que acelera, e um eixo dianteiro que esterça — o volante."
- **Os Dois Ângulos ($\theta$ e $\psi$):** "Um ponto de atenção crucial no projeto foi separar os referenciais: o esterçamento do volante ($\psi$) é a nossa entrada mecânica de controle nas rodas. Já a orientação inteira do chassi ($\theta$) é o estado global do carro. Mudar o volante ($\psi$) não rotaciona o carro automaticamente, apenas cria um raio de curvatura. O carro precisa de aceleração nesse raio para começar a virar o $\theta$."
- **A Matemática:** "O Centro Instantâneo de Rotação é puramente geométrico: depende da distância entre eixos (o 'wheelbase') e da tangente do volante ($\psi$). Isso gera a nossa matriz Jacobiana, onde a velocidade angular do chassi é calculada a partir dessa relação."

### 4. Simulação em Python: Inversa e Direta (3:45 - 4:45) - *Da Teoria à Prática*
- **O Código:** "Para dar vida a essas equações, desenvolvemos algoritmos em Python utilizando a integração numérica de Euler para acumular a posição iterativamente no tempo."
- **Cinemática Inversa vs Direta:** "A simulação foi estruturada em duas vias:
  1. **Cinemática Inversa (Controle):** Nós dizemos 'Quero que o robô ande e faça essa curva' e o código nos devolve quanto o volante deve virar (Ackermann) ou a velocidade exata de cada roda independente (Diferencial).
  2. **Cinemática Direta (Odometria):** Fornecemos a potência pura dos motores para a matemática, e o robô desenha seu caminho no espaço."

### 5. Conclusão (4:45 - 5:00) - *Fechamento*
- **Resultados Visuais:** "O resultado disso tudo são geradores autônomos de visualização. Os scripts traçam gráficos de evolução temporal e animam perfeitamente a trajetória do chassi no espaço 2D."
- **Despedida:** "Todo o projeto, do código aos SVGs e GIFs, está dividido, modularizado e documentado de forma didática no repositório. Muito obrigado."

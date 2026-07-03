import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

sns.set_theme(
    style="whitegrid",
    rc={
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "font.size": 12,
        "axes.titlesize": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 11
    }
)

def maquina_estados_comandos(t):
    """
    Define os comandos wL e wR baseados no tempo da simulação.
    """
    if t < 2.0:
        # 1. Frente 0.30m
        return 3.0, 3.0
    elif t < 4.0:
        # 2. Dobra a direita (90 graus)
        return np.pi/2, -np.pi/2
    elif t < 6.0:
        # 3. Frente 0.30m
        return 3.0, 3.0
    elif t < 8.0:
        # 4. Dobra a esquerda (90 graus)
        return -np.pi/2, np.pi/2
    elif t < 10.0:
        # 5. Tras 0.30m
        return -3.0, -3.0
    elif t < 12.0:
        # 6. Frente 0.30m
        return 3.0, 3.0
    else:
        # 7. Para
        return 0.0, 0.0

def simular_trajetoria_complexa(r=0.05, d=0.1, dt=0.05, tf=13.0):
    passos = int(tf / dt)
    t = np.linspace(0, tf, passos)
    
    x = np.zeros(passos)
    y = np.zeros(passos)
    phi = np.zeros(passos)
    
    for i in range(1, passos):
        wL, wR = maquina_estados_comandos(t[i-1])
        
        v = (r / 2) * (wR + wL)
        w = (r / (2 * d)) * (wR - wL)
        
        x_dot = v * np.cos(phi[i-1])
        y_dot = v * np.sin(phi[i-1])
        phi_dot = w
        
        x[i] = x[i-1] + x_dot * dt
        y[i] = y[i-1] + y_dot * dt
        phi[i] = phi[i-1] + phi_dot * dt
        
    return t, x, y, phi

# Executando a simulacao
tf_simulacao = 13.0
dt_simulacao = 0.05
t, x, y, phi = simular_trajetoria_complexa(tf=tf_simulacao, dt=dt_simulacao)

# Configurando a figura
fig = plt.figure(figsize=(10, 5))
gs = fig.add_gridspec(3, 2, width_ratios=[1.2, 1])

ax_traj = fig.add_subplot(gs[:, 0])
ax_traj.set_xlim(-0.2, 0.5)
ax_traj.set_ylim(-0.5, 0.2)
ax_traj.set_aspect('equal')
ax_traj.set_title('Trajetória Sequencial (X, Y)')
ax_traj.set_xlabel('Posição X (m)')
ax_traj.set_ylabel('Posição Y (m)')
linha_traj, = ax_traj.plot([], [], color='black', linewidth=2, label='Caminho do Robô')
ax_traj.legend(loc='upper right')

ax_x = fig.add_subplot(gs[0, 1])
ax_x.set_xlim(0, tf_simulacao)
ax_x.set_ylim(-0.1, 0.4)
ax_x.set_title('Evolução das Variáveis')
ax_x.set_ylabel('x (m)')
linha_x, = ax_x.plot([], [], color='blue', linewidth=2)

ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
ax_y.set_ylim(-0.4, 0.1)
ax_y.set_ylabel('y (m)')
linha_y, = ax_y.plot([], [], color='red', linewidth=2)

ax_phi = fig.add_subplot(gs[2, 1], sharex=ax_x)
ax_phi.set_ylim(-2, 1)
ax_phi.set_ylabel(r'$\phi$ (rad)')
ax_phi.set_xlabel('Tempo (s)')
linha_phi, = ax_phi.plot([], [], color='green', linewidth=2)

fig.tight_layout()

# Salvando a imagem estatica final antes de animar
linha_traj.set_data(x, y)
linha_x.set_data(t, x)
linha_y.set_data(t, y)
linha_phi.set_data(t, phi)
plt.savefig('trajetoria_sequencial_final.png', dpi=300, bbox_inches='tight')
print("Imagem estática gerada com sucesso.")

# Limpando os dados das linhas para comecar a animacao
linha_traj.set_data([], [])
linha_x.set_data([], [])
linha_y.set_data([], [])
linha_phi.set_data([], [])

def atualizar(frame):
    linha_traj.set_data(x[:frame], y[:frame])
    linha_x.set_data(t[:frame], x[:frame])
    linha_y.set_data(t[:frame], y[:frame])
    linha_phi.set_data(t[:frame], phi[:frame])
    return linha_traj, linha_x, linha_y, linha_phi

passos_totais = int(tf_simulacao / dt_simulacao)
anim = FuncAnimation(fig, atualizar, frames=passos_totais, interval=50, blit=True)

print("Renderizando o GIF da sequencia completa...")
anim.save('trajetoria_sequencial.gif', writer='pillow', fps=20)
print("Pronto! GIF salvo no diretorio.")
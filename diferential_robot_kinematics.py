import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import os

# Configuracao global do Seaborn
sns.set_theme(
    style="whitegrid",
    rc={
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "font.size": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 11
    }
)

def simular_cinematica(wL, wR, r=0.05, d=0.1, dt=0.05, tf=5.0):
    passos = int(tf / dt)
    t = np.linspace(0, tf, passos)
    
    x = np.zeros(passos)
    y = np.zeros(passos)
    phi = np.zeros(passos)
    
    for i in range(1, passos):
        v = (r / 2) * (wR + wL)
        w = (r / (2 * d)) * (wR - wL)
        
        x_dot = v * np.cos(phi[i-1])
        y_dot = v * np.sin(phi[i-1])
        phi_dot = w
        
        x[i] = x[i-1] + x_dot * dt
        y[i] = y[i-1] + y_dot * dt
        phi[i] = phi[i-1] + phi_dot * dt
        
    return t, x, y, phi

raio_roda = 0.05
dist_roda = 0.1 
tf_simulacao = 5.0
dt_simulacao = 0.05

cenarios = {
    "Frente": [5.0, 5.0],
    "Tras": [-5.0, -5.0],
    "Curva_Esquerda": [2.0, 5.0],
    "Curva_Direita": [5.0, 2.0]
}

# Funcao de atualizacao isolada para evitar vazamento de memoria no loop
def atualizar(frame, t, x, y, phi, l_traj, l_x, l_y, l_phi):
    l_traj.set_data(x[:frame], y[:frame])
    l_x.set_data(t[:frame], x[:frame])
    l_y.set_data(t[:frame], y[:frame])
    l_phi.set_data(t[:frame], phi[:frame])
    return l_traj, l_x, l_y, l_phi

passos_totais = int(tf_simulacao / dt_simulacao)

print("Iniciando a renderização dos SVGs e GIFs. Isso pode levar um minutinho...")
os.makedirs('imagens', exist_ok=True)

for nome, (wL, wR) in cenarios.items():
    print(f"Renderizando cenário: {nome}...")
    
    t, x, y, phi = simular_cinematica(wL, wR, r=raio_roda, d=dist_roda, dt=dt_simulacao, tf=tf_simulacao)
    
    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.2, 1])
    
    # Trajetoria
    ax_traj = fig.add_subplot(gs[:, 0])
    ax_traj.set_xlim(-1.5, 1.5)
    ax_traj.set_ylim(-1.5, 1.5)
    ax_traj.set_aspect('equal')
    ax_traj.set_xlabel('Posição X (m)')
    ax_traj.set_ylabel('Posição Y (m)')
    linha_traj, = ax_traj.plot([], [], color='black', linewidth=2, label=f'$\\omega_L$={wL}, $\\omega_R$={wR}')
    ax_traj.legend(loc='upper right')
    
    # Estado X
    ax_x = fig.add_subplot(gs[0, 1])
    ax_x.set_xlim(0, tf_simulacao)
    ax_x.set_ylim(-1.5, 1.5)
    ax_x.set_ylabel('x (m)')
    linha_x, = ax_x.plot([], [], color='blue', linewidth=2)
    
    # Estado Y
    ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
    ax_y.set_ylim(-1.5, 1.5)
    ax_y.set_ylabel('y (m)')
    linha_y, = ax_y.plot([], [], color='red', linewidth=2)
    
    # Estado Phi
    ax_phi = fig.add_subplot(gs[2, 1], sharex=ax_x)
    ax_phi.set_ylim(-4, 4)
    ax_phi.set_ylabel('$\\phi$ (rad)')
    ax_phi.set_xlabel('Tempo (s)')
    linha_phi, = ax_phi.plot([], [], color='green', linewidth=2)
    
    fig.tight_layout()
    
    # --- Passo 1: Salvar a versao estatica em SVG (Grafico completo) ---
    linha_traj.set_data(x, y)
    linha_x.set_data(t, x)
    linha_y.set_data(t, y)
    linha_phi.set_data(t, phi)
    
    nome_svg = os.path.join('imagens', f'estatico_{nome}.svg')
    fig.savefig(nome_svg, format='svg', bbox_inches='tight')
    
    # --- Passo 2: Limpar os dados nas linhas para o GIF animado comecar do zero ---
    linha_traj.set_data([], [])
    linha_x.set_data([], [])
    linha_y.set_data([], [])
    linha_phi.set_data([], [])
    
    # --- Passo 3: Criar e salvar a animacao ---
    anim = FuncAnimation(
        fig, 
        atualizar, 
        frames=passos_totais, 
        fargs=(t, x, y, phi, linha_traj, linha_x, linha_y, linha_phi), 
        interval=50, 
        blit=True
    )
    
    nome_gif = os.path.join('imagens', f'animacao_{nome}.gif')
    anim.save(nome_gif, writer='pillow', fps=20)
    
    # Fechando a figura para liberar memoria para a proxima iteracao
    plt.close(fig)

print("Processo finalizado! SVGs e GIFs salvos na pasta 'imagens/'.")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.transforms as transforms
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

def simular_cinematica_inversa(v, w, r=0.05, d=0.1):
    """
    Cinematica Inversa: 
    Recebe a velocidade linear (v) e angular (w) desejadas para o chassi
    e retorna as velocidades angulares necessarias nas rodas (wL, wR).
    """
    wR = (v + d * w) / r
    wL = (v - d * w) / r
    return wL, wR

raio_roda = 0.05
dist_roda = 0.1 
tf_simulacao = 5.0
dt_simulacao = 0.05

# Cenarios de teste definidos pelas velocidades ALVO do chassi (v, w)
# para testar a Cinematica Inversa
cenarios = {
    "Frente": [0.25, 0.0],
    "Tras": [-0.25, 0.0],
    "Curva_Esquerda": [0.175, 0.75],
    "Curva_Direita": [0.175, -0.75]
}

def atualizar(frame, t, x, y, phi, l_traj, l_x, l_y, l_phi, chassis, wheel_L, wheel_R, caster, center, ax_traj):
    l_traj.set_data(x[:frame], y[:frame])
    l_x.set_data(t[:frame], x[:frame])
    l_y.set_data(t[:frame], y[:frame])
    l_phi.set_data(t[:frame], phi[:frame])
    
    tr = transforms.Affine2D().rotate(phi[frame]).translate(x[frame], y[frame]) + ax_traj.transData
    chassis.set_transform(tr)
    wheel_L.set_transform(tr)
    wheel_R.set_transform(tr)
    caster.set_transform(tr)
    center.set_transform(tr)
    
    return l_traj, l_x, l_y, l_phi, chassis, wheel_L, wheel_R, caster, center

def atualizar_inversa(frame, t, x, y, phi, v_val, w_val, wL_val, wR_val, l_traj, l_x, l_y, l_phi, l_wR, chassis, wheel_L, wheel_R, caster, center, ax_traj):
    l_traj.set_data(x[:frame], y[:frame])
    
    # Arrays preenchidos com o valor constante ate o frame atual
    l_x.set_data(t[:frame], np.full(frame, v_val))
    l_y.set_data(t[:frame], np.full(frame, w_val))
    l_phi.set_data(t[:frame], np.full(frame, wL_val))
    l_wR.set_data(t[:frame], np.full(frame, wR_val))
    
    tr = transforms.Affine2D().rotate(phi[frame]).translate(x[frame], y[frame]) + ax_traj.transData
    chassis.set_transform(tr)
    wheel_L.set_transform(tr)
    wheel_R.set_transform(tr)
    caster.set_transform(tr)
    center.set_transform(tr)
    
    return l_traj, l_x, l_y, l_phi, l_wR, chassis, wheel_L, wheel_R, caster, center

passos_totais = int(tf_simulacao / dt_simulacao)

print("Iniciando a renderização dos SVGs e GIFs. Isso pode levar um minutinho...")
os.makedirs('imagens', exist_ok=True)

for nome, (v_alvo, w_alvo) in cenarios.items():
    print(f"Renderizando cenário: {nome}...")
    
    # --- Passo 1: CINEMATICA INVERSA ---
    # Descobre quais velocidades de roda sao necessarias para atingir o (v, w) desejado
    wL, wR = simular_cinematica_inversa(v_alvo, w_alvo, r=raio_roda, d=dist_roda)
    
    # --- Passo 2: CINEMATICA DIRETA ---
    # Simula o movimento aplicando essas velocidades nas rodas
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
    
    # Estado X -> Velocidade v
    ax_x = fig.add_subplot(gs[0, 1])
    ax_x.set_xlim(0, tf_simulacao)
    ax_x.set_ylim(-0.5, 0.5)
    ax_x.set_ylabel('v (m/s)')
    linha_x, = ax_x.plot([], [], color='blue', linewidth=2, label=f'v = {v_alvo:.2f} m/s')
    ax_x.legend(loc='upper right')
    
    # Estado Y -> Velocidade angular w
    ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
    ax_y.set_ylim(-1.5, 1.5)
    ax_y.set_ylabel('$\\omega$ (rad/s)')
    linha_y, = ax_y.plot([], [], color='red', linewidth=2, label=f'$\\omega$ = {w_alvo:.2f} rad/s')
    ax_y.legend(loc='upper right')
    
    # Estado Phi -> Velocidades Calculadas wL e wR
    ax_phi = fig.add_subplot(gs[2, 1], sharex=ax_x)
    ax_phi.set_ylim(-15, 15)
    ax_phi.set_ylabel('Rodas (rad/s)')
    ax_phi.set_xlabel('Tempo (s)')
    linha_phi, = ax_phi.plot([], [], color='green', linewidth=2, label=f'$\\omega_L$ = {wL:.2f} rad/s')
    linha_wR, = ax_phi.plot([], [], color='orange', linewidth=2, label=f'$\\omega_R$ = {wR:.2f} rad/s')
    ax_phi.legend(loc='upper right')
    
    # Adicionando o robô como patches (formas) no gráfico
    chassis = patches.Polygon([[-0.1, 0.15], [0.1, 0.15], [0.2, 0], [0.1, -0.15], [-0.1, -0.15]], 
                              closed=True, edgecolor='black', facecolor='white', linewidth=2, zorder=3)
    wheel_L = patches.Rectangle((-0.05, 0.08), 0.1, 0.04, edgecolor='black', facecolor='tab:blue', zorder=4)
    wheel_R = patches.Rectangle((-0.05, -0.12), 0.1, 0.04, edgecolor='black', facecolor='tab:blue', zorder=4)
    caster = patches.Circle((0.15, 0), 0.025, edgecolor='black', facecolor='tab:blue', zorder=4)
    center = patches.Circle((0, 0), 0.02, edgecolor='black', facecolor='black', zorder=5)

    ax_traj.add_patch(chassis)
    ax_traj.add_patch(wheel_L)
    ax_traj.add_patch(wheel_R)
    ax_traj.add_patch(caster)
    ax_traj.add_patch(center)
    
    fig.tight_layout()
    
    # --- Passo 1: Salvar a versao estatica em SVG (Grafico completo) ---
    linha_traj.set_data(x, y)
    linha_x.set_data(t, np.full(len(t), v_alvo))
    linha_y.set_data(t, np.full(len(t), w_alvo))
    linha_phi.set_data(t, np.full(len(t), wL))
    linha_wR.set_data(t, np.full(len(t), wR))
    
    # Atualiza posicao do robo para o ultimo frame
    tr_final = transforms.Affine2D().rotate(phi[-1]).translate(x[-1], y[-1]) + ax_traj.transData
    chassis.set_transform(tr_final)
    wheel_L.set_transform(tr_final)
    wheel_R.set_transform(tr_final)
    caster.set_transform(tr_final)
    center.set_transform(tr_final)
    
    nome_svg = os.path.join('imagens', f'estatico_{nome}.svg')
    fig.savefig(nome_svg, format='svg', bbox_inches='tight')
    
    # --- Passo 2: Limpar os dados nas linhas para o GIF animado comecar do zero ---
    linha_traj.set_data([], [])
    linha_x.set_data([], [])
    linha_y.set_data([], [])
    linha_phi.set_data([], [])
    linha_wR.set_data([], [])
    
    # --- Passo 3: Criar e salvar a animacao ---
    anim = FuncAnimation(
        fig, 
        atualizar_inversa, 
        frames=passos_totais, 
        fargs=(t, x, y, phi, v_alvo, w_alvo, wL, wR, linha_traj, linha_x, linha_y, linha_phi, linha_wR, chassis, wheel_L, wheel_R, caster, center, ax_traj), 
        interval=50, 
        blit=True
    )
    
    nome_gif = os.path.join('imagens', f'animacao_{nome}.gif')
    anim.save(nome_gif, writer='pillow', fps=20)
    
    # Fechando a figura para liberar memoria para a proxima iteracao
    plt.close(fig)

print("Processo finalizado! SVGs e GIFs da Cinematica Inversa salvos na pasta 'imagens/'.")

# ============================================================================
# CINEMATICA DIRETA: cenarios com velocidades de roda (wL, wR) especificadas diretamente
# O algoritmo recebe as velocidades de entrada e integra a postura via Euler.
# ============================================================================

cenarios_direta = {
    "Direta_Frente": [5.0, 5.0],
    "Direta_Tras": [-5.0, -5.0],
    "Direta_Curva_Esquerda": [2.0, 5.0],
    "Direta_Curva_Direita": [5.0, 2.0]
}

print("\nIniciando a renderização dos cenários de Cinemática Direta...")

for nome, (wL, wR) in cenarios_direta.items():
    print(f"Renderizando cenário (Direta): {nome}...")
    
    # Cinematica Direta: integra diretamente a partir das velocidades das rodas
    t, x, y, phi = simular_cinematica(wL, wR, r=raio_roda, d=dist_roda, dt=dt_simulacao, tf=tf_simulacao)
    
    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.2, 1])
    
    ax_traj = fig.add_subplot(gs[:, 0])
    ax_traj.set_xlim(-1.5, 1.5)
    ax_traj.set_ylim(-1.5, 1.5)
    ax_traj.set_aspect('equal')
    ax_traj.set_xlabel('Posição X (m)')
    ax_traj.set_ylabel('Posição Y (m)')
    linha_traj, = ax_traj.plot([], [], color='black', linewidth=2, label=f'$\\omega_L$={wL}, $\\omega_R$={wR}')
    ax_traj.legend(loc='upper right')
    
    ax_x = fig.add_subplot(gs[0, 1])
    ax_x.set_xlim(0, tf_simulacao)
    ax_x.set_ylim(-1.5, 1.5)
    ax_x.set_ylabel('x (m)')
    linha_x, = ax_x.plot([], [], color='blue', linewidth=2)
    
    ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
    ax_y.set_ylim(-1.5, 1.5)
    ax_y.set_ylabel('y (m)')
    linha_y, = ax_y.plot([], [], color='red', linewidth=2)
    
    ax_phi = fig.add_subplot(gs[2, 1], sharex=ax_x)
    ax_phi.set_ylim(-30, 30)
    ax_phi.set_ylabel('$\\phi$ (rad)')
    ax_phi.set_xlabel('Tempo (s)')
    linha_phi, = ax_phi.plot([], [], color='green', linewidth=2)
    
    chassis_d = patches.Polygon([[-0.1, 0.15], [0.1, 0.15], [0.2, 0], [0.1, -0.15], [-0.1, -0.15]], 
                              closed=True, edgecolor='black', facecolor='white', linewidth=2, zorder=3)
    wheel_L_d = patches.Rectangle((-0.05, 0.08), 0.1, 0.04, edgecolor='black', facecolor='tab:blue', zorder=4)
    wheel_R_d = patches.Rectangle((-0.05, -0.12), 0.1, 0.04, edgecolor='black', facecolor='tab:blue', zorder=4)
    caster_d = patches.Circle((0.15, 0), 0.025, edgecolor='black', facecolor='tab:blue', zorder=4)
    center_d = patches.Circle((0, 0), 0.02, edgecolor='black', facecolor='black', zorder=5)

    ax_traj.add_patch(chassis_d)
    ax_traj.add_patch(wheel_L_d)
    ax_traj.add_patch(wheel_R_d)
    ax_traj.add_patch(caster_d)
    ax_traj.add_patch(center_d)
    
    fig.tight_layout()
    
    linha_traj.set_data(x, y)
    linha_x.set_data(t, x)
    linha_y.set_data(t, y)
    linha_phi.set_data(t, phi)
    
    tr_final = transforms.Affine2D().rotate(phi[-1]).translate(x[-1], y[-1]) + ax_traj.transData
    chassis_d.set_transform(tr_final)
    wheel_L_d.set_transform(tr_final)
    wheel_R_d.set_transform(tr_final)
    caster_d.set_transform(tr_final)
    center_d.set_transform(tr_final)
    
    nome_svg = os.path.join('imagens', f'estatico_direta_{nome}.svg')
    fig.savefig(nome_svg, format='svg', bbox_inches='tight')
    
    linha_traj.set_data([], [])
    linha_x.set_data([], [])
    linha_y.set_data([], [])
    linha_phi.set_data([], [])
    
    anim = FuncAnimation(
        fig, 
        atualizar, 
        frames=passos_totais, 
        fargs=(t, x, y, phi, linha_traj, linha_x, linha_y, linha_phi, chassis_d, wheel_L_d, wheel_R_d, caster_d, center_d, ax_traj), 
        interval=50, 
        blit=True
    )
    
    nome_gif = os.path.join('imagens', f'animacao_direta_{nome}.gif')
    anim.save(nome_gif, writer='pillow', fps=20)
    
    plt.close(fig)

print("Processo finalizado! SVGs e GIFs da Cinematica Direta salvos na pasta 'imagens/'.")
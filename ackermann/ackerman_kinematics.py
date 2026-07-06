import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns

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


def simular_ackermann(v, psi, L=0.2, dt=0.05, tf=5.0):
    """
    Cinematica Direta do modelo Ackermann:
    Recebe a velocidade linear (v) e o angulo de estercamento (psi) aplicados,
    e retorna a evolucao temporal da postura (x, y, theta) do chassi via integracao de Euler.
    """
    passos = int(tf / dt) + 1
    t = np.arange(passos) * dt

    if np.isscalar(v):
        v = np.full(passos, v)
    if np.isscalar(psi):
        psi = np.full(passos, psi)

    x = np.zeros(passos)
    y = np.zeros(passos)
    theta = np.zeros(passos)

    for i in range(1, passos):
        theta_atual = theta[i - 1]
        v_atual = v[i - 1]
        psi_atual = psi[i - 1]

        J = np.array([
            [np.cos(theta_atual)],
            [np.sin(theta_atual)],
            [np.tan(psi_atual) / L]
        ])

        q_dot = J * v_atual

        x_dot = q_dot[0, 0]
        y_dot = q_dot[1, 0]
        theta_dot = q_dot[2, 0]

        x[i] = x[i - 1] + x_dot * dt
        y[i] = y[i - 1] + y_dot * dt
        theta[i] = theta[i - 1] + theta_dot * dt

    return t, x, y, theta, v, psi


def simular_ackermann_inversa(v, omega, L=0.2):
    """
    Cinematica Inversa do modelo Ackermann:
    Recebe a velocidade linear (v) e angular (omega) desejadas para o chassi
    e retorna o angulo de estercamento (psi) necessario nas rodas dianteiras.
    """
    if abs(omega) < 1e-9:
        psi = 0.0
    else:
        R = v / omega
        psi = np.arctan(L / R)
    return v, psi


dist_eixos = 0.2
W = 0.12 # Largura do carro
wheel_l = 0.06
wheel_w = 0.025

corners_chassis = np.array([
    [-0.05, W/2],
    [dist_eixos + 0.05, W/2],
    [dist_eixos + 0.05, -W/2],
    [-0.05, -W/2],
    [-0.05, W/2]
])

corners_wheel = np.array([
    [-wheel_l/2, wheel_w/2],
    [wheel_l/2, wheel_w/2],
    [wheel_l/2, -wheel_w/2],
    [-wheel_l/2, -wheel_w/2],
    [-wheel_l/2, wheel_w/2]
])

def rot_matrix(angle):
    return np.array([[np.cos(angle), -np.sin(angle)],
                     [np.sin(angle),  np.cos(angle)]])

def get_wheel_pts(cx, cy, angle, theta, x, y):
    R_steer = rot_matrix(angle)
    pts = (R_steer @ corners_wheel.T).T
    pts[:, 0] += cx
    pts[:, 1] += cy
    R_theta = rot_matrix(theta)
    pts_global = (R_theta @ pts.T).T
    pts_global[:, 0] += x
    pts_global[:, 1] += y
    return pts_global[:, 0], pts_global[:, 1]

def get_chassis_pts(theta, x, y):
    R_theta = rot_matrix(theta)
    pts_global = (R_theta @ corners_chassis.T).T
    pts_global[:, 0] += x
    pts_global[:, 1] += y
    return pts_global[:, 0], pts_global[:, 1]


def atualizar(frame, x, y, t, theta, psi_arr, l_traj, l_x, l_y, l_theta, l_c, l_rl, l_rr, l_fl, l_fr):
    l_traj.set_data(x[:frame + 1], y[:frame + 1])
    l_x.set_data(t[:frame + 1], x[:frame + 1])
    l_y.set_data(t[:frame + 1], y[:frame + 1])
    l_theta.set_data(t[:frame + 1], theta[:frame + 1])
    
    x_f, y_f, th_f = x[frame], y[frame], theta[frame]
    psi_f = psi_arr[frame]
    
    c_x, c_y = get_chassis_pts(th_f, x_f, y_f)
    l_c.set_data(c_x, c_y)
    
    rl_x, rl_y = get_wheel_pts(0, W/2, 0, th_f, x_f, y_f)
    l_rl.set_data(rl_x, rl_y)
    
    rr_x, rr_y = get_wheel_pts(0, -W/2, 0, th_f, x_f, y_f)
    l_rr.set_data(rr_x, rr_y)
    
    fl_x, fl_y = get_wheel_pts(dist_eixos, W/2, psi_f, th_f, x_f, y_f)
    l_fl.set_data(fl_x, fl_y)
    
    fr_x, fr_y = get_wheel_pts(dist_eixos, -W/2, psi_f, th_f, x_f, y_f)
    l_fr.set_data(fr_x, fr_y)
    
    return l_traj, l_x, l_y, l_theta, l_c, l_rl, l_rr, l_fl, l_fr

def atualizar_inversa(frame, x, y, t, theta, psi_arr, v_val, w_val, l_traj, l_x, l_y, l_theta, l_c, l_rl, l_rr, l_fl, l_fr):
    l_traj.set_data(x[:frame + 1], y[:frame + 1])
    l_x.set_data(t[:frame + 1], np.full(frame + 1, v_val))
    l_y.set_data(t[:frame + 1], np.full(frame + 1, w_val))
    l_theta.set_data(t[:frame + 1], psi_arr[:frame + 1])
    
    x_f, y_f, th_f = x[frame], y[frame], theta[frame]
    psi_f = psi_arr[frame]
    
    c_x, c_y = get_chassis_pts(th_f, x_f, y_f)
    l_c.set_data(c_x, c_y)
    
    rl_x, rl_y = get_wheel_pts(0, W/2, 0, th_f, x_f, y_f)
    l_rl.set_data(rl_x, rl_y)
    
    rr_x, rr_y = get_wheel_pts(0, -W/2, 0, th_f, x_f, y_f)
    l_rr.set_data(rr_x, rr_y)
    
    fl_x, fl_y = get_wheel_pts(dist_eixos, W/2, psi_f, th_f, x_f, y_f)
    l_fl.set_data(fl_x, fl_y)
    
    fr_x, fr_y = get_wheel_pts(dist_eixos, -W/2, psi_f, th_f, x_f, y_f)
    l_fr.set_data(fr_x, fr_y)
    
    return l_traj, l_x, l_y, l_theta, l_c, l_rl, l_rr, l_fl, l_fr

tf_simulacao = 5.0
dt_simulacao = 0.05

# Cenarios da Cinematica Inversa: velocidades-alvo do chassi (v, omega)
cenarios_inversa = {
    "Frente": [0.4, 0.0],
    "Tras": [-0.4, 0.0],
    "Curva_Esquerda": [0.4, 0.6],
    "Curva_Direita": [0.4, -0.6]
}

def margem(vetor, frac=0.15, minimo=0.5):
    lo, hi = vetor.min(), vetor.max()
    span = hi - lo
    m = max(span * frac, minimo)
    return lo - m, hi + m

print("Renderizando SVGs e GIFs para a Cinematica Inversa do modelo de Ackermann...")

for nome, (v_alvo, w_alvo) in cenarios_inversa.items():
    print(f"Processando cenario (Inversa): {nome}...")

    # Passo 1: CINEMATICA INVERSA
    v_val, psi_val = simular_ackermann_inversa(v_alvo, w_alvo, L=dist_eixos)

    # Passo 2: CINEMATICA DIRETA
    t, x, y, theta, v_arr, psi_arr = simular_ackermann(v_val, psi_val, L=dist_eixos, dt=dt_simulacao, tf=tf_simulacao)
    passos_totais = len(t)

    x_lim = margem(x)
    y_lim = margem(y)
    theta_lim = margem(theta, frac=0.1, minimo=0.3)

    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.2, 1])

    ax_traj = fig.add_subplot(gs[:, 0])
    ax_traj.set_xlim(*x_lim)
    ax_traj.set_ylim(*y_lim)
    ax_traj.set_aspect('equal')
    ax_traj.set_xlabel('Posicao X (m)')
    ax_traj.set_ylabel('Posicao Y (m)')
    linha_traj, = ax_traj.plot([], [], color='gray', linestyle='--', linewidth=1.5,
                                label=f'$v$={v_val}, $\\psi$={psi_val}')
    ax_traj.legend(loc='upper right')
    
    # Linhas do carro
    l_c, = ax_traj.plot([], [], color='#2E86AB', linewidth=2) # Chassi azulado
    l_rl, = ax_traj.plot([], [], color='black', linewidth=4)
    l_rr, = ax_traj.plot([], [], color='black', linewidth=4)
    l_fl, = ax_traj.plot([], [], color='black', linewidth=4)
    l_fr, = ax_traj.plot([], [], color='black', linewidth=4)

    ax_x = fig.add_subplot(gs[0, 1])
    ax_x.set_xlim(0, tf_simulacao)
    ax_x.set_ylim(-0.5, 0.5)
    ax_x.set_ylabel('v (m/s)')
    linha_x, = ax_x.plot([], [], color='blue', linewidth=2, label=f'v = {v_alvo:.2f} m/s')
    ax_x.legend(loc='upper right')

    ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
    ax_y.set_ylim(-1.0, 1.0)
    ax_y.set_ylabel('$\\omega$ (rad/s)')
    linha_y, = ax_y.plot([], [], color='red', linewidth=2, label=f'$\\omega$ = {w_alvo:.2f} rad/s')
    ax_y.legend(loc='upper right')

    ax_theta = fig.add_subplot(gs[2, 1], sharex=ax_x)
    ax_theta.set_ylim(-1.0, 1.0)
    ax_theta.set_ylabel('$\\psi$ (rad)')
    ax_theta.set_xlabel('Tempo (s)')
    linha_theta, = ax_theta.plot([], [], color='green', linewidth=2, label=f'$\\psi$ = {psi_val:.2f} rad')
    ax_theta.legend(loc='upper right')

    fig.tight_layout()

    # SVG (estatico, desenha o carro na posicao final)
    linha_traj.set_data(x, y)
    linha_x.set_data(t, np.full(len(t), v_alvo))
    linha_y.set_data(t, np.full(len(t), w_alvo))
    linha_theta.set_data(t, psi_arr)
    
    # Desenhar o carro no ultimo frame pro SVG
    x_f, y_f, th_f = x[-1], y[-1], theta[-1]
    p_f = psi_arr[-1]
    cx, cy = get_chassis_pts(th_f, x_f, y_f)
    l_c.set_data(cx, cy)
    wx, wy = get_wheel_pts(0, W/2, 0, th_f, x_f, y_f)
    l_rl.set_data(wx, wy)
    wx, wy = get_wheel_pts(0, -W/2, 0, th_f, x_f, y_f)
    l_rr.set_data(wx, wy)
    wx, wy = get_wheel_pts(dist_eixos, W/2, p_f, th_f, x_f, y_f)
    l_fl.set_data(wx, wy)
    wx, wy = get_wheel_pts(dist_eixos, -W/2, p_f, th_f, x_f, y_f)
    l_fr.set_data(wx, wy)
    
    fig.savefig(os.path.join('imagens', f'estatico_ackermann_{nome}.svg'), format='svg', bbox_inches='tight')

    # Limpando para o GIF
    linha_traj.set_data([], [])
    linha_x.set_data([], [])
    linha_y.set_data([], [])
    linha_theta.set_data([], [])
    l_c.set_data([], [])
    l_rl.set_data([], [])
    l_rr.set_data([], [])
    l_fl.set_data([], [])
    l_fr.set_data([], [])

    anim = FuncAnimation(
        fig, atualizar_inversa, frames=passos_totais,
        fargs=(x, y, t, theta, psi_arr, v_alvo, w_alvo, linha_traj, linha_x, linha_y, linha_theta, l_c, l_rl, l_rr, l_fl, l_fr),
        interval=50, blit=True
    )
    anim.save(os.path.join('imagens', f'animacao_ackermann_{nome}.gif'), writer='pillow', fps=20)

    plt.close(fig)

print("Processo finalizado! SVGs e GIFs da Cinematica Inversa salvos.")

# ============================================================================
# CINEMATICA DIRETA: cenarios com v e psi especificados diretamente
# O algoritmo recebe as velocidades de entrada e integra a postura via Euler.
# ============================================================================

cenarios_direta = {
    "Direta_Frente": [0.4, 0.0],
    "Direta_Tras": [-0.4, 0.0],
    "Direta_Curva_Esquerda": [0.4, 0.3],
    "Direta_Curva_Direita": [0.4, -0.3]
}

print("\nRenderizando SVGs e GIFs para a Cinematica Direta do modelo de Ackermann...")

for nome, (v_val, psi_val) in cenarios_direta.items():
    print(f"Processando cenario (Direta): {nome}...")

    t, x, y, theta, v_arr, psi_arr = simular_ackermann(v_val, psi_val, L=dist_eixos, dt=dt_simulacao, tf=tf_simulacao)
    passos_totais = len(t)

    x_lim = margem(x)
    y_lim = margem(y)
    theta_lim = margem(theta, frac=0.1, minimo=0.3)

    fig = plt.figure(figsize=(10, 5))
    gs = fig.add_gridspec(3, 2, width_ratios=[1.2, 1])

    ax_traj = fig.add_subplot(gs[:, 0])
    ax_traj.set_xlim(*x_lim)
    ax_traj.set_ylim(*y_lim)
    ax_traj.set_aspect('equal')
    ax_traj.set_xlabel('Posicao X (m)')
    ax_traj.set_ylabel('Posicao Y (m)')
    linha_traj, = ax_traj.plot([], [], color='gray', linestyle='--', linewidth=1.5,
                                label=f'$v$={v_val}, $\\psi$={psi_val:.2f}')
    ax_traj.legend(loc='upper right')
    
    l_c, = ax_traj.plot([], [], color='#2E86AB', linewidth=2)
    l_rl, = ax_traj.plot([], [], color='black', linewidth=4)
    l_rr, = ax_traj.plot([], [], color='black', linewidth=4)
    l_fl, = ax_traj.plot([], [], color='black', linewidth=4)
    l_fr, = ax_traj.plot([], [], color='black', linewidth=4)

    ax_x = fig.add_subplot(gs[0, 1])
    ax_x.set_xlim(0, tf_simulacao)
    ax_x.set_ylim(*x_lim)
    ax_x.set_ylabel('x (m)')
    linha_x, = ax_x.plot([], [], color='blue', linewidth=2)

    ax_y = fig.add_subplot(gs[1, 1], sharex=ax_x)
    ax_y.set_ylim(*y_lim)
    ax_y.set_ylabel('y (m)')
    linha_y, = ax_y.plot([], [], color='red', linewidth=2)

    ax_theta = fig.add_subplot(gs[2, 1], sharex=ax_x)
    ax_theta.set_ylim(*theta_lim)
    ax_theta.set_ylabel('$\\theta$ (rad)')
    ax_theta.set_xlabel('Tempo (s)')
    linha_theta, = ax_theta.plot([], [], color='green', linewidth=2)

    fig.tight_layout()

    linha_traj.set_data(x, y)
    linha_x.set_data(t, x)
    linha_y.set_data(t, y)
    linha_theta.set_data(t, theta)
    
    x_f, y_f, th_f = x[-1], y[-1], theta[-1]
    p_f = psi_arr[-1]
    cx, cy = get_chassis_pts(th_f, x_f, y_f)
    l_c.set_data(cx, cy)
    wx, wy = get_wheel_pts(0, W/2, 0, th_f, x_f, y_f)
    l_rl.set_data(wx, wy)
    wx, wy = get_wheel_pts(0, -W/2, 0, th_f, x_f, y_f)
    l_rr.set_data(wx, wy)
    wx, wy = get_wheel_pts(dist_eixos, W/2, p_f, th_f, x_f, y_f)
    l_fl.set_data(wx, wy)
    wx, wy = get_wheel_pts(dist_eixos, -W/2, p_f, th_f, x_f, y_f)
    l_fr.set_data(wx, wy)
    
    fig.savefig(os.path.join('imagens', f'estatico_ackermann_direta_{nome}.svg'), format='svg', bbox_inches='tight')

    linha_traj.set_data([], [])
    linha_x.set_data([], [])
    linha_y.set_data([], [])
    linha_theta.set_data([], [])
    l_c.set_data([], [])
    l_rl.set_data([], [])
    l_rr.set_data([], [])
    l_fl.set_data([], [])
    l_fr.set_data([], [])

    anim = FuncAnimation(
        fig, atualizar, frames=passos_totais,
        fargs=(x, y, t, theta, psi_arr, linha_traj, linha_x, linha_y, linha_theta, l_c, l_rl, l_rr, l_fl, l_fr),
        interval=50, blit=True
    )
    anim.save(os.path.join('imagens', f'animacao_ackermann_direta_{nome}.gif'), writer='pillow', fps=20)

    plt.close(fig)

print("Processo finalizado! SVGs e GIFs da Cinematica Direta salvos.")
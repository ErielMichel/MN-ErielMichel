import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Parámetros físicos
m = 0.43            # Masa del balón (kg)
g = 9.81            # Gravedad
rho = 1.225         # Densidad del aire al nivel del mar
Cd = 0.25           # Coeficiente de arrastre
Cm = 0.23           # Coeficiente de Magnus
r = 0.11            # Radio del balón
A = np.pi * r**2    # Área frontal del balón

def simular_tiro(velocidad_angular):
    def ecuaciones_balon(t, estado):
        x, y, z, vx, vy, vz = estado
        v = np.array([vx, vy, vz])
        v_mag = np.linalg.norm(v)
        
        # Si la velocidad angular es 0, no hay efecto Magnus
        omega = np.array([0, 0, velocidad_angular])
        
        F_drag = -0.5 * rho * Cd * A * v_mag * v
        F_magnus = 0.5 * rho * Cm * A * r * np.cross(omega, v)
        F_gravedad = np.array([0, 0, -m * g])
        
        a = (F_drag + F_magnus + F_gravedad) / m
        return [vx, vy, vz, a[0], a[1], a[2]]

    def toca_suelo(t, estado): return estado[2]
    toca_suelo.terminal, toca_suelo.direction = True, -1

    
    v0, theta = 26.0, np.radians(22.0)
    phi = np.radians(10.0)
    
    vx = v0 * np.cos(theta) * np.cos(phi)
    vy = v0 * np.cos(theta) * np.sin(phi) 
    vz = v0 * np.sin(theta)
    
    estado_inicial = [0.0, 0.0, 0.0, vx, vy, vz]
    
    sol = solve_ivp(ecuaciones_balon, (0, 5.0), estado_inicial, method='RK45', max_step=0.01, events=toca_suelo)
    return sol.y[0], sol.y[1], sol.y[2]


# Tiro 1: Sin efecto (Línea recta, se va afuera)
x_recto, y_recto, z_recto = simular_tiro(0.0)

# Tiro 2: Con Efecto (La comba)
x_curva, y_curva, z_curva = simular_tiro(-90.0)


fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#132b20')
ax.set_facecolor('#132b20')

# Área y arco
ax.plot([25, 25, 5.5, 5.5, 25], [-15, 15, 15, -15, -15], color='white', linewidth=2, alpha=0.2) 
ax.plot([25, 25], [-3.66, 3.66], color='white', linewidth=4)

# Portero
ax.add_patch(patches.Circle((24.5, -2.0), radius=0.5, color='#FFD700', ec='white', lw=1, zorder=5))

# La línea recta (Sin efecto)
ax.plot(x_recto, y_recto, color='gray', linewidth=2, linestyle='--', label='Trayectoria sin efecto (afuera)')

# La línea con efecto 
ax.plot(x_curva, y_curva, color='#39FF14', linewidth=3, label='Trayectoria con Efecto Magnus')
sizes = np.interp(z_curva, (z_curva.min(), z_curva.max()), (10, 80)) 
ax.scatter(x_curva, y_curva, c=z_curva, cmap='plasma', s=sizes, zorder=4, edgecolors='white', linewidths=0.5)

ax.plot(0, 0, marker='o', markersize=12, color='white', zorder=6)

ax.set_title('La magia de la comba: Recto vs Efecto', color='white', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Distancia al arco (m)', color='#A0A0A0')
ax.set_ylabel('Ancho de la cancha (m)', color='#A0A0A0')

# Hacemos un zoom en el ancho de la cancha para que la comba se aprecie
ax.set_xlim(-2, 28)
ax.set_ylim(-5, 8) 
ax.set_aspect('equal') 

ax.tick_params(colors='#A0A0A0')
for spine in ax.spines.values(): spine.set_edgecolor('#A0A0A0')

# Leyenda
legend = ax.legend(loc='upper left', facecolor='#132b20', edgecolor='white')
for text in legend.get_texts(): text.set_color('white')

plt.tight_layout()
plt.savefig('comparacion_efecto.png', dpi=300, bbox_inches='tight', facecolor='#132b20')
plt.show()
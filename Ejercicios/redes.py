import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.text import Text

def draw_network_topology():
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Título
    ax.text(8, 11.5, 'Tarea 3: Configuración de Red Cisco', fontsize=16, ha='center', weight='bold')
    
    # Dibujar routers
    hq = patches.Rectangle((4, 5), 2, 2, linewidth=3, edgecolor='blue', facecolor='lightblue')
    br1 = patches.Rectangle((10, 7), 2, 2, linewidth=3, edgecolor='green', facecolor='lightgreen')
    br2 = patches.Rectangle((10, 3), 2, 2, linewidth=3, edgecolor='red', facecolor='lightcoral')
    
    ax.add_patch(hq)
    ax.add_patch(br1)
    ax.add_patch(br2)
    
    # Texto de los routers
    ax.text(5, 6, 'HQ\nS0/0/0: 10.10.10.252/30\nS0/0/1: 172.16.100.1/30\nLB0: 192.168.4.1/24\nLB1: 192.168.5.1/24\nLB2: 192.168.6.1/24', 
            ha='center', va='center', fontsize=9, fontfamily='monospace', weight='bold')
    
    ax.text(11, 8, 'BRANCH1 (W)\nS0/0/0: 10.10.10.253/30\nLB0: 192.168.1.1/24\nLB1: 192.168.2.1/24\nLB2: 192.168.3.1/24', 
            ha='center', va='center', fontsize=9, fontfamily='monospace', weight='bold')
    
    ax.text(11, 4, 'BRANCH2 (E)\nS0/0/1: 172.16.100.2/30\nLB0: 192.168.7.1/24\nLB1: 192.168.8.1/24\nLB2: 192.168.9.1/24', 
            ha='center', va='center', fontsize=9, fontfamily='monospace', weight='bold')
    
    # Conexiones
    ax.plot([6, 10], [6, 8], 'k-', linewidth=2)
    ax.plot([6, 10], [6, 4], 'k-', linewidth=2)
    
    # Etiquetas de conexiones
    ax.text(8, 7.2, '10.10.10.252/30 ↔ 10.10.10.253/30', fontsize=9, ha='center', 
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))
    ax.text(8, 4.8, '172.16.100.1/30 ↔ 172.16.100.2/30', fontsize=9, ha='center', 
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='black'))
    
    # Leyenda de interfaces
    ax.text(2, 1, 'Leyenda:\n• S0/0/0, S0/0/1: Interfaces seriales\n• LB0, LB1, LB2: Interfaces LAN', 
            fontsize=10, bbox=dict(facecolor='lightyellow', alpha=0.8, edgecolor='orange'))
    
    # Notas
    ax.text(8, 0.5, 'Nota: Configure el reloj en interfaces seriales DCE\n      Asigne direcciones IP según tabla de direccionamiento', 
            fontsize=10, ha='center', style='italic', color='darkred')
    
    plt.tight_layout()
    plt.savefig('cisco_network_topology.png', dpi=300, bbox_inches='tight')
    plt.show()

draw_network_topology()
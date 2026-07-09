import matplotlib.pyplot as plt
import networkx as nx
import random
from matplotlib.animation import FuncAnimation
import numpy as np
def generate_animation(filename='static/animation.gif'):
    random.seed(10)

    restaurants = {
        'R1': (2, 2),
        'R2': (-3, 1),
        'R3': (1, -3)
    }

    depots = {
        'D1': (2.2, 2.2),
        'D2': (-2.8, 1.2),
        'D3': (1.2, -2.8)
    }

    customers = {
        f'C{i+1}': (random.uniform(-5, 5), random.uniform(-5, 5))
        for i in range(10)
    }

    agents = {
        'A1': depots['D1'],
        'A2': depots['D2'],
        'A3': depots['D3']
    }

    agent_paths = {
        'A1': ['D1', 'R1', 'C1', 'C2', 'C3', 'D1'],
        'A2': ['D2', 'R2', 'C4', 'C5', 'C6', 'D2'],
        'A3': ['D3', 'R3', 'C7', 'C8', 'C9', 'C10', 'D3']
    }

    G = nx.Graph()
    for d, pos in depots.items():
        G.add_node(d, pos=pos)
    for r, pos in restaurants.items():
        G.add_node(r, pos=pos)
    for c, pos in customers.items():
        G.add_node(c, pos=pos)
    for a, pos in agents.items():
        G.add_node(a, pos=pos)
    for path in agent_paths.values():
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1])

    pos = nx.get_node_attributes(G, 'pos')

    def interpolate(p1, p2, steps=30):
        x = np.linspace(p1[0], p2[0], steps)
        y = np.linspace(p1[1], p2[1], steps)
        return list(zip(x, y))

    agent_coords = {}
    agent_segments = {}
    for agent, path in agent_paths.items():
        coords, segments = [], []
        for i in range(len(path) - 1):
            p1, p2 = pos[path[i]], pos[path[i+1]]
            segment = interpolate(p1, p2, steps=25)
            coords.extend(segment)
            segments.extend([f"{path[i]} → {path[i+1]}"] * len(segment))
        agent_coords[agent] = coords
        agent_segments[agent] = segments

    fig, ax = plt.subplots(figsize=(12, 9))
    agent_colors = {'A1': 'red', 'A2': 'blue', 'A3': 'green'}
    agent_dots = {
        agent: ax.plot([], [], 'o', color=color, markersize=9)[0]
        for agent, color in agent_colors.items()
    }
    status_texts = {
        agent: ax.text(1.01, 0.8 - i*0.25, '', transform=ax.transAxes, fontsize=10, va='top')
        for i, agent in enumerate(agent_coords)
    }

    def setup_static():
        ax.clear()
        nx.draw_networkx_nodes(G, pos, nodelist=depots, node_color='black', node_size=300, label='Depots', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=restaurants, node_color='orange', node_size=300, label='Restaurants', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=customers, node_color='lightgreen', node_size=250, label='Customers', ax=ax)
        for path in agent_paths.values():
            edge_list = list(zip(path[:-1], path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='gray', width=1.5, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', ax=ax)
        ax.set_title("Clean Delivery Path Animation", fontsize=14)
        ax.axis("off")
        ax.legend(loc='lower right')
        ax.text(1.01, 1.0,
            "Assignments\n"
            "------------------\n"
            "A1 → C1, C2, C3\n"
            "A2 → C4, C5, C6\n"
            "A3 → C7, C8, C9, C10",
            transform=ax.transAxes, fontsize=9, va='top', bbox=dict(facecolor='whitesmoke', edgecolor='gray'))

    max_frames = max(len(c) for c in agent_coords.values())

    def update(frame):
        ax.clear()
        setup_static()
        for agent in agent_coords:
            coords = agent_coords[agent]
            if frame < len(coords):
                x, y = coords[frame]
                agent_dots[agent].set_data(x, y)
                ax.add_artist(agent_dots[agent])
                segment = agent_segments[agent][frame]
                next_node = segment.split(' → ')[1]
                status = f"{agent} now: {segment}\nNext: {next_node}"
                status_texts[agent].set_text(status)

    setup_static()
    ani = FuncAnimation(fig, update, frames=max_frames, interval=120, repeat=False)
    ani.save(filename, writer='pillow', fps=10)
    plt.close(fig)

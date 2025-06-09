import networkx as nx
import argparse
import yaml
import json
import random
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_search(G, history, found_at=None):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8, 6))

    def update(i):
        ax.clear()
        nx.draw_networkx_nodes(G, pos, node_color='lightgray', ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)

        visited = history[:i+1]
        path_nodes = [x[0] for x in visited]

        # Color visited nodes
        colors = ['green' if node == found_at else 'yellow' for node in path_nodes]
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_color=colors, ax=ax)

        ax.set_title(f"Step {i+1}/{len(history)}")
        ax.axis('off')

    ani = animation.FuncAnimation(fig, update, frames=len(history), interval=1000, repeat=False)
    plt.show()


def load_config(path):
    with open(path, 'r') as f:
        if path.endswith('.yaml') or path.endswith('.yml'):
            return yaml.safe_load(f)
        elif path.endswith('.json'):
            return json.load(f)
        else:
            raise ValueError("Unsupported config format")

def build_graph(config):
    G = nx.Graph()
    for node, res in config['nodes'].items():
        G.add_node(node, resources=set(res), cache=set())
    for u, v in config['edges']:
        G.add_edge(u, v)
    return G

def validate_graph(G, config):
    if not nx.is_connected(G):
        raise ValueError("Graph is not connected.")
    for node, data in G.nodes(data=True):
        if len(data['resources']) > 0:
            for r in data['resources']:
                if r not in config['resources']:
                    raise ValueError(f"Resource {r} in node {node} is not declared.")
    for node in G.nodes:
        if G.degree[node] < config.get('min_degree', 1):
            raise ValueError(f"Node {node} has degree less than min_degree.")

def flooding(G, start, target, ttl):
    visited = set()
    queue = deque([(start, ttl)])
    messages = 0
    nodes = set()
    while queue:
        current, t = queue.popleft()
        if t < 0 or current in visited:
            continue
        visited.add(current)
        nodes.add(current)
        messages += 1
        if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
            return messages, len(nodes)
        for neighbor in G.neighbors(current):
            queue.append((neighbor, t - 1))
    return messages, len(nodes)

def informed_flooding(G, start, target, ttl):
    visited = set()
    queue = deque([(start, ttl)])
    messages = 0
    nodes = set()
    while queue:
        current, t = queue.popleft()
        if t < 0 or current in visited:
            continue
        visited.add(current)
        nodes.add(current)
        messages += 1
        if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
            for node in visited:
                G.nodes[node]['cache'].add(target)
            return messages, len(nodes)
        for neighbor in G.neighbors(current):
            if target in G.nodes[neighbor]['cache']:
                queue.appendleft((neighbor, t - 1))
            else:
                queue.append((neighbor, t - 1))
    return messages, len(nodes)

def random_walk(G, start, target, ttl, visualize=False):
    current = start
    messages = 0
    visited = set()
    history = [(current,)]

    for _ in range(ttl + 1):
        messages += 1
        visited.add(current)
        if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
            if visualize:
                animate_search(G, history, found_at=current)
            return messages, len(visited)
        neighbors = list(G.neighbors(current))
        if not neighbors:
            break
        current = random.choice(neighbors)
        history.append((current,))

    if visualize:
        animate_search(G, history)
    return messages, len(visited)


def informed_random_walk(G, start, target, ttl):
    current = start
    messages = 0
    visited = set()
    for _ in range(ttl + 1):
        messages += 1
        visited.add(current)
        if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
            for node in visited:
                G.nodes[node]['cache'].add(target)
            return messages, len(visited)
        neighbors = list(G.neighbors(current))
        random.shuffle(neighbors)
        informed = [n for n in neighbors if target in G.nodes[n]['cache']]
        if informed:
            current = informed[0]
        elif neighbors:
            current = neighbors[0]
        else:
            break
    return messages, len(visited)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--node", required=True)
    parser.add_argument("--resource", required=True)
    parser.add_argument("--ttl", type=int, required=True)
    parser.add_argument("--algo", choices=["flooding", "informed_flooding", "random_walk", "informed_random_walk"], required=True)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    G = build_graph(config)
    validate_graph(G, config)

    algos = {
        "flooding": flooding,
        "informed_flooding": informed_flooding,
        "random_walk": random_walk,
        "informed_random_walk": informed_random_walk
    }

    # messages, nodes = algos[args.algo](G, args.node, args.resource, args.ttl)
    messages, nodes = algos[args.algo](G, args.node, args.resource, args.ttl, visualize=args.visualize)

    print(f"Algorithm: {args.algo}")
    print(f"Messages exchanged: {messages}")
    print(f"Nodes involved: {nodes}")

if __name__ == "__main__":
    main()

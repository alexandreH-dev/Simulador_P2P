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

        visited_nodes = [node for node, _ in history[:i+1]]
        colors = []
        for node, found in history[:i+1]:
            if found:
                colors.append('green')
            else:
                colors.append('yellow')

        nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color=colors, ax=ax)

        ax.set_title(f"Passo {i+1}/{len(history)}")
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
    found = False

    while queue:
        current, t = queue.popleft()
        if t < 0 or current in visited:
            continue
        visited.add(current)
        nodes.add(current)
        messages += 1

        if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
            print(f"[{messages}] Visitando nó '{current}': Recurso encontrado! ✅")
            found = True
            break
        else:
            print(f"[{messages}] Visitando nó '{current}': Recurso não encontrado ❌")

        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                print(f"-> Enviando mensagem para vizinho '{neighbor}' (TTL={t-1})")
                queue.append((neighbor, t - 1))

    # Exibir nós que ficaram na fila mas não foram processados (opcional)
    while queue:
        current, _ = queue.popleft()
        if current not in visited:
            print(f"[-] Visitando nó '{current}': Recurso não encontrado ❌")

    if not found:
        print("Busca finalizada. Recurso não foi encontrado.")
    return messages, len(nodes)

def random_walk(G, start, target, ttl, visualize=False):
    current = start
    messages = 0
    visited = set()
    history = [(current, False)]  # (nó, achou?)

    for step in range(ttl + 1):
        messages += 1
        visited.add(current)

        found = target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']
        if found:
            print(f"[{messages}] Visitando nó '{current}': Recurso encontrado! ✅")
            history[-1] = (current, True)  # Atualiza o status de achado
            if visualize:
                animate_search(G, history, found_at=current)
            return messages, len(visited)
        else:
            print(f"[{messages}] Visitando nó '{current}': Recurso não encontrado ❌")

        neighbors = [n for n in G.neighbors(current) if n not in visited]
        if not neighbors:
            print(f"-> Nenhum vizinho novo para visitar a partir de '{current}'. Encerrando.")
            break

        next_node = random.choice(neighbors)
        print(f"-> Escolhendo vizinho '{next_node}' para próxima visita (TTL restante: {ttl - step})")
        current = next_node
        history.append((current, False))

    if visualize:
        animate_search(G, history)

    print("Busca finalizada. Recurso não foi encontrado.")
    return messages, len(visited)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--node", required=True)
    parser.add_argument("--resource", required=True)
    parser.add_argument("--ttl", type=int, required=True)
    parser.add_argument("--algo", choices=["flooding", "random_walk"], required=True)
    parser.add_argument("--visualize", action="store_true")
    args = parser.parse_args()

    config = load_config(args.config)
    G = build_graph(config)
    validate_graph(G, config)

    algos = {
        "flooding": flooding,
        "random_walk": random_walk
    }

    # Execução do algoritmo
    if args.algo == "random_walk":
        messages, nodes = algos[args.algo](G, args.node, args.resource, args.ttl, visualize=args.visualize)
    else:
        messages, nodes = algos[args.algo](G, args.node, args.resource, args.ttl)

    print("\n===== RESULTADO FINAL =====")
    print(f"Algoritmo: {args.algo}")
    print(f"Mensagens trocadas: {messages}")
    print(f"Nós envolvidos: {nodes}")

if __name__ == "__main__":
    main()

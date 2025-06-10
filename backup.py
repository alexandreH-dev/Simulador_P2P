# def flooding(G, start, target, ttl):
#     visited = set()
#     queue = deque([(start, ttl)])
#     messages = 0
#     nodes = set()
#     found = False
#     found_at = None

#     while queue:
#         current, t = queue.popleft()
#         if t < 0 or current in visited:
#             continue
#         visited.add(current)
#         nodes.add(current)
#         messages += 1

#         if not found and (target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']):
#             print(f"[{messages}] Visitando nó '{current}': Recurso encontrado! ✅")
#             found = True
#             found_at = current
#         else:
#             print(f"[{messages}] Visitando nó '{current}': Recurso não encontrado ❌")

#         for neighbor in G.neighbors(current):
#             if neighbor not in visited:
#                 print(f"-> Enviando mensagem para vizinho '{neighbor}' (TTL={t-1})")
#                 queue.append((neighbor, t - 1))

#     if not found:
#         print("Busca finalizada. Recurso não foi encontrado.")
#     else:
#         print(f"\n✔ Recurso foi encontrado no nó '{found_at}'.")

#     return messages, len(nodes)


# def random_walk(G, start, target, ttl, visualize=False):
#     current = start
#     messages = 0
#     visited = set()
#     history = [(current,)]

#     for step in range(ttl + 1):
#         if current in visited:
#             print(f"[{messages+1}] Nó '{current}' já foi visitado. Pulando.")
#             break

#         visited.add(current)
#         messages += 1
#         print(f"[{messages}] Visitando nó '{current}': ", end='')

#         if target in G.nodes[current]['resources'] or target in G.nodes[current]['cache']:
#             print("Recurso encontrado! ✅")
#             if visualize:
#                 animate_search(G, history, found_at=current)
#             return messages, len(visited)
#         else:
#             print("Recurso não encontrado ❌")

#         neighbors = [n for n in G.neighbors(current) if n not in visited]
#         if not neighbors:
#             print("Sem vizinhos não visitados disponíveis. Encerrando busca.")
#             break

#         next_node = random.choice(neighbors)
#         print(f"-> Caminhando para vizinho '{next_node}'")
#         current = next_node
#         history.append((current,))

#     if visualize:
#         animate_search(G, history)
#     print("Busca finalizada. Recurso não foi encontrado.")
#     return messages, len(visited)
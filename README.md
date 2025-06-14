# 🔎 Algoritmos de Busca em Redes P2P

Este projeto implementa quatro algoritmos de busca para sistemas peer-to-peer (P2P), simulando a propagação de requisições em uma rede distribuída. É possível visualizar a busca em tempo real por meio de animações interativas.

## 📌 Algoritmos Implementados

- 🔁 Flooding  
- 🎲 Random Walk  

Cada algoritmo respeita o parâmetro TTL (Time-To-Live), limitando o número de saltos permitidos na rede.

---

## 📂 Estrutura do Projeto

```bash
p2p_search/
├── p2p_search.py        # Código principal com os algoritmos
├── config.yaml          # Arquivo de configuração da rede
├── requirements.txt     # Dependências do projeto
├── README.md            # Este arquivo
```
---

## ⚙️ Instalação
1. Clone o repositório:
```bash
git clone https://github.com/alexandreH-dev/Simulador_P2P.git
cd p2p_search
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
---

## 🧾 Configuração
Exemplo de config.yaml:
```yaml
nodes:
  n1: [r1]
  n2: []
  n3: [r2]
  n4: []
  n5: []

edges:
  - [n1, n2]
  - [n2, n3]
  - [n3, n4]
  - [n4, n5]
  - [n5, n1]

resources:
  - r1
  - r2

min_degree: 1
```
```yaml
nodes:
  n1: [r1]
  n2: [r2]
  n3: [r3]
  n4: [r4]
  n5: [r5]
  n6: [r6]

edges:
  - [n1, n2]
  - [n2, n3]
  - [n2, n4]
  - [n3, n6]
  - [n3, n5]

resources:
  - r1
  - r2
  - r3
  - r4
  - r5
  - r6

min_degree: 1
```
--- 
## 🚀 Como Executar
### 🔍 Execução padrão
```bash
python p2p_search.py config.yaml --node n1 --resource r3 --ttl 3 --algo flooding
```
### 🎞️ Execução com visualização animada
```bash
python p2p_search.py config.yaml --node n1 --resource r3 --ttl 3 --algo random_walk --visualize
```

--- 
## 📊 Saída
Ao final da execução, o programa exibe:

- Algoritmo utilizado

- Número de mensagens trocadas

- Total de nós envolvidos na busca

Exemplo:
```yaml
Algorithm: random_walk
Messages exchanged: 4
Nodes involved: 4
```


---

## 📈 Visualização
A animação exibe a progressão da busca em tempo real com:

- Círculos amarelos: nós visitados
- Círculo verde: nó onde o recurso foi encontrado
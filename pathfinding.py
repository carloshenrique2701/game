from collections import deque 

"""
A classe PathFinding é projetada para encontrar o 
caminho mais curto entre dois pontos em um mapa 2D baseado em grade, 
evitando obstáculos e NPCs (personagens não jogáveis).

"""
class PathFinding:
	# Inicializa a classe com um objeto de jogo, um mapa miniatura e um conjunto de movimentos possíveis (para cima, para baixo, para a esquerda, para a direita e diagonais). 
	# Também cria um grafo vazio e chama o método get_graph para populá-lo.
	def __init__(self, game):
		self.game = game 
		self.map = game.map.mini_map
		self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1] 
		self.graph = {} 
		self.get_graph() 

	# Utiliza a busca em largura (BFS) para encontrar o caminho mais curto entre um nó start e um nó goal em um grafo. 
	# Em seguida, ela reconstrói o caminho percorrendo os nós do goal até o start e retorna o último nó do caminho (ou seja, o nó que precede o start).
	def get_path(self, start, goal):
		self.visited = self.bfs(start, goal, self.graph)
		path = [goal]
		step = self.visited.get(goal, start)


		while step and step != start:
			path.append(step)
			step = self.visited[step]
		return path[-1]

	#realiza uma Busca em Largura (BFS) em um grafo para encontrar o caminho mais curto de um nó 'start' para todos os outros nós, parando quando atinge um nó 'objetivo'(goal).
	def bfs(self, start, goal, graph):
		queue = deque([start]) #insere o nó inicial na fila usando o deque(estrutura de dados que suporta eficientemente a adição e remoção de elementos em ambos os extremos (início e fim).)
		visited = {start: None}

		while queue:
			cur_node = queue.popleft()
			if cur_node == goal:
				break 

			next_nodes = graph[cur_node]

			for next_node in next_nodes:
				if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
					queue.append(next_node)
					visited[next_node] = cur_node
		return visited

	def get_next_nodes(self, x, y):
		return [(x + dx , y + dy) for dx, dy in self.ways if (x + dx, y + dy) not in self.game.map.world_map] #retorna os nós vizinhos do nó (x, y) que não são obstáculos.

	#constrói um grafo a partir de um mapa 2D, adicionando conexões entre células vazias adjacentes.
	def get_graph(self):
		for y, row in enumerate(self.map):
			for x, col in enumerate(row):
				if not col:
					self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y) 



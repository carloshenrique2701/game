import pygame as pg 
from settings import * 

# O que criamos nesta 4 aula
class ObjectRenderer:

	def __init__(self, game):
		self.game = game 
		self.screen = game.screen
		self.wall_textures = self.load_wall_textures()

		#textura do ceu
		self.sky_image = self.get_texture('resources/textures/sky.png', (width, half_height))
		self.sky_offset = 0 

		#magem que indica que o player sofreu dano
		self.blood_screen = self.get_texture('resources/textures/blood_screen.png', res)

		#Texturas dos dígitos de sanidade / vida
		self.digit_size = 90 
		self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
							for i in range(11)]
		self.digits = dict(zip(map(str, range(11)), self.digit_images))
		self.game_over_image = self.get_texture('resources/textures/game_over.png', res)

		#Lanterna
		self.darkness = pg.Surface((width, height), pg.SRCALPHA)
		self.darkness.fill((0, 0, 0, 180))
		self.light_mask = self.create_light_mask()

	def create_light_mask(self):
		mask = pg.Surface((width, height), pg.SRCALPHA)
		radius = self.game.player.light_radius

		# Cálculo da posição da luz com base no ângulo do jogador
		angle = self.game.player.angle
		offset_distance = radius * 0.5  # distância da lanterna à frente do jogador

		center_x = int(width // 2 + offset_distance * math.cos(angle))
		center_y = int(height // 2 + offset_distance * math.sin(angle) * 0.5)  # vertical mais suave

		for y in range(height):
			for x in range(width):
				dist = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
				if dist <= radius:
					alpha = int(255 * (1 - dist / radius))
					mask.set_at((x, y), (255, 255, 255, alpha))

		return mask


	def draw(self):
		self.draw_background()
		self.render_game_objects()
		self.draw_player_health()
		
		# Depois aplica a escuridão com a lanterna
		if not self.light_mask:
			self.create_light_mask()
		
		# Cria uma cópia da escuridão
		final_darkness = self.darkness.copy()
		
		# Aplica a máscara de luz
		final_darkness.blit(self.light_mask, (0, 0), special_flags=pg.BLEND_MULT)
		
		# Desenha a escuridão final
		self.game.screen.blit(final_darkness, (0, 0))

	def game_over(self):
		self.screen.blit(self.game_over_image, (0, 0)) #coloca a imagem de game over na tela 

	"""
	A lógica do laço é a seguinte:

	1- i recebe o índice da posição atual na string (começando em 0).
	2- char recebe o valor do caractere na posição atual (ou seja, o dígito da vida do jogador).
	3- O código usa o índice i para calcular a posição x na tela onde o dígito deve ser desenhado. A posição x é calculada multiplicando o índice i pelo tamanho do dígito (self.digit_size).
	4- O código desenha o dígito correspondente ao caractere char na posição calculada usando a função blit.
	5- O laço repete esses passos para cada caractere na string health.
	"""
	def draw_player_health(self):
		health = str(self.game.player.health)
		for i, char in enumerate(health):
			self.screen.blit(self.digits[char], (i * self.digit_size, 0)) 
		self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0)) 

	def player_damage(self):
		#sobrepõe a imagem do dano na tela se o player sofrer dano
		self.screen.blit(self.blood_screen, (0, 0))


	def draw_background(self):
		self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % width
		self.screen.blit(self.sky_image, (-self.sky_offset, 0))
		self.screen.blit(self.sky_image, (-self.sky_offset + width, 0))
		pg.draw.rect(self.screen, floor_color, (0, half_height, width, height))


	"""
	1- Ordenação dos objetos: A função sorted() é usada para ordenar a lista de objetos a serem renderizados (self.game.raycasting.objects_to_render) com base na profundidade (depth) 
	de cada objeto. A ordenação é feita em ordem decrescente (reverse=True), ou seja, os objetos mais distantes (com maior profundidade) são renderizados primeiro.
	
	2- Iteração sobre os objetos ordenados: A função for é usada para iterar sobre a lista ordenada de objetos. Cada objeto é representado por uma tupla (depth, image, pos) que contém:
	depth: a profundidade do objeto
	image: a imagem do objeto a ser renderizada
	pos: a posição do objeto na tela
	
	3- Renderização dos objetos: Para cada objeto, a função blit() é usada para renderizar a imagem do objeto na tela, na posição especificada (pos).
	"""
	def render_game_objects(self):
		list_objects = sorted(self.game.raycasting.objects_to_render ,\
			key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_objects:
			self.screen.blit(image, pos)

	def create_light_mask(self):
		# Cria um gradiente circular para a lanterna
		mask = pg.Surface((width, height))
		mask.fill((0, 0, 0))
		
		# Desenha um círculo de luz no centro
		center_x, center_y = width // 2, height // 2
		radius = 200  # Alcance da lanterna
		
		for y in range(center_y - radius, center_y + radius):
			for x in range(center_x - radius, center_x + radius):
				dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
				if dist <= radius:
					alpha = min(255, int(255 * (1 - dist/radius)))
					mask.set_at((x, y), (255, 255, 255, alpha))
		
		self.light_mask = mask


	@staticmethod #Metodo estatic para nao precisar instanciar a classe
	def get_texture(path, res=(texture_size, texture_size)):
		#carrega a imagem e converte para efeito alpha
		texture = pg.image.load(path).convert_alpha()
		#converte a resolução da imagem
		return pg.transform.scale(texture, res)


	#São usados numeros para referenciar as texturas nas paredes do minimap
	def load_wall_textures(self):
		return {
			1: self.get_texture('resources/textures/1.png'),
			2: self.get_texture('resources/textures/2.png'),
			3: self.get_texture('resources/textures/3.png'),
			4: self.get_texture('resources/textures/4.png'),
			5: self.get_texture('resources/textures/5.png'),
		}
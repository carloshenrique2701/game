#link da imagem/sprite para baixar
#https://github.com/StanislavPetrovV/DOOM-style-Game/tree/main/resources/sprites/static_sprites
import pygame as pg 
from settings import * 
import os 
from collections import deque



class SpriteObject:
	def __init__(self, game, path='resources/sprites/static_sprites/candlebra.png', 
		pos=(10.5, 3.5), scale=0.7, shift=0.28):
		self.game = game 

		#personagem do jogo
		self.player = game.player
		self.x, self.y = pos

		#imagem da sprite
		self.image = pg.image.load(path).convert_alpha()
		self.image_width = self.image.get_width()
		self.image_half_width = self.image.get_width() // 2
		self.image_ratio = self.image_width / self.image.get_height()

		#variáveis de controle da sprite
		self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
		self.sprite_half_width = 0 
		self.sprite_scale = scale 
		self.sprite_height_shift = shift

	#Calcula o tamanho e a posição projetados da sprite na tela com base na sua distância do jogador e adiciona à lista de renderização do jogo.
	def get_sprite_projection(self):
		#diminui o tamanho da projeção da sprite no mapa
		proj = screen_dist / self.norm_dist * self.sprite_scale
		proj_width, proj_height = proj * self.image_ratio, proj 

		image = pg.transform.scale(self.image, (proj_width, proj_height))

		self.sprite_half_width = proj_width // 2 
		height_shift = proj_height * self.sprite_height_shift
		pos = self.screen_x - self.sprite_half_width, half_height - proj_height // 2 + height_shift

		self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

	# Calcula a posição da sprite na tela em relação ao jogador, 
	# levando em conta o ângulo e a distância do jogador. Se a sprite estiver dentro dos limites da tela, chama get_sprite_projection.
	def get_sprite(self):
		dx = self.x - self.player.x 
		dy = self.y - self.player.y 
		self.dx, self.dy = dx, dy 
		self.theta = math.atan2(dy, dx)

		delta = self.theta - self.player.angle
		if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
			delta += math.tau 

		delta_rays = delta / delta_angle
		self.screen_x = (half_num_rays + delta_rays) * scale

		#distância da sprite
		self.dist = math.hypot(dx, dy)
		#distância normal da sprite
		self.norm_dist = self.dist * math.cos(delta)

		if -self.image_half_width < self.screen_x < (width + self.image_half_width) and self.norm_dist > 0.5:
			self.get_sprite_projection()



	def update(self):
		self.get_sprite()


"""
subclasse de SpriteObject que representa uma sprite animada em um jogo. Ela carrega uma série de imagens de um diretório e as anima em um intervalo de tempo especificado.
"""
class AnimatedSprite(SpriteObject):
	def __init__(self, game, path='resources/sprites/animated_sprites/green_light/0.png',
			pos=(11.5, 3.5), scale=0.8, shift=0.15, animation_time=120):
		super().__init__(game, path, pos, scale, shift)
		self.animation_time = animation_time
		self.path = path.rsplit('/', 1)[0]
		self.images = self.get_images(self.path)
		self.animation_time_prev = pg.time.get_ticks()
		self.animation_trigger = False 


	def update(self):
		super().update()
		self.check_animation_time()
		self.animate(self.images)

	#Anima a sprite rotacionando a lista de imagens e definindo a imagem atual como a primeira da lista, mas apenas se o gatilho de animação estiver ativado.
	def animate(self, images):
		if self.animation_trigger:
			images.rotate(-1)
			self.image = images[0]

	# Verifica se é hora de animar a sprite com base no intervalo de tempo de animação e define o gatilho de animação conforme necessário.
	def check_animation_time(self):
		self.animation_trigger = False 
		time_now = pg.time.get_ticks()
		if time_now - self.animation_time_prev > self.animation_time:
			self.animation_time_prev = time_now 
			self.animation_trigger = True 

	#Carrega uma lista de imagens de um diretório especificado e as retorna como um objeto deque(já foi explicado em pathfiding).
	def get_images(self, path):
		images = deque()

		for file_name in os.listdir(path):
			if os.path.isfile(os.path.join(path, file_name)):
				img = pg.image.load(path + '/' + file_name).convert_alpha()
				images.append(img)
		return images 


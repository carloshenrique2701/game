import pygame as pg 
from settings import * 

# O que criamos nesta 4 aula
class ObjectRenderer:

	def __init__(self, game):
		self.game = game 
		self.screen = game.screen
		self.wall_textures = self.load_wall_textures()
		#parte4
		self.sky_image = self.get_texture('resources/textures/sky.png', (width, half_height))
		self.sky_offset = 0 
		#parte final - explicar - imagem que indica que o player sofreu dano
		self.blood_screen = self.get_texture('resources/textures/blood_screen.png', res)
		#parte final 
		self.digit_size = 90 
		self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
							for i in range(11)]
		self.digits = dict(zip(map(str, range(11)), self.digit_images))
		self.game_over_image = self.get_texture('resources/textures/game_over.png', res)



	#aula 4
	def draw(self):
		self.draw_background()
		self.render_game_objects()

		#parte final
		self.draw_player_health()

	#parte final
	def game_over(self):
		self.screen.blit(self.game_over_image, (0, 0))

	def draw_player_health(self):
		#parte final
		#desenha a barra de vida do player
		#e cada vez que ele recebe dano a barra de vida diminui
		health = str(self.game.player.health)
		for i, char in enumerate(health):
			self.screen.blit(self.digits[char], (i * self.digit_size, 0))
		self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

	#parte final explicar
	def player_damage(self):
		#parte final - explicar
		#sobrepõe a imagem do dano na tela se o player sofrer dano
		self.screen.blit(self.blood_screen, (0, 0))


	#aulaa4
	def draw_background(self):
		self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % width
		self.screen.blit(self.sky_image, (-self.sky_offset, 0))
		self.screen.blit(self.sky_image, (-self.sky_offset + width, 0))
		#floor 
		pg.draw.rect(self.screen, floor_color, (0, half_height, width, height))

	#aula 4
	def render_game_objects(self):
		#parte 5 - para resolver problema de visualização da sprite,
		#adicione o sorted abaixo
		list_objects = sorted(self.game.raycasting.objects_to_render ,\
			key=lambda t: t[0], reverse=True)
		for depth, image, pos in list_objects:
			self.screen.blit(image, pos)


	@staticmethod
	def get_texture(path, res=(texture_size, texture_size)):
		#carrega a imagem e converte para efeito alpha
		texture = pg.image.load(path).convert_alpha()
		#converte a resolução da imagem
		return pg.transform.scale(texture, res)


	def load_wall_textures(self):
		return {
			1: self.get_texture('resources/textures/1.png'),
			2: self.get_texture('resources/textures/2.png'),
			3: self.get_texture('resources/textures/3.png'),
			4: self.get_texture('resources/textures/4.png'),
			5: self.get_texture('resources/textures/5.png'),
		}
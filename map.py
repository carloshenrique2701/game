import pygame as pg 
from main import *
from settings import *

_ = False 
#mapa do jogo - valores digitados como 1 representará paredes e valores booleanos falsos \
#serão espaços vazios para uma melhor percepção do mapa.
mini_map = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
	#altera pra 3 e pra 2 e 4
	[1, _, _, 3, 3, 3, 3, _, _, _, 2, 2, 2, _, _, 1],
	[1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
	[1, _, _, _, _, _, 4, _, _, _, _, _, 2, _, _, 1],
	[1, _, _, 3, 3, 3, 3, _, _, _, _, _, _, _, _, 1],
	[1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
	[1, _, _, 4, _, _, _, 4, _, _, _, _, _, _, _, 1],
	[1, 1, 3, 1, 3, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1]
]


class Map:

	def __init__(self, game):
		self.game = game 
		self.mini_map = mini_map
		self.world_map = {}
		self.get_map()


	def get_map(self):
		for j, row in enumerate(self.mini_map):
			for i, value in enumerate(row):
				if value:
					self.world_map[(i, j)] = value 


	def draw(self):
		[pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100\
			, 100, 100), 2)
		for pos in self.world_map] 


		
import pygame as pg 
import sys 
from settings import * 
from map import *
from object_render import *
from raycasting import * 
from sprite_object import * 
from object_handler import *
from weapon import *
from sound import * 
from pathfinding import *
from menu import MainMenu
from player import *


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(res)
		self.clock = pg.time.Clock()
		self.delta_time = 1
		self.global_event = pg.USEREVENT + 0
		pg.time.set_timer(self.global_event, 40)

		# Configurações iniciais do mouse
		pg.mouse.set_visible(True)  # Visível no menu
		pg.event.set_grab(False)    # Mouse livre

		# Estado do jogo
		self.running = False
		self.paused = False

		# Carrega o menu primeiro
		self.menu = MainMenu(self)

	def start_game(self):
		"""Chamado quando o jogador seleciona 'Iniciar Jogo'"""
		self.new_game()
		self.running = True
		pg.mouse.set_visible(False)
		pg.event.set_grab(True)  # Agora trava o mouse para gameplay
	

	def new_game(self):
		self.map = Map(self)
		self.player = Player(self)
		# 4 aula
		self.object_renderer = ObjectRenderer(self)
		#instância a classe do raycasting aqui
		self.raycasting = RayCasting(self)
		self.object_handler = ObjectHandler(self)
		self.weapon = Weapon(self)
		self.sound = Sound(self)
		self.pathfinding = PathFinding(self) #erro
		#self.static_sprite = SpriteObject(self)
		#self.animated_sprite = AnimatedSprite(self)

	def update(self):
		self.player.update()
		self.raycasting.update()
		self.object_handler.update()
		self.weapon.update()
		#self.static_sprite.update()
		#self.animated_sprite.update()


	def draw(self):
		# Renderização normal do jogo
		self.object_renderer.draw()
		self.weapon.draw()
		
		# Sobrepõe a tela de pause se necessário
		if self.paused:
			self.draw_pause_screen()

	def draw_pause_screen(self):
		# Cria uma superfície semi-transparente
		s = pg.Surface((width, height), pg.SRCALPHA)
		s.fill((0, 0, 0, 180))  # Preto com 70% de opacidade
		self.screen.blit(s, (0, 0))
		
		# Texto de pause
		font = pg.font.Font(None, 100)
		text = font.render("PAUSED", True, (255, 255, 255))
		text_rect = text.get_rect(center=(width//2, height//2 - 50))
		self.screen.blit(text, text_rect)
		
		# Instruções
		font = pg.font.Font(None, 36)
		instructions = font.render("Press ESC to continue", True, (200, 200, 200))
		instructions_rect = instructions.get_rect(center=(width//2, height//2 + 50))
		self.screen.blit(instructions, instructions_rect)


	def check_events(self):
		self.global_trigger = False 
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.toggle_pause()
					#quando o jogador aperta escape(esc) ele pausa o jogo, porem, o codigo esta com algum erro. No momento que eu despauso se o mouse estiver a direita do centro a visão do jogador da uma bugada e vira um pouco para a esquerda. O mesmo acontece ao inverso 
			elif event.type == self.global_event:
				self.global_trigger = True 
			#tiro do player
			self.player.single_fire_event(event)

	def toggle_pause(self):
		
		if not self.running:  # Se não estiver no jogo, não pausa
			return
			
		self.paused = not self.paused
		pg.mouse.set_visible(self.paused)  # Mostra mouse apenas se pausado
		pg.event.set_grab(not self.paused)  # Trava mouse se não pausado. set_grab é usado para travar o mouse
		
		if self.paused:
			pg.mouse.get_rel()  # Limpa movimento residual ANTES de liberar
			pg.event.set_grab(False)  # Libera o mouse
			pg.mouse.set_pos([half_width, half_height])
			#self.sound.pause_sound.play()  # Opcional: som de pause
		else:
			pg.mouse.get_rel()  # Limpa movimento residual ANTES de travar
			pg.event.set_grab(True)  # Trava o mouse
        	#self.sound.unpause_sound.play()  # Adicione um som de unpause se quiser

	def run(self):
		while True:
			if not self.running:
				self.menu.handle_events()
				self.menu.draw()
			else:
				# Lógica normal do jogo
				self.check_events()	
				if not self.paused:
					self.update()
				self.draw()

			pg.display.flip()
			self.delta_time = self.clock.tick(fps)
			pg.display.set_caption(f'fps: {self.clock.get_fps() :.1f}')

#executa o game
if __name__ == "__main__":
	game = Game() #erro
	game.run()

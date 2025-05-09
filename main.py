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

		# Configurações iniciais da tela
		self.screen = pg.display.set_mode(res) 
		self.clock = pg.time.Clock() # Controle de FPS do pygame
		self.delta_time = 1

		#Atributo global_event para disparar um evento a cada 40ms(milisegundos)
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

		# Agora trava o mouse para gameplay e deixa ele invisível
		pg.mouse.set_visible(False)
		pg.event.set_grab(True)  
	
	#iniciando o jogo e declarando as instancias
	def new_game(self):
		self.map = Map(self)
		self.player = Player(self)
		self.object_renderer = ObjectRenderer(self)
		self.raycasting = RayCasting(self)
		self.object_handler = ObjectHandler(self)
		self.weapon = Weapon(self)
		self.sound = Sound(self)
		self.pathfinding = PathFinding(self)
		#self.static_sprite = SpriteObject(self)
		#self.animated_sprite = AnimatedSprite(self)

	#Desenha o jogo, se estiver pausado, chama a tela de pause
	def draw(self):
		# Renderização normal do jogo
		self.object_renderer.draw()
		self.weapon.draw()
		
		# Sobrepõe a tela de pause se necessário
		if self.paused:
			self.draw_pause_screen()

	#Desenha a tela de pause
	def draw_pause_screen(self):
		# Cria uma superfície semi-transparente
		s = pg.Surface((width, height), pg.SRCALPHA) #pega o tamanho da tela e usa o SRCALPHA para criar uma superfície semi-transparente
		s.fill((0, 0, 0, 180))  # Preto com 70% de opacidade
		self.screen.blit(s, (0, 0)) # Coloca a superfície na tela
		
		# Texto de pause
		font = pg.font.Font(None, 100)
		text = font.render("PAUSED", True, (255, 255, 255))
		text_rect = text.get_rect(center=(width//2, height//2 - 50))#posiciona o texto na tela em um retangulo
		self.screen.blit(text, text_rect)
		
		# Instruções
		font = pg.font.Font(None, 36)
		instructions = font.render("Pressione ESC to continue", True, (200, 200, 200))
		instructions_rect = instructions.get_rect(center=(width//2, height//2 + 50))#posiciona o texto na tela em um retangulo
		self.screen.blit(instructions, instructions_rect)

	#Checa os eventos que são pegos a cada 40ms
	def check_events(self):
		self.global_trigger = False #Atributo global_trigger para disparar um evento a cada 40ms
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.toggle_pause()
			elif event.type == self.global_event: #se o evento for global_event, entao global_trigger = True para que ele seja chamado na funcao run
				self.global_trigger = True 
			#tiro do player
			self.player.single_fire_event(event)

	def toggle_pause(self):
		
		if not self.running:  # Se o jogo estiver parado, retorna
			return
			
		self.paused = not self.paused 
		pg.mouse.set_visible(self.paused)  # Mostra mouse apenas se pausado
		pg.event.set_grab(not self.paused)  # Trava mouse se não pausado. set_grab é usado para travar o mouse
		
		if self.paused:
			pg.mouse.get_rel()  # Limpa movimento residual ANTES de liberar
			pg.event.set_grab(False)  # Libera o mouse
			pg.mouse.set_pos([half_width, half_height])
			#self.sound.pause_sound.play()  # som de pause
		else:
			pg.mouse.get_rel()  # Limpa movimento residual ANTES de travar
			pg.event.set_grab(True)  # Trava o mouse
        	#self.sound.unpause_sound.play()  # Adicione um som de unpause


	#Basicamente vai funcionar como um loop de atualizações constantes do jogo
	def update(self):
		self.player.update()
		self.raycasting.update()
		self.object_handler.update()
		self.weapon.update()
		#self.static_sprite.update()
		#self.animated_sprite.update()


	#Principal loop do jogo
	def run(self):
		while True:
			if not self.running:
				self.menu.handle_events()#chama o menu
				self.menu.draw()
			else:
				# Lógica normal do jogo
				self.check_events()	
				if not self.paused:
					self.update()
				self.draw()

			pg.display.flip()#atualiza a tela
			self.delta_time = self.clock.tick(fps) # Controle de FPS
			pg.display.set_caption(f'FPS: {self.clock.get_fps() :.1f}') # Mostra o FPS na tela

#executa o game
if __name__ == "__main__":
	game = Game() 
	game.run()

from settings import *
import pygame as pg 
import math 
from npc import * 
from object_handler import * 

class Player:

	def __init__(self, game):

		self.game = game 
		self.x, self.y = player_pos
		self.angle = player_angle
		#se for True, significa que o jogador atirou.
		self.shot = False 

		#vida do player - 
		self.health = player_max_health 
		self.health_recovery_delay = 700 
		self.time_prev = pg.time.get_ticks() #usado para calcular o atraso de recuperação de saúde
	
		#movimento do mouse
		self.rel = 0
		self.pitch = 0

		#Lanterna
		self.light_intensity = 10.0
		self.light_radius = 200

	def update_light(self):
		# Apenas atualiza se houver alteração significativa
		old_radius = self.light_radius
		self.light_intensity = max(0.3, self.light_intensity - 0.0001)
		new_radius = int(self.light_radius * self.light_intensity)

		if abs(new_radius - old_radius) > 1 or self.game.player.rel != 0:
			self.light_radius = new_radius
			self.game.object_renderer.light_mask = self.game.object_renderer.create_light_mask()

	"""
	Gerenciamento de Saúde

	recover_health: Recupera a saúde do jogador em 1 ponto se o atraso de recuperação de saúde tiver passado e a saúde do jogador for menor que a máxima.
	
	check_health_recovery_delay: Verifica se o atraso de recuperação de saúde tiver passado e retorna True se tiver.
	
	get_damage: Reduz a saúde do jogador por uma quantidade especificada e reproduz um efeito sonoro.
	"""
	#
	def recover_health(self):
		if self.check_health_recovery_delay() and self.health < player_max_health:
			self.health += 1 
	#
	def check_health_recovery_delay(self):
		time_now = pg.time.get_ticks()
		if time_now - self.time_prev > self.health_recovery_delay:
			self.time_prev = time_now
			return True 
	# 
	def get_damage(self, damage):
		#reduz a vida do player ao sofrer dano do inimigo
		self.health -= damage
		self.game.object_renderer.player_damage()
		self.game.sound.player_pain.play()

		#
		self.check_game_over()

	# Verifica se a saúde do jogador é menor que 1 e termina o jogo se for.
	def check_game_over(self):
		if self.health < 1:
			self.game.object_renderer.game_over()
			pg.display.flip()
			pg.time.delay(1500)
			self.game.new_game()

	#verifica se o player pressionou o mouse para atirar
	def single_fire_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1 and not self.shot and not self.game.weapon.reloading:
				self.game.sound.shotgun.play() #executa som de tiro ao atirar
				self.shot = True 
				self.game.weapon.reloading = True

	"""
	Movimento

	movement: Atualiza a posição do jogador com base na entrada do teclado e verifica colisões com paredes.

	check_wall: Verifica se uma posição dada é uma parede no mapa.

	check_wall_collision: Verifica colisões com paredes e atualiza a posição do jogador conforme necessário.
	"""
	#
	def movement(self):
		#movimento do player
		sin_a = math.sin(self.angle)
		cos_a = math.cos(self.angle)
		dx, dy = 0, 0
		speed = player_speed * self.game.delta_time
		speed_sin = speed * sin_a 
		speed_cos = speed * cos_a 

		#obtém e armazena todas as teclas pressionadas no game
		#dx e dy representam o deslocamento do player no mapa olhando de cima
		keys = pg.key.get_pressed()
		if keys[pg.K_w]:
			#vai para cima
			dx += speed_cos 
			dy += speed_sin
		if keys[pg.K_s]:
			#vai para baixo
			dx += -speed_cos
			dy += -speed_sin
		if keys[pg.K_a]:
			#vai para esquerda
			dx += speed_sin 
			dy += -speed_cos 
		if keys[pg.K_d]:
			#vai para direita
			dx += -speed_sin 
			dy += speed_cos

		#função que checa a colisão com as paredes do game
		self.check_wall_collision(dx, dy)
		self.angle %= math.tau #o angulo fica entre 0 e 2pi, evitando erros de arredondamento(overflow)
	#	
	def check_wall(self, x, y):
		return (x, y) not in self.game.map.world_map
	#
	def check_wall_collision(self, dx, dy):

		scale = player_size_scale / self.game.delta_time

		if self.check_wall(int(self.x + dx * scale), int(self.y)):
			self.x += dx 
		if self.check_wall(int(self.x), int(self.y + dy * scale)):
			self.y += dy

	#Atualiza o ângulo do jogador com base no movimento do mouse.
	def mouse_control(self):

		if self.game.paused:  # Só centraliza se o jogo não estiver pausado
			pg.mouse.get_rel()  # Descarta qualquer movimento durante o pause
			return

		if not self.game.paused:  # Só move a câmera se o jogo não estiver pausado
			mx, my = pg.mouse.get_rel()

			#movimento horizontal
			self.rel = mx
			self.angle += self.rel * mouse_sensitivity * self.game.delta_time



	#atualiza o movimento do player constantemente para que ele consiga andar
	def update(self):
		self.movement()
		self.mouse_control()
		self.recover_health()
		self.update_light()
		print(self.x, self.y)

	#Retorna a posição atual do player
	@property 
	def pos(self):
		return self.x, self.y 

	#Retorna a posição do jogador no mapa.
	@property
	def map_pos(self):
		return int(self.x), int(self.y)
	
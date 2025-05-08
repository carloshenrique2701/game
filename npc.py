from sprite_object import * 
from random import choice, random, randint 


class NPC(AnimatedSprite):
	def __init__(self, game, path='resources/sprites/npc/soldier/0.png', pos=(10.5, 5.5),
		scale=0.6, shift=0.38, animation_time=180):
		super().__init__(game, path, pos, scale, shift, animation_time)
		#obtendo imagens 
		self.attack_images = self.get_images(self.path + '/attack')
		self.death_images = self.get_images(self.path + '/death')
		self.idle_images = self.get_images(self.path + '/idle')
		self.pain_images = self.get_images(self.path + '/pain')
		self.walk_images = self.get_images(self.path + '/walk')

		#distância de ataque
		self.attack_dist = randint(3, 6)
		self.speed = 0.03 
		self.size = 10
		#vida npc
		self.health = 100 
		#dano do ataque
		self.attack_damage = 10 
		self.accuracy = 0.15 
		#se o npc está vivo
		self.alive = True 
		#se ele foi atingido
		self.pain = False 

		#parar o tiro através das paredes
		self.ray_cast_value = False
		self.frame_counter = 0
		self.player_search_trigger = None 


	def update(self):
		self.check_animation_time()
		self.get_sprite()
		#atualizar a lógica do npc
		self.run_logic()
		#self.draw_ray_cast()


	#checa onde o npc está no mapa
	def check_wall(self, x, y):
		return (x, y) not in self.game.map.world_map

	#define a colisão do npc com as paredes
	def check_wall_collision(self, dx, dy):
		#parte 4
		if self.check_wall(int(self.x + dx * self.size), int(self.y)):
			self.x += dx 
		if self.check_wall(int(self.x), int(self.y + dy * self.size)):
			self.y += dy


	def movement(self):
		next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
		next_x, next_y = next_pos

		#pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
		if next_pos not in self.game.object_handler.npc_positions:
			angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
			dx = math.cos(angle) * self.speed 
			dy = math.sin(angle) * self.speed
			self.check_wall_collision(dx, dy)


	def attack(self):
		if self.animation_trigger:
			self.game.sound.npc_shot.play()
			#parte final - explicar
			if random() < self.accuracy:
				#receber dano do jogador
				self.game.player.get_damage(self.attack_damage)


	def animate_death(self):
		if not self.alive:
			if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
				self.death_images.rotate(-1)
				self.image = self.death_images[0]
				self.frame_counter += 1


	def animate_pain(self):
		self.animate(self.pain_images)
		#checa se o npc já sentiu o disparo, se sim, paramos a animação de dor
		if self.animation_trigger:
			self.pain = False 


	def check_hit_in_npc(self):
		#checa se o player disparou no npc
		if self.ray_cast_value and self.game.player.shot:
			if half_width - self.sprite_half_width < self.screen_x < half_width + self.sprite_half_width:
				self.game.sound.npc_pain.play()
				#nesta verificação o player já atirou e o npc sentiu o disparo
				self.game.player.shot = False 
				self.pain = True 
				self.health -= self.game.weapon.damage
				self.check_health()


	def check_health(self):
		if self.health < 1:
			self.alive = False #npc morreu
			self.game.sound.npc_death.play()

	def run_logic(self):
		#toda lógica do npc, se baseia se ele está vivo ou não
		#nesta parte o inimigo/npc vai ficar inspecionando tudo ao seu redor
		if self.alive:
			self.ray_cast_value = self.ray_cast_player_npc()
			self.check_hit_in_npc()
			#se ele estiver vivo
			if self.pain:
				#se npc receber o disparo, ele sentirá
				self.animate_pain()
			elif self.ray_cast_value:
				self.player_search_trigger = True 
				if self.dist < self.attack_dist:
					self.animate(self.attack_images)
					self.attack()
				else:
					self.animate(self.walk_images)
					self.movement()
			elif self.player_search_trigger:
				self.animate(self.walk_images)
				self.movement()
			else:
				self.animate(self.idle_images)
		else:
			self.animate_death()


	@property
	def map_pos(self):
		#checa se a visão do player se encontra com a do npc
		return int(self.x), int(self.y)


	def ray_cast_player_npc(self):
		if self.game.player.map_pos == self.map_pos:
			return True 

		wall_dist_v, wall_dist_h = 0, 0 #distância parede na vertical e horizontal
		player_dist_v, player_dist_h = 0, 0

		ox, oy = self.game.player.pos
		x_map, y_map = self.game.player.map_pos

		ray_angle = self.theta #parte final
		
		sin_a = math.sin(ray_angle)
		cos_a = math.cos(ray_angle)

		# horizontais
		y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

		depth_hor = (y_hor - oy) / sin_a 
		x_hor = ox + depth_hor * cos_a

		delta_depth = dy / sin_a 
		dx = delta_depth * cos_a

		for i in range(max_depth):
			tile_hor = int(x_hor), int(y_hor)
			if tile_hor == self.map_pos:
				player_dist_h = depth_hor
				break
			if tile_hor in self.game.map.world_map:
				#aula4 - textura horizontal
				wall_dist_h = depth_hor
				break 
			x_hor += dx 
			y_hor += dy 
			depth_hor += delta_depth


			#verticais
		x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

		depth_vert = (x_vert - ox) / cos_a
		y_vert = oy + depth_vert * sin_a 

		delta_depth = dx / cos_a 
		dy = delta_depth * sin_a

		for i in range(max_depth):
			tile_vert = int(x_vert), int(y_vert)
			if tile_vert == self.map_pos:
				player_dist_v = depth_vert
				break
			if tile_vert in self.game.map.world_map:
				#aula 4 - textura vertical 
				wall_dist_v = depth_vert
				break 
			x_vert += dx
			y_vert += dy 
			depth_vert += delta_depth

		#depth 
		texture_vert = None 
		texture_hor = None 
		if depth_vert < depth_hor:
			#aula 4
			depth, texture = depth_vert, texture_vert
			y_vert %= 1
			offset = y_vert if cos_a > 0 else (1 - y_vert)
		else:	
			#aula4
			depth, texture = depth_hor, texture_hor
			x_hor %= 1 
			offset = (1 - x_hor) if sin_a > 0 else x_hor

		#remove fishbowl effect // remover efeito aquário - parte 3 
		depth *= math.cos(self.game.player.angle - ray_angle)
			#projection / projeção
		proj_height = screen_dist / (depth + 0.0001) #parte 3



		#ray casting results - aula 4
		#self.ray_casting_result.append((depth, proj_height, texture, offset))

		#ray_angle += delta_angle


		player_dist = max(player_dist_v, player_dist_h)
		wall_dist = max(wall_dist_v, wall_dist_h)

		if 0 < player_dist < wall_dist or not wall_dist:
			return True 
		return False 


	def draw_ray_cast(self):
		pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
		if self.ray_cast_player_npc():
			pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
				(100 * self.x, 100 * self.y), 2)



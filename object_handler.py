from sprite_object import * 
from npc import * 



class ObjectHandler:
	def __init__(self, game):
		self.game = game 
		self.sprite_list = []
		#parte npc
		self.npc_list = []
		self.npc_sprite_path = 'resources/sprites/npc/'
		self.static_sprite_path = 'resources/sprites/static_sprites'
		self.anim_sprite_path = 'resources/sprites/animated_sprites'
		add_sprite = self.add_sprite
		add_npc = self.add_npc #instância de classe parte npc
		self.npc_positions = {}
		#mapa onde adicionaremos sprite no jogo
		add_sprite(SpriteObject(game))
		add_sprite(AnimatedSprite(game))
		#organizar todas as sprites no mapa
		add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
		add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
		add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
		add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
		add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
		add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
		add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
		#adiciona red light 
		add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + '/red_light/0.png', pos=(14.5, 7.5)))
		add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + '/red_light/0.png', pos=(12.5, 7.5)))
		add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + '/red_light/0.png', pos=(14.5, 7.5)))

		#add_npc_map 
		#add_npc(NPC(game))
		#add_npc(NPC(game, pos=(11.5, 4.5)))
		#add_npc(NPC(game, pos=(11.5, 5.5)))
		#add_npc(NPC(game, pos=(11.5, 5.5)))
		#add_npc(NPC(game, pos=(11.7, 5.8)))
		#add_npc(NPC(game, pos=(11.9, 5.9)))
		#add_npc(NPC(game, pos=(11.8, 5.5)))



	def update(self):
		self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
		[sprite.update() for sprite in self.sprite_list]
		[npc.update() for npc in self.npc_list]

	#parte npc
	def add_npc(self, npc):
		#adiciona npc no mapa
		self.npc_list.append(npc)



	def add_sprite(self, sprite):
		#adiciona as sprites na lista vazia
		self.sprite_list.append(sprite)

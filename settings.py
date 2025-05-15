import math

#configurações do jogo

#resolução da tela e frames/segundo
res = width, height = 1300, 700
fps = 120
half_width, half_height = width // 2, height // 2 #pega o inteiro da divisão

#configurações do player e movimentação geral
player_pos = 44, 49 #Posição inicial do player
player_angle = 0 #angulo inicial
player_speed = 0.003 
player_rot_speed = 0.002 #velocidade de rotação
player_size_scale = 100 #tamanho de colisão do player com as paredes(distancia de colisão)
player_max_health = 100
player_height = 0.5

#configurações do mouse
mouse_sensitivity = 0.0001 #sensibilidade do mouse
mouse_max_rel = 40 #limite de movimento do mouse
mouse_border_left = 100 #limite da borda esquerda do mouse
mouse_border_right = width - mouse_border_left #limite da borda direita do mouse (tamanho da tela - borda esquerda)

#Para calculos de direções e colisões
fov = math.pi / 3 #campo de visão(90 graus)
half_fov = fov / 2 #metade do angulo de visão
num_rays = width // 2 #quantidade de raios que serão projetados, pegando o inteiro da divisão da largura da tela
half_num_rays = num_rays // 2 
delta_angle = fov / num_rays #angulo de visão dividido pela quantidade de raios (delta), para que os raios sejam equidistantes
max_depth = 50 #alcance dos raios para as colisões(para que as paredes carreguem adequadamente)
vertical_fov = 0 # Campo de visão vertical (45 graus)
vertical_sensitivity = mouse_sensitivity  # Sensibilidade do mouse vertical
max_pitch = math.pi / 3  # Ângulo máximo para cima/baixo (60 graus)

#cor do chao, cinza esbelto
floor_color = (150, 150, 150)

##Para calculos da projeção 3d
screen_dist = half_width / math.tan(half_fov) #tangente inversa da metade do angulo de visão para a metade da distância de tela(basicamente, serve para calcular coordenadas da projecao em relação ao player)
scale = width / num_rays #escala da projecao

#tamanho de textura e calculos
texture_size = 1256
half_texture_size = texture_size // 2 #metade do tamanho da textura

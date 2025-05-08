import math

#configurações do jogo

#resolução da tela e frames/segundo
res = width, height = 1300, 700
fps = 60
half_width, half_height = width // 2, height // 2 #pega o inteiro da divisão

#configurações do player e movimentação geral
player_pos = 1.5, 5
player_angle = 0
player_speed = 0.004
player_rot_speed = 0.002
player_size_scale = 120 #tamanho de colisão do player com as paredes
player_max_health = 100

#configurações do mouse
mouse_sensitivity = 0.0001 
mouse_max_rel = 40 #limite de movimento do mouse
mouse_border_left = 100 #limite da borda esquerda do mouse
mouse_border_right = width - mouse_border_left #limite da borda direita do mouse (tamanho da tela - borda esquerda)

#Para calculos de direções e colisões
fov = math.pi / 3 #angulo de visão
half_fov = fov / 2 #metade do angulo de visão
num_rays = width // 2 #quantidade de raios que serão projetados
half_num_rays = num_rays // 2 
delta_angle = fov / num_rays #angulo de visão dividido pela quantidade de raios (delta), para que os raios sejam equidistantes
max_depth = 50 #alcance dos raios para as colisões(para que as paredes carreguem adequadamente)

#cor do chao, verde grama
floor_color = (34, 100, 34)
#distância de tela
screen_dist = half_width / math.tan(half_fov) #tangente inversa do angulo de visão

#Para projeção 3d
scale = width / num_rays #escala da projecao

#tamanho de textura e calculos
texture_size = 256
half_texture_size = texture_size // 2 #metade do tamanho da textura

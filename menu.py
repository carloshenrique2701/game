import pygame as pg
import sys
from settings import *

class MainMenu:
    def __init__(self, game):
        self.game = game

        #Atributos de font
        self.font = pg.font.Font('fonts/titulo.ttf', 74) #Tipo de fonte e o tamanho
        self.small_font = pg.font.Font('fonts/resto.ttf', 36) #https://fonts.google.com/

        #Atributos de opções
        self.selected = 0
        self.options = ["Iniciar Jogo", "Sair"]
        
    def draw(self):
        # Fundo escuro
        self.game.screen.fill((20, 20, 20))
        
        # Título
        title = self.font.render("Sussuros do Labirinto", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width//2, height//4))
        self.game.screen.blit(title, title_rect)
        
        # Opções
        for i, option in enumerate(self.options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255) #Cores das opções
            text = self.small_font.render(option, True, color)
            rect = text.get_rect(center=(width//2, height//2 + i*50))
            self.game.screen.blit(text, rect)
        
        # Instruções
        help_text = self.small_font.render("Use MOUSE ou as setas UP e DOWN para selecionar", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(width//2, height - 100))
        self.game.screen.blit(help_text, help_rect)
    
    #Função para lidar com os eventos de teclado e mouse sobre as opçoes
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_LEFT:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pg.K_UP or event.key == pg.K_RIGHT:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
                    self.select_option()

            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                for i, option in enumerate(self.options):
                    rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.selected = i  

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.check_mouse_click()
    
    #checa se o mouse foi clicado em alguma das opções
    def check_mouse_click(self):
        mouse_pos = pg.mouse.get_pos()
        for i, _ in enumerate(self.options):
            text_rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
            if text_rect.collidepoint(mouse_pos):
                self.selected = i
                self.select_option()
    
    #valida qual opção foi selecionada
    def select_option(self):
        if self.selected == 0:  # Iniciar Jogo
            pg.mouse.get_rel()
            self.game.start_game()
        else:  # Sair
            pg.quit()
            sys.exit()
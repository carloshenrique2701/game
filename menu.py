import pygame as pg
import sys
from settings import *

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 74)
        self.small_font = pg.font.Font(None, 36)
        self.selected = 0
        self.options = ["Iniciar Jogo", "Sair"]
        
    def draw(self):
        # Fundo escuro
        self.game.screen.fill((20, 20, 20))
        
        # Título
        title = self.font.render("MEU JOGO FODA", True, (255, 255, 255))
        title_rect = title.get_rect(center=(width//2, height//4))
        self.game.screen.blit(title, title_rect)
        
        # Opções
        for i, option in enumerate(self.options):
            color = (255, 215, 0) if i == self.selected else (255, 255, 255)
            text = self.small_font.render(option, True, color)
            rect = text.get_rect(center=(width//2, height//2 + i*50))
            self.game.screen.blit(text, rect)
        
        # Instruções
        help_text = self.small_font.render("Use MOUSE ou as setas UP e DOWN para selecionar", True, (200, 200, 200))
        help_rect = help_text.get_rect(center=(width//2, height - 100))
        self.game.screen.blit(help_text, help_rect)
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pg.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pg.K_RETURN:
                    self.select_option()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.check_mouse_click()
    
    def check_mouse_click(self):
        mouse_pos = pg.mouse.get_pos()
        for i, _ in enumerate(self.options):
            text_rect = pg.Rect(width//2 - 100, height//2 + i*50 - 18, 200, 36)
            if text_rect.collidepoint(mouse_pos):
                self.selected = i
                self.select_option()
    
    def select_option(self):
        if self.selected == 0:  # Iniciar Jogo
            self.game.start_game()
        else:  # Sair
            pg.quit()
            sys.exit()
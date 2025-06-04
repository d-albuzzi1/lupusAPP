import pygame
import sys
from functools import partial

import random
import os
import time

pygame.init()

# Dimensioni dello schermo tipo telefono
WIDTH, HEIGHT = 360, 640
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lupus")

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 150, 255)
DARK_BLUE = (30, 100, 200)

# Font
FONT = pygame.font.SysFont("DejaVu Sans", 24)

# Variabili per i valori delle opzioni
value_contadini = 3
value_lupi = 3
value_guardiano = 1
value_veggente = 1
value_medium = 1
value_indemoniato = 0
value_curioso = 0

# Classe Pulsante
class Button:
    def __init__(self, x, y, w, h, text, base_color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_color = base_color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=6)

        text_surf = FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

# Classe per selettore numerico con frecce
class NumberSelector:
    def __init__(self, x, y, value_ref, name):
        self.left_btn = Button(x, y, 30, 40, "◀", WHITE, DARK_BLUE, action=self.decrease)
        self.right_btn = Button(x + 55, y, 30, 40, "▶", WHITE, DARK_BLUE, action=self.increase)
        self.value_ref = value_ref
        self.name = name
        self.x = x + 35
        self.y = y + 3

    def draw(self, surface):
        self.left_btn.draw(surface)
        self.right_btn.draw(surface)

        val = FONT.render(str(self.value_ref[0]), True, BLACK)
        val_rect = val.get_rect(center=(self.x + 5, self.y + 20))
        surface.blit(val, val_rect)

    def handle_event(self, event):
        self.left_btn.handle_event(event)
        self.right_btn.handle_event(event)

    def increase(self):
        if self.name == 'Contadini' and self.value_ref[0] < 15:
            self.value_ref[0] += 1
        if self.name == 'Lupi' and self.value_ref[0] < 5:
            self.value_ref[0] += 1
        elif self.value_ref[0] < 1:
            self.value_ref[0] += 1

    def decrease(self):
        if self.value_ref[0] > 0:
            self.value_ref[0] -= 1

# Controllo schermate
current_screen = 0
start_screen = 0
role_selection_screen = 1

def sync_role_values():
    global value_contadini, value_lupi
    value_contadini = value_contadini_ref[0]
    value_lupi = value_lupi_ref[0]

def change_screen(screen_number):
    global current_screen
    if current_screen == role_selection_screen:
        sync_role_values()
    current_screen = screen_number


# Pulsanti principali
role_sel_btn = Button(30, 200, 300, 50, "Modifica ruoli disponibili", GRAY, DARK_BLUE, 
                    action=partial(change_screen, role_selection_screen))
player_sel_btn = Button(70, 280, 220, 50, "Imposta giocatori", GRAY, DARK_BLUE, 
                    action=None)
start_btn = Button(110, 480, 140, 50, "Inizia", GRAY, DARK_BLUE, 
                    action=None)

btn_contadini = Button(40, 100, 120, 50, "Contadini", WHITE, WHITE)
btn_lupi = Button(40, 150, 120, 50, "Lupi", WHITE, WHITE)
btn_guardiano = Button(40, 200, 120, 50, "Guardiano", WHITE, WHITE)
btn_veggente = Button(40, 250, 120, 50, "Veggente", WHITE, WHITE)
btn_medium = Button(40, 300, 120, 50, "Medium", WHITE, WHITE)
btn_indemoniato = Button(40, 350, 120, 50, "Indemoniato", WHITE, WHITE)
btn_curioso = Button(40, 400, 120, 50, "Curioso", WHITE, WHITE)

next_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                    action=None)
back_btn = Button(110, 480, 140, 50, "Indietro", GRAY, DARK_BLUE, 
                    action=partial(change_screen, start_screen))

# Selettori dei ruoli 
value_contadini_ref = [value_contadini]
value_lupi_ref = [value_lupi]
value_guardiano_ref = [value_guardiano]
value_veggente_ref = [value_veggente]
value_medium_ref = [value_medium]
value_indemoniato_ref = [value_indemoniato]
value_curioso_ref = [value_curioso]

selector_contadini = NumberSelector(180, 100, value_contadini_ref, name='Contadini')
selector_lupi = NumberSelector(180, 150, value_lupi_ref, name='Lupi')
selector_guardiano = NumberSelector(180, 200, value_guardiano_ref, name='Guardiano')
selector_veggente = NumberSelector(180, 250, value_veggente_ref, name='Veggente')
selector_medium = NumberSelector(180, 300, value_medium_ref, name='Medium')
selector_indemoniato = NumberSelector(180, 350, value_indemoniato_ref, name='Indemoniato')
selector_curioso = NumberSelector(180, 400, value_curioso_ref, name='Curioso')

# Funzioni disegno schermate

def draw_start_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Benvenuti a Lupus!", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    role_sel_btn.draw(SCREEN)
    player_sel_btn.draw(SCREEN)
    start_btn.draw(SCREEN)

def draw_role_selection_screen():
    SCREEN.fill(WHITE)
    title = FONT.render("Selezione ruoli disponibili", True, BLACK)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    btn_contadini.draw(SCREEN)
    selector_contadini.draw(SCREEN)
    btn_lupi.draw(SCREEN)
    selector_lupi.draw(SCREEN)
    btn_guardiano.draw(SCREEN)
    selector_guardiano.draw(SCREEN)
    btn_veggente.draw(SCREEN)
    selector_veggente.draw(SCREEN)
    btn_medium.draw(SCREEN)
    selector_medium.draw(SCREEN)
    btn_indemoniato.draw(SCREEN)
    selector_indemoniato.draw(SCREEN)
    btn_curioso.draw(SCREEN)
    selector_curioso.draw(SCREEN)

    back_btn.draw(SCREEN)

# def draw_screen_1():
#     SCREEN.fill(WHITE)
#     title = FONT.render("Seconda schermata", True, BLACK)
#     SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
#     next_btn.draw(SCREEN)

# Main loop

clock = pygame.time.Clock()
running = True
while running:
    SCREEN.fill(WHITE)

    if current_screen == start_screen:
        draw_start_screen()
    elif current_screen == role_selection_screen:
        draw_role_selection_screen()
    else:
        end_text = FONT.render("Fine!", True, BLACK)
        SCREEN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == start_screen:
            role_sel_btn.handle_event(event)
            player_sel_btn.handle_event(event)
            start_btn.handle_event(event)

        elif current_screen == role_selection_screen:
            back_btn.handle_event(event)
            selector_contadini.handle_event(event)
            selector_lupi.handle_event(event)
            selector_guardiano.handle_event(event)
            selector_veggente.handle_event(event)
            selector_medium.handle_event(event)
            selector_indemoniato.handle_event(event)
            selector_curioso.handle_event(event)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

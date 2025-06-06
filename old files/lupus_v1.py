import pygame
import sys
from functools import partial

import random

# Avvio del gioco
print("Benvenuti a Lupus!")
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

# Classe Player
class Player:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.alive = True
        self.targeted = False
        self.protected = False
        self.just_protected = False
        self.divinated = False
        self.medium = False
        self.vote = 0
        self.vote_done = False

    def __str__(self):
        return f"{self.name} ({'Alive' if self.alive else 'Dead'}) - {self.role}"

# # player_names = ["Albu","Gabri","Marco","Chiara", "Dani", "Fede"]
# player_names = ["A", "B", "C", "D"]
# # for i in range(6):
# #     name = input(f"Inserisci il nome del giocatore {i + 1}: ")
# #     player_names.append(name)

player_names = ["A", "B", "C", "D", "E", "F"]
# players_data = [Player(name) for name in player_names]
alive_players = len(player_names)

class GroupOfCheckbox:
    def __init__(self, x, y, number):
        self.number = number
        self.value_ref = [0] * number
        self.checkbox_array = []

        for i in range(number):
            btn = Button(x, y + i * 40, 35, 35, "◯ ", WHITE, WHITE, action=partial(self.box_checked, i))
            self.checkbox_array.append(btn)

    def draw(self, surface):
        for i in range(self.number):
            label_text = self.checkbox_array[i].text[2:]  # Rimuovi ◯ o ⬤
            symbol = "⬤" if self.value_ref[i] == 1 else "◯"
            self.checkbox_array[i].text = f"{symbol} {label_text}"
            self.checkbox_array[i].draw(surface)

    def handle_event(self, event):
        for btn in self.checkbox_array:
            btn.handle_event(event)

    def box_checked(self, index):
        # Deseleziona tutte
        for i in range(self.number):
            self.value_ref[i] = 0
        # Seleziona solo quella cliccata
        self.value_ref[index] = 1
    
    def get_values(self):
        self.value_array = []
        for i in range(self.number):
            self.value_array.append(self.value_ref[i])
        return self.value_array

# Controllo schermate
current_screen = 0
start_screen = 0
role_reveal_screen = 1
night_phase_start = 2
night_phase = 3
day_phase = 4
day_phase_vote = 5
vote_outcome = 6

role_selection_screen = -1
divination_screen = -2
medium_screen = -3
game_over_screen = -5

current_player = 0
current_phase = 0

class ScreenActions:

    def __init__(self):
        global player_names
        self.player_names = player_names
        self.players = [Player(name) for name in player_names]
    
    # def get_alive_players(self):
    #     return [p for p in self.players if p.alive]

    def sync_role_values(self):
        global value_contadini, value_lupi, value_guardiano, value_veggente, value_medium, value_indemoniato, value_curioso
        value_contadini = value_contadini_ref[0]
        value_lupi = value_lupi_ref[0]
        value_guardiano = value_guardiano_ref[0]
        value_veggente = value_veggente_ref[0]
        value_medium = value_medium_ref[0]
        value_indemoniato = value_indemoniato_ref[0]
        value_curioso = value_curioso_ref[0]

    def change_screen(self, screen_number):
        global current_screen
        if current_screen == role_selection_screen:
            self.sync_role_values()
        if current_screen == divination_screen:
            self.next_player_screen()
        if current_screen == medium_screen:
            self.next_player_screen()
        
        current_screen = screen_number

    def next_screen(self):
        global current_screen, current_player, current_phase
        current_player = 0
        current_phase = 0
        current_screen += 1
    
    def next_player_screen(self):
        global current_screen, current_phase, current_player, alive_players
        # print(current_screen)
        # print(current_player)
        if current_phase == 1:
            #if current_player <  len(player_names)-1:
            if current_player <  alive_players-1:
                current_player += 1
            else:
                # print(current_player)
                current_screen += 1
                current_player = 0
        current_phase = 1 - current_phase
        self.checkbox_clear()

    def checkbox_clear(self):
        global checkbox
        for box in checkbox:
            for i in range(box.number):
                box.value_ref[i] = 0

screen_actions = ScreenActions()

# Pulsanti principali
role_sel_btn = Button(30, 200, 300, 50, "Modifica ruoli disponibili", GRAY, DARK_BLUE, 
                    action=partial(screen_actions.change_screen, role_selection_screen))
player_sel_btn = Button(70, 280, 220, 50, "Imposta giocatori", GRAY, DARK_BLUE, 
                    action=None)

btn_contadini = Button(40, 100, 120, 50, "Contadini", WHITE, WHITE)
btn_lupi = Button(40, 150, 120, 50, "Lupi", WHITE, WHITE)
btn_guardiano = Button(40, 200, 120, 50, "Guardiano", WHITE, WHITE)
btn_veggente = Button(40, 250, 120, 50, "Veggente", WHITE, WHITE)
btn_medium = Button(40, 300, 120, 50, "Medium", WHITE, WHITE)
btn_indemoniato = Button(40, 350, 120, 50, "Indemoniato", WHITE, WHITE)
btn_curioso = Button(40, 400, 120, 50, "Curioso", WHITE, WHITE)

next_screen_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                     action=partial(screen_actions.next_screen))

next_player_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                     action=partial(screen_actions.next_player_screen))

back_btn = Button(110, 480, 140, 50, "OK", GRAY, DARK_BLUE, 
                    action=partial(screen_actions.change_screen, start_screen))

start_btn = Button(90, 480, 180, 50, "Nuova partita", GRAY, DARK_BLUE, 
                    action=partial(screen_actions.change_screen, start_screen))

divination_btn = Button(100, 480, 160, 50, "Divinazione", GRAY, DARK_BLUE, 
                    # action=partial(screen_actions.divination_screen))
                    action=partial(screen_actions.change_screen, divination_screen))

medium_btn = Button(100, 480, 160, 50, "Divinazione", GRAY, DARK_BLUE, 
                    # action=partial(screen_actions.divination_screen))
                    action=partial(screen_actions.change_screen, medium_screen))

night_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                    # action=partial(screen_actions.divination_screen))
                    action=partial(screen_actions.change_screen, night_phase))

night_start_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                    # action=partial(screen_actions.divination_screen))
                    action=partial(screen_actions.change_screen, night_phase_start))

checkbox = []
for i in range(len(player_names)):
    checkbox.append(GroupOfCheckbox(40, 200, number=i+1)) # il temine i-esimo avrà i+1 caselle

# Selettori dei ruoli

value_contadini = 5
value_lupi = 1
value_guardiano = 0
value_veggente = 0
value_medium = 0
value_indemoniato = 0
value_curioso = 0

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

inactive_roles = ['Contadino', 'Indemoniato', 'Curioso']
targeted_indexes = []
protected_indexes = []
divinated_indexes = []
medium_indexes = []
voted_indexes = []

# Classe Game: Funzioni disegno schermate
# RUOLI IMPLEMENTATI: Lupo, Guardiano, Veggente, Medium, Indemoniato, Curioso
class Game:

    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.role_assigned = False
        self.round_count = 1
        self.ballot = None
        self.lynched = None
        self.game_over = False

    def assign_roles(self):
        if self.role_assigned is False:
            self.roles = []
            for i in range(0, value_contadini, 1):
                self.roles.append('Contadino')
            for i in range(0, value_lupi, 1):
                self.roles.append('Lupo')
            for i in range(0, value_guardiano, 1):
                self.roles.append('Guardiano')
            for i in range(0, value_veggente, 1):
                self.roles.append('Veggente')
            for i in range(0, value_medium, 1):
                self.roles.append('Medium')
            for i in range(0, value_indemoniato, 1):
                self.roles.append('Indemoniato')
            for i in range(0, value_curioso, 1):
                self.roles.append('Curioso')
            
            print(f"Ruoli in gioco: {self.roles}")

            roles = random.sample(self.roles, len(self.players))
            for player, role in zip(self.players, roles):
                player.role = role
            
            self.role_assigned = True

    def get_alive_players(self):
        return [p for p in self.players if p.alive]
    
    def get_dead_players(self):
        return [p for p in self.players if not p.alive]

    def draw_start_screen(self):
        global current_player, current_phase
        current_player = 0
        current_phase = 0

        SCREEN.fill(WHITE)
        title = FONT.render("Benvenuti a Lupus!", True, BLACK)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        role_sel_btn.draw(SCREEN)
        player_sel_btn.draw(SCREEN)
        next_screen_btn.draw(SCREEN)

    def draw_role_selection_screen(self):
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

    def draw_role_reveal_screen(self):
        global current_phase, current_player
        self.assign_roles()
        player = self.players[current_player]
        SCREEN.fill(WHITE)

        if current_phase == 0:
            title1 = FONT.render(f"{player.name},", True, BLACK)
            title2 = FONT.render("prosegui per", True, BLACK)
            title3 = FONT.render("vedere il tuo ruolo", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
            SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
            SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
            next_player_btn.draw(SCREEN)
        else:
            title1 = FONT.render(f"{player.name},", True, BLACK)
            title2 = FONT.render("il tuo ruolo è:", True, BLACK)
            title3 = FONT.render(f"{player.role}", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
            SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
            SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
            next_player_btn.draw(SCREEN)

    def draw_divination_screen(self):
        SCREEN.fill(WHITE)

        divinated_player = None
        for player in self.players:
            if player.divinated is True:
                divinated_player = player
                break

        title1 = FONT.render(f"{divinated_player.name}", True, BLACK)
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        if divinated_player.role == 'Lupo':
            title2 = FONT.render("è un Lupo!", True, BLACK)
        else:
            title2 = FONT.render("NON è un Lupo!", True, BLACK)
            
        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))

        night_btn.draw(SCREEN)

    def draw_medium_screen(self):
        SCREEN.fill(WHITE)

        medium_player = None
        for player in self.get_dead_players():
            if player.medium is True:
                medium_player = player
                break

        title1 = FONT.render(f"{medium_player.name}", True, BLACK)
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        if medium_player.role == 'Lupo':
            title2 = FONT.render("è un Lupo!", True, BLACK)
        else:
            title2 = FONT.render("NON è un Lupo!", True, BLACK)
            
        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))

        night_btn.draw(SCREEN)

    def draw_night_phase_start_screen(self):

        self.check_game_over()
        self.lynched = None

        SCREEN.fill(WHITE)
        title1 = FONT.render("È notte. Tutti chiudono", True, BLACK)
        title2 = FONT.render("gli occhi 30 secondi,", True, BLACK)
        title3 = FONT.render("mentre i lupi discutono", True, BLACK)
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
        SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
        next_screen_btn.draw(SCREEN)

    def draw_night_phase(self):
        global current_player, current_phase
        global targeted_indexes, protected_indexes, divinated_indexes, medium_indexes
        global alive_players

        player = self.get_alive_players()[current_player]
        alive_players = len(self.get_alive_players())

        SCREEN.fill(WHITE)

        if current_phase == 0:

            title1 = FONT.render(f"{player.name},", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
            title2 = FONT.render("clicca per proseguire", True, BLACK)
            SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))
            next_player_btn.draw(SCREEN)

        else:
            
            title1 = FONT.render(f"{player.role}", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))

            # CONTADINI, INDEMONIATO, CURIOSO
            if player.role in inactive_roles:
                if player.alive is True:
                    title3 = FONT.render("Torna a dormire", True, BLACK)
                next_player_btn.draw(SCREEN)
            
            # LUPI MANNARI
            if player.role == 'Lupo':
                if player.alive is True:
                    title1 = FONT.render("Scegli una vittima", True, BLACK)
                    SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 150))
                    
                    targets = [p for p in self.get_alive_players() if p.role != 'Lupo']
                    len_box = len(targets)-1
                    checkbox[len_box].draw(SCREEN)
                    for i, p in enumerate(targets):
                        name = FONT.render(f"{p.name}", True, BLACK)
                        SCREEN.blit(name, (90, 203 + i*42))
                    
                    targeted_indexes = checkbox[len_box].get_values()

                    for i, p in enumerate(targets):
                        if targeted_indexes[i] == 0:
                            p.targeted = False
                        elif targeted_indexes[i] == 1:
                            p.targeted = True
                next_player_btn.draw(SCREEN)

            # GUARDIANO
            if player.role == 'Guardiano':
                if player.alive is True:
                    title1 = FONT.render("Scegli chi proteggere", True, BLACK)
                    SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 150))

                    targets = [p for p in self.get_alive_players() if p.just_protected is False]
                    len_box = len(targets)-1
                    checkbox[len_box].draw(SCREEN)
                    for i, p in enumerate(targets):
                        name = FONT.render(f"{p.name}", True, BLACK)
                        SCREEN.blit(name, (90, 203 + i*42))

                    protected_indexes = checkbox[len_box].get_values()

                    for i, p in enumerate(targets):
                        if protected_indexes[i] == 0:
                            p.protected = False
                        elif protected_indexes[i] == 1:
                            p.protected = True
                next_player_btn.draw(SCREEN)

            # VEGGENTE
            if player.role == 'Veggente':
                if player.alive is True:
                    title1 = FONT.render("Scegli chi divinare", True, BLACK)
                    SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 150))

                    others = [p for p in self.get_alive_players() if p.role != 'Veggente']
                    len_box = len(others)-1
                    checkbox[len_box].draw(SCREEN)
                    for i, p in enumerate(others):
                        name = FONT.render(f"{p.name}", True, BLACK)
                        SCREEN.blit(name, (90, 203 + i*42))
                    
                    divinated_indexes = checkbox[len_box].get_values()

                    for i, p in enumerate(others):
                        if divinated_indexes[i] == 0:
                            p.divinated = False
                        elif divinated_indexes[i] == 1:
                            p.divinated = True
                    divination_btn.draw(SCREEN)

            # MEDIUM
            if player.role == 'Medium':
                if player.alive is True:
                    if self.round_count > 1 :
                        title1 = FONT.render("Scegli chi divinare", True, BLACK)
                        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 150))

                        others = [p for p in self.get_dead_players() if p.role != 'Medium']
                        len_box = len(others)-1
                        checkbox[len_box].draw(SCREEN)
                        for i, p in enumerate(others):
                            name = FONT.render(f"{p.name}", True, BLACK)
                            SCREEN.blit(name, (90, 203 + i*42))
                        
                        medium_indexes = checkbox[len_box].get_values()
                        # print(medium_indexes)

                        for i, p in enumerate(others):
                            if medium_indexes[i] == 0:
                                p.medium = False
                            elif medium_indexes[i] == 1:
                                p.medium = True

                        medium_btn.draw(SCREEN)
                    else:
                        title2 = FONT.render("Aspetta la prossima notte", True, BLACK)
                        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))
                        next_player_btn.draw(SCREEN)   

    def draw_day_phase(self):
        global alive_players
        SCREEN.fill(WHITE)
        title1 = FONT.render("È giorno.", True, BLACK)

        for player in self.players:
            if player.targeted is True:
                if player.protected is True:
                    title2 = FONT.render("Nessuno è stato ucciso", True, BLACK)
                    SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))

                else:
                    title2 = FONT.render(f"{player.name} sei morto", True, BLACK)
                    SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))
                    player.alive = False

        title3 = FONT.render("Prosegui per andare ai voti", True, BLACK)

        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 200))

        alive_players = len(self.get_alive_players())
        next_screen_btn.draw(SCREEN)

    def draw_day_phase_vote(self):

        self.check_game_over()

        global current_player, current_phase
        global alive_players
        global voted_indexes
        current_phase = 1

        SCREEN.fill(WHITE)

        alive = self.get_alive_players()
        voter = alive[current_player]

        elegible = alive
        title1 = FONT.render("Votazioni per l'eliminazione:", True, BLACK)
        
        if self.ballot is not None:
            elegible = self.ballot
            # print(elegible, self.ballot)
            title1 = FONT.render("Votazioni di ballottaggio:", True, BLACK)
            
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))

        title2 = FONT.render(f"{voter.name}, scegli chi votare:", True, BLACK)
        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))
        
        options = [p for p in elegible if p != voter]
        len_box = len(options)-1
        checkbox[len_box].draw(SCREEN)
        for i, p in enumerate(options):
            name = FONT.render(f"{p.name}", True, BLACK)
            SCREEN.blit(name, (90, 203 + i*42))
        
        voted_indexes = checkbox[len_box].get_values()

        if voter.vote_done is False:
            for i, p in enumerate(options):
                if voted_indexes[i] == 1:
                    p.vote += 1
                    voter.vote_done = True

        next_player_btn.draw(SCREEN)  

    def vote_outcome(self):
        global alive_players
        global current_player, current_screen

        SCREEN.fill(WHITE)

        max_votes = 0
        possible = []
        possible_names = []
        for p in self.players:
            # print(p.name, p.vote, max_votes)
            if p.vote > max_votes:
                max_votes = p.vote
        for p in self.players:
            if p.vote == max_votes:
                possible.append(p)
                possible_names.append(p.name) 
        # print(len(possible), possible_names)

        if len(possible) == 1: 
            lynched_name = possible[0].name
            self.lynched = lynched_name
            for p in self.players:
                if p.name == lynched_name:
                    p.alive = False

            alive_players = len(self.get_alive_players())
        else:
            self.ballot = possible
            # print(self.ballot)
            for p in self.players:
                p.vote = 0
                p.vote_done = False

            current_player = 0
            current_screen = day_phase_vote


    def draw_vote_outcome_screen(self): # DA IMPLEMENTARE: BALLOTTAGGIO SUL PAREGGIO
            
        SCREEN.fill(WHITE)

        if self.lynched is None:
            # print("chiamata")
            self.ballot = None
            self.vote_outcome()

        title1 = FONT.render(f"{self.lynched} è stato linciato!", True, BLACK)
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        
        for player in self.players:
            player.vote = 0
            player.vote_done = False
            if player.targeted is True:
                player.targeted = False
            if player.just_protected is True:
                player.just_protected = False
            if player.protected is True:
                player.protected = False
                player.just_protected = True
            if player.divinated is True:
                player.divinated = False
            if player.medium is True:
                player.medium = False

        self.round_count += 1
        night_start_btn.draw(SCREEN)

    def check_game_over(self):
        global current_screen

        wolves = [p for p in self.get_alive_players() if p.role == 'Lupo' or p.role =='Indemoniato']
        villagers = [p for p in self.get_alive_players() if p.role != 'Lupo']
        if not wolves:
            self.check_game_over = 'VITTORIA CONTADINI'
            current_screen = game_over_screen
        elif len(wolves) >= len(villagers):
            self.check_game_over = 'VITTORIA lUPI'
            current_screen = game_over_screen
        
    def draw_game_over_screen(self):
        SCREEN.fill(WHITE)
        if self.check_game_over == 'VITTORIA CONTADINI':
            title1 = FONT.render("I CONTADINI VINCONO!", True, BLACK)
        elif self.check_game_over == 'VITTORIA LUPI':
            title1 = FONT.render("I LUPI VINCONO!", True, BLACK)
        else:
            title1 = FONT.render("Error", True, BLACK)
    
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        start_btn.draw(SCREEN)

game = Game(player_names)

# Main loop
def main_loop():
    clock = pygame.time.Clock()
    running = True
    while running:
        SCREEN.fill(WHITE)

        if current_screen == start_screen:
            game.draw_start_screen()
        elif current_screen == role_selection_screen:
            game.draw_role_selection_screen()
        elif current_screen == role_reveal_screen:
            game.draw_role_reveal_screen()
        elif current_screen == night_phase_start:
            game.draw_night_phase_start_screen()
        elif current_screen == night_phase:
            game.draw_night_phase()
        elif current_screen == divination_screen:
            game.draw_divination_screen()
        elif current_screen == medium_screen:
            game.draw_medium_screen()
        elif current_screen == day_phase:
            game.draw_day_phase()
        elif current_screen == day_phase_vote:
            game.draw_day_phase_vote()
        elif current_screen == vote_outcome:
            game.draw_vote_outcome_screen()
        elif current_screen == game_over_screen:
            game.draw_game_over_screen()
        else:
            # print(current_screen)
            end_text = FONT.render("Fine!", True, BLACK)
            SCREEN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_screen == start_screen:
                role_sel_btn.handle_event(event)
                player_sel_btn.handle_event(event)
                next_screen_btn.handle_event(event)

            elif current_screen == role_selection_screen:
                back_btn.handle_event(event)
                selector_contadini.handle_event(event)
                selector_lupi.handle_event(event)
                selector_guardiano.handle_event(event)
                selector_veggente.handle_event(event)
                selector_medium.handle_event(event)
                selector_indemoniato.handle_event(event)
                selector_curioso.handle_event(event)
            
            elif current_screen == role_reveal_screen:
                next_player_btn.handle_event(event)
            
            elif current_screen == night_phase_start:
                next_screen_btn.handle_event(event)

            elif current_screen == night_phase:
                
                players = game.get_alive_players()
                player = players[current_player]
                current_player_role = player.role
                
                global targeted_indexes, protected_indexes, divinated_indexes, medium_indexes
                # print(medium_indexes, current_phase, game.round_count)
                
                handle_next = False
                handle_div = False
                handle_med = False
                if current_player_role == "Lupo" and current_phase==1:
                    for index in targeted_indexes:
                        if index == 1:
                            handle_next = True
                elif current_player_role == "Guardiano" and current_phase==1:
                    for index in protected_indexes:
                        if index == 1:
                            handle_next = True
                elif current_player_role == "Veggente" and current_phase==1:
                    for index in divinated_indexes:
                        if index == 1:
                            handle_div = True
                elif current_player_role == "Medium" and current_phase==1 and game.round_count>1:
                    # print("a")
                    for index in medium_indexes:
                        if index == 1:
                            handle_med = True
                elif current_player_role in inactive_roles or current_phase==0:
                    handle_next = True
                
                if current_player_role == "Medium" and game.round_count==1:
                    handle_next = True

                if handle_next is True: next_player_btn.handle_event(event)
                if handle_div is True:  divination_btn.handle_event(event)
                if handle_med is True: medium_btn.handle_event(event)

                # Attivo sempre tutte le checkbox, ma non è un problema, non mi vanno in conflitto, 
                # le pulisco ogni volta e salvo sempre i dati da un'altra parte
                for i in range(len(player_names)):
                    checkbox[i].handle_event(event)
            
            elif current_screen == divination_screen:
                night_btn.handle_event(event)

            elif current_screen == medium_screen:
                night_btn.handle_event(event)

            elif current_screen == day_phase:
                next_screen_btn.handle_event(event)

            elif current_screen == day_phase_vote:
                global voted_indexes

                # Attivo sempre tutte le checkbox, ma non è un problema, non mi vanno in conflitto, 
                # le pulisco ogni volta e salvo sempre i dati da un'altra parte
                for i in range(len(player_names)):
                    checkbox[i].handle_event(event)

                for index in voted_indexes:
                        if index == 1:
                            next_player_btn.handle_event(event)

            elif current_screen == vote_outcome:
                night_start_btn.handle_event(event)
            
            elif current_screen == game_over_screen:
                start_btn.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

main_loop()

pygame.quit()
sys.exit()

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

# class Checkbox:
#     def __init__(self, x, y):
#         self.value_ref = [0]  # ad es. [0]
#         self.btn = Button(x, y, 40, 40, "◯", WHITE, DARK_BLUE, action=self.box_checked)
#         # self.x = x + 40  # posizione del testo accanto
#         # self.y = y + 10

#     def draw(self, surface):
#         # Aggiorna simbolo in base allo stato attuale
#         self.btn.text = "⬤" if self.value_ref[0] == 1 else "◯"
#         self.btn.draw(surface)

#         # # Disegna etichetta accanto alla checkbox
#         # label_surf = FONT.render(self.label, True, BLACK)
#         # surface.blit(label_surf, (self.x, self.y))

#     def handle_event(self, event):
#         self.btn.handle_event(event)
    
#     def box_checked(self, surface):
#         self.value_ref[0] = 1 - self.value_ref[0]  # toggle tra 0 e 1
#         self.draw(surface)


# Classe Player
class Player:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.alive = True
        self.targeted = False
        self.protected = False
        self.just_protected = False
        self.vote = None

    def __str__(self):
        return f"{self.name} ({'Alive' if self.alive else 'Dead'}) - {self.role}"

# Avvio del gioco
print("Benvenuti a Lupus!")

# player_names = ["Albu","Gabri","Marco","Chiara", "Dani", "Fede"]
player_names = ["A", "B", "C", "D", "E"]



class GroupOfCheckbox:
    def __init__(self, x, y, number):
        self.number = number
        self.value_ref = [0] * number
        self.checkbox_array = []

        for i in range(number):
            #label = labels[i] if labels else f"Opzione {i+1}"
            btn = Button(x, y + i * 60, 200, 40, "◯ ", WHITE, DARK_BLUE, action=partial(self.box_checked, i))
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


# Controllo schermate
current_screen = 1
start_screen = 1
role_selection_screen = 0
role_reveal_screen = 2
night_phase_start = 3
night_phase = 4

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
        # global value_contadini_ref, value_lupi_ref, value_guardiano_ref, value_veggente_ref, value_medium_ref, value_indemoniato_ref, value_curioso_ref
        # print('contadini:', value_contadini, value_contadini_ref[0])
        value_contadini = value_contadini_ref[0]
        value_lupi = value_lupi_ref[0]
        value_guardiano = value_guardiano_ref[0]
        value_veggente = value_veggente_ref[0]
        value_medium = value_medium_ref[0]
        value_indemoniato = value_indemoniato_ref[0]
        value_curioso = value_curioso_ref[0]

        # print('contadini:', value_contadini, value_contadini_ref[0])

    def change_screen(self, screen_number):
        global current_screen
        if current_screen == role_selection_screen:
            self.sync_role_values()
        current_screen = screen_number

    def next_screen(self):
        global current_screen #, value_contadini
        # print('contadini:', value_contadini, value_contadini_ref[0])
        current_screen += 1
    
    def next_player_screen(self):
        global current_screen, current_phase, current_player
        # print(current_player, len(player_names)) 
        if current_phase == 1:
            if current_player <  len(player_names)-1:
                current_player += 1
            else:
                print(current_player)
                current_screen += 1
                current_player = 0
        current_phase = 1 - current_phase


screen_actions = ScreenActions()

# Pulsanti principali
role_sel_btn = Button(30, 200, 300, 50, "Modifica ruoli disponibili", GRAY, DARK_BLUE, 
                    action=partial(screen_actions.change_screen, role_selection_screen))
player_sel_btn = Button(70, 280, 220, 50, "Imposta giocatori", GRAY, DARK_BLUE, 
                    action=None)
# start_btn = Button(110, 480, 140, 50, "Inizia", GRAY, DARK_BLUE, action=None)

btn_contadini = Button(40, 100, 120, 50, "Contadini", WHITE, WHITE)
btn_lupi = Button(40, 150, 120, 50, "Lupi", WHITE, WHITE)
btn_guardiano = Button(40, 200, 120, 50, "Guardiano", WHITE, WHITE)
btn_veggente = Button(40, 250, 120, 50, "Veggente", WHITE, WHITE)
btn_medium = Button(40, 300, 120, 50, "Medium", WHITE, WHITE)
btn_indemoniato = Button(40, 350, 120, 50, "Indemoniato", WHITE, WHITE)
btn_curioso = Button(40, 400, 120, 50, "Curioso", WHITE, WHITE)

# next_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, action=None)

next_screen_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                     action=partial(screen_actions.next_screen))

next_player_btn = Button(110, 480, 140, 50, "Avanti", GRAY, DARK_BLUE, 
                     action=partial(screen_actions.next_player_screen))

back_btn = Button(110, 480, 140, 50, "OK", GRAY, DARK_BLUE, 
                    action=partial(screen_actions.change_screen, start_screen))

# Selettori dei ruoli
# starting_values = [3, 3, 1, 1, 1, 0, 0] # contadini, lupi, guardiano. veggente, medium, indemoniato, curioso

value_contadini = 4
value_lupi = 1
value_guardiano = 0
value_veggente = 0
value_medium = 0
value_indemoniato = 0
value_curioso = 0

# value_ref = []*len(starting_values)
# for i in range(len(starting_values)):
#     value_ref[i] = [starting_values[i]]

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



# Classe Game: Funzioni disegno schermate
class Game:

    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.role_assigned = False

        # RUOLI IMPLEMENTATI: Lupo, Guardiano, Veggente, Medium, Indemoniato, Curioso
        # self.roles = ['Lupo', 'Lupo', 'Veggente', 'Guardiano', 'Medium', 'Contadino']
        # self.roles = ['Lupo', 'Lupo', 'Veggente', 'Guardiano', 'Contadino', 'Contadino']
        # self.roles = ['Lupo', 'Medium', 'Contadino']

        # self.roles = []
        # for i in range(0, value_contadini, 1):
        #     self.roles.append('Contadino')
        # for i in range(0, value_lupi, 1):
        #     self.roles.append('Lupo')
        # for i in range(0, value_guardiano, 1):
        #     self.roles.append('Guardiano')
        # for i in range(0, value_veggente, 1):
        #     self.roles.append('Veggente')
        # for i in range(0, value_medium, 1):
        #     self.roles.append('Medium')
        # for i in range(0, value_indemoniato, 1):
        #     self.roles.append('Indemoniato')
        # for i in range(0, value_curioso, 1):
        #     self.roles.append('Curioso')
        
        # print(f"Ruoli in gioco: {self.roles}")
        # self.assign_roles()

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
            # self.assign_roles()

            roles = random.sample(self.roles, len(self.players))
            for player, role in zip(self.players, roles):
                player.role = role
            
            self.role_assigned = True

    def get_alive_players(self):
        return [p for p in self.players if p.alive]
    
    def get_dead_players(self):
        return [p for p in self.players if not p.alive]

    def draw_start_screen(self):
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
            # current_phase =+ 1
            title1 = FONT.render(f"{player.name},", True, BLACK)
            title2 = FONT.render("prosegui per", True, BLACK)
            title3 = FONT.render("vedere il tuo ruolo", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
            SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
            SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
            next_player_btn.draw(SCREEN)
        else:
            # current_phase = 0
            title1 = FONT.render(f"{player.name},", True, BLACK)
            title2 = FONT.render("il tuo ruolo è:", True, BLACK)
            title3 = FONT.render(f"{player.role}", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
            SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
            SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
            next_player_btn.draw(SCREEN)

    def draw_night_phase_start_screen(self):
        SCREEN.fill(WHITE)
        title1 = FONT.render("Tutti chiudono gli", True, BLACK)
        title2 = FONT.render("occhi 30 sec, mentre", True, BLACK)
        title3 = FONT.render("i lupi discutono", True, BLACK)
        SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
        SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 135))
        SCREEN.blit(title3, (WIDTH // 2 - title3.get_width() // 2, 170))
        next_screen_btn.draw(SCREEN)

    def draw_night_phase(self):
        global current_player
        player = self.players[current_player]
        SCREEN.fill(WHITE)

        global current_phase

        if current_phase == 0:

            title = FONT.render(f"{player.name}, clicca per proseguire", True, BLACK)
            SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
            next_player_btn.draw(SCREEN)

        else:
            
            title1 = FONT.render(f"{player.name}, il tuo ruolo è: {player.role}", True, BLACK)
            SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))

            # CONTADINI, INDEMONIATO, CURIOSO
            inactive_roles = ['Contadino', 'Indemoniato', 'Curioso']
            if player.role in inactive_roles:
                if player.alive is True:
                    title2 = FONT.render("Torna a dormire", True, BLACK)
                else:
                    title2 = FONT.render("Ormai dormi per sempre", True, BLACK)
                SCREEN.blit(title2, (WIDTH // 2 - title2.get_width() // 2, 150))

            # LUPI MANNARI
            if player.role == 'Lupo':
                if player.alive is True:
                    title1 = FONT.render("Scegli una vittima", True, BLACK)
                    SCREEN.blit(title1, (WIDTH // 2 - title1.get_width() // 2, 100))
                    
                    targets = [p for p in self.get_alive_players() if p.role != 'Lupo']
                    targets_name = []*len(targets)
                    
                    targets_status = GroupOfCheckbox(40, 150, number=len(targets))
                    for i, p in enumerate(targets):
                        # print(f"{i+1}. {p.name}")
                        targets_name[i] = Button(90, 150 + i*20, 120, 50, f"{p.name}", WHITE, WHITE)



                    # SALVARE IL TARGETED!!!!!!!!!!!!

                    victim = targets[index]
                    victim.targeted = True
                else:
                    print("Sei morto. Le tue vittime verranno a prenderti")
                os.system('cls' if os.name == 'nt' else 'clear')

            # GUARDIANO
            if player.role == 'Guardiano':
                if player.alive is True:
                    print("Guardiano, scegli chi vuoi proteggere")
                    targets = [p for p in self.get_alive_players() if p.just_protected is False]
                    for i, p in enumerate(targets):
                        print(f"{i+1}. {p.name}")
                    try:
                        index = int(input("Inserisci il numero del giocatore da proteggere: "))
                        index -= 1
                    except:
                        print("Input non valido, verrà scelto in automatico il primo")
                        index = 0
                    safe_player = targets[index]
                    safe_player.protected = True
                else:
                    print('Sei morto, proteggi i fantasmi')
                    time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')

            # VEGGENTE
            if player.role == 'Veggente':
                if player.alive is True:
                    print("Veggente, scegli un giocatore da scoprire:")
                    others = [p for p in self.get_alive_players() if p.role != 'Veggente']
                    for i, p in enumerate(others):
                        print(f"{i+1}. {p.name}")
                    choice = int(input("Numero del giocatore da scrutare: "))
                    choice -= 1
                    # print(f"{others[choice].name} è un {others[choice].role}")
                    if others[choice].role == "Lupo":
                        print(f"{others[choice].name} è un Lupo")
                    else:
                        print(f"{others[choice].name} NON è un Lupo")
                else:
                    print("Sei morto")
                time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')

            # MEDIUM
            if player.role == 'Medium':
                if player.alive is True:
                    if round_count > 1 :
                        others = [p for p in self.get_dead_players() if p.role != 'Medium']
                        print("Medium, scegli un giocatore da scoprire:")
                        for i, p in enumerate(others):
                            print(f"{i+1}. {p.name}")
                        choice = int(input("Numero del giocatore da scrutare: "))
                        choice -= 1
                        # print(f"{others[choice].name} è un {others[choice].role}")
                        if others[choice].role == "Lupo":
                            print(f"{others[choice].name} è un Lupo")
                        else:
                            print(f"{others[choice].name} NON è un Lupo")
                    else:
                        print("Vai al bar e aspetta la prossima notte")
                else:
                    print("Sei morto")
                time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')



    def day_phase(self, round_count):
        print("\n--- GIORNO ---")

        for player in self.get_alive_players():
            if player.targeted is True:
                if player.protected is True:
                    print("Nessuno è stato ucciso nella notte")
                else:
                    print(f"Purtroppo {player.name} non ha superato la notte")
                    player.alive = False

        input("Discussione tra i giocatori... premi INVIO per proseguire")
        # time.sleep(5)
        print("\nÈ ora di votare per il linciaggio.")
        votes = {}
        alive = self.get_alive_players()
        for voter in alive:
            print(f"\n{voter.name}, scegli chi votare:")
            options = [p for p in alive if p != voter]
            for i, p in enumerate(options):
                print(f"{i}. {p.name}")
            choice = int(input("Numero del giocatore da votare: "))
            voted = options[choice]
            votes[voted.name] = votes.get(voted.name, 0) + 1

        # Determina chi ha più voti
        max_votes = max(votes.values())
        possible = [name for name, count in votes.items() if count == max_votes]
        lynched_name = random.choice(possible)
        for p in self.players:
            if p.name == lynched_name:
                p.alive = False
                print(f"{lynched_name} è stato linciato!")
                break
        
        for player in self.get_alive_players():
            if player.targeted is True:
                player.targeted = False
            if player.protected is True:
                player.protected = False
                player.just_protected = True

    def check_game_over(self):
        wolves = [p for p in self.get_alive_players() if p.role == 'Lupo' or p.role =='Indemoniato']
        villagers = [p for p in self.get_alive_players() if p.role != 'Lupo']
        if not wolves:
            print("\nI CONTADINI VINCONO!")
            return True
        elif len(wolves) >= len(villagers):
            print("\nI LUPI MANNARI VINCONO!")
            return True
        return False

    def play(self):
        round_count = 1
        while not self.check_game_over():
            print(f"\n======= ROUND {round_count} =======")
            self.night_phase(round_count)
            if self.check_game_over():
                break
            self.day_phase(round_count)
            if self.check_game_over():
                break
            round_count += 1












# # Avvio del gioco
# print("Benvenuti a Lupus!")

# # player_names = ["Albu","Gabri","Marco","Chiara", "Dani", "Fede"]
# player_names = ["A", "B", "C"]
# # for i in range(6):
# #     name = input(f"Inserisci il nome del giocatore {i + 1}: ")
# #     player_names.append(name)

game = Game(player_names)
# game.play()




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
        else:
            print(current_screen)
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
                next_player_btn.handle_event(event)

        pygame.display.flip()
        clock.tick(60)







main_loop()

pygame.quit()
sys.exit()

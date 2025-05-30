import random
import os
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.role = None
        self.alive = True
        self.targeted = False
        self.protected = False
        self.vote = None

    def __str__(self):
        return f"{self.name} ({'Alive' if self.alive else 'Dead'}) - {self.role}"


class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.roles = ['Lupo Mannaro', 'Villico', 'Veggente', 'Guardiano', 'Villico', 'Villico']
        self.assign_roles()

    def assign_roles(self):
        roles = random.sample(self.roles, len(self.players))
        for player, role in zip(self.players, roles):
            player.role = role
            input(f"{player.name}, premi INVIO per vedere il tuo ruolo. (Assicurati che nessuno guardi!)")
            print(f"Il tuo ruolo è: {role}")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')

    def get_alive_players(self):
        return [p for p in self.players if p.alive]

    def night_phase(self):
        print("\n--- NOTTE ---")

        for player in self.players:
            input(f"{player.name}, premi INVIO per proseguire. (Assicurati che nessuno guardi!)")
            print(f"Il tuo ruolo è: {player.role}")

            if player.role == 'Villico':
                if player.alive is True:
                    try:
                        index = int(input("Torna a dormire. Premi un numero per proseguire :"))
                    except :
                        print("Attendi")
                else:
                    print("Ormai dormi per sempre")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')

            if player.role == 'Lupo Mannaro':
                print("Lupi, scegliete la vittima. (Parlate tra di voi, poi uno solo inserisca)")
                targets = [p for p in self.get_alive_players() if p.role != 'Lupo Mannaro']
                for i, p in enumerate(targets):
                    print(f"{i}. {p.name}")
                try:
                    index = int(input("Inserisci il numero del giocatore da uccidere: "))
                except:
                    print("Input non valido, verrà scelto in automatico lo 0")
                    index = 0
                victim = targets[index]
                victim.targeted = True
                os.system('cls' if os.name == 'nt' else 'clear')

            if player.role == 'Guardiano':
                if player.alive is True:
                    print("Guardiano, scegli chi vuoi proteggere")
                    targets = [p for p in self.get_alive_players()]
                    for i, p in enumerate(targets):
                        print(f"{i}. {p.name}")
                    try:
                        index = int(input("Inserisci il numero del giocatore da proteggere: "))
                    except:
                        print("Input non valido, verrà scelto in automatico lo 0")
                        index = 0
                    safe_player = targets[index]
                    safe_player.protected = True
                else:
                    print('Sei morto, proteggi i fantasmi')
                    time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')

            if player.role == 'Veggente':
                if player.alive is True:
                    print("Veggente, scegli un giocatore da scoprire:")
                    others = [p for p in self.get_alive_players() if p.role != 'Veggente']
                    for i, p in enumerate(others):
                        print(f"{i}. {p.name}")
                    choice = int(input("Numero del giocatore da scrutare: "))
                    # print(f"{others[choice].name} è un {others[choice].role}")
                    if p.role == "Lupo Mannaro":
                        print(f"{others[choice].name} è un Lupo Mannaro")
                    else:
                        print(f"{others[choice].name} NON è un Lupo Mannaro")
                else:
                    print("Sei morto, sai già tutto")
                time.sleep(3)
                os.system('cls' if os.name == 'nt' else 'clear')


            # time.sleep(3)
            # os.system('cls' if os.name == 'nt' else 'clear')

        # # Lupi scelgono la vittima
        # wolves = [p for p in self.get_alive_players() if p.role == 'Lupo Mannaro']
        # if wolves:
        #     print("Lupi, scegliete la vittima. (Parlate tra di voi, poi uno solo inserisca)")
        #     targets = [p for p in self.get_alive_players() if p.role != 'Werewolf']
        #     for i, p in enumerate(targets):
        #         print(f"{i}. {p.name}")
        #     index = int(input("Inserisci il numero del giocatore da uccidere: "))
        #     victim = targets[index]
        #     victim.targeted = True
        #     os.system('cls' if os.name == 'nt' else 'clear')

        # # Guardiano
        # guard = [p for p in self.get_alive_players() if p.role == 'Guardiano']
        # if guard:
        #     print("Guardiano, scegli chi vuoi proteggere")
        #     targets = [p for p in self.get_alive_players() if p.role != 'Guardiano']
        #     for i, p in enumerate(targets):
        #         print(f"{i}. {p.name}")
        #     index = int(input("Inserisci il numero del giocatore da proteggere: "))
        #     safe_player = targets[index]
        #     safe_player.protected = True
        #     os.system('cls' if os.name == 'nt' else 'clear')

        # # Veggente vede un ruolo
        # seers = [p for p in self.get_alive_players() if p.role == 'Veggente']
        # seer = seers[0]
        # print(f"\n{seer.name} (Veggente), scegli un giocatore da scoprire:")
        # others = [p for p in self.get_alive_players() if p != seer]
        # for i, p in enumerate(others):
        #     print(f"{i}. {p.name}")
        # choice = int(input("Numero del giocatore da scrutare: "))
        # if seer-alive is True:
        #     print(f"{others[choice].name} è un {others[choice].role}")
        # else:
        #     print("Sei morto, sai già tutto")
        # time.sleep(3)
        # os.system('cls' if os.name == 'nt' else 'clear')

    def day_phase(self):
        print("\n--- GIORNO ---")

        for player in self.get_alive_players():
            if player.targeted is True:
                if player.protected is True:
                    print("Nessuno è stato ucciso nella notte")
                else:
                    print(f"Purtroppo \n{player.name} non ha superato la notte")
                    player.alive = False
               
                player.targeted = False
                player.protected = False

        # potential_victim = [p for p in self.get_alive_players() if p.targeted is True]
        # potential_victim = potential_victim[0]
        # safe_player = [p for p in self.get_alive_players() if p.protected is True]
        
        # safe_player = safe_player[0]

        # if potential_victim != safe_player:
        #     print(f"Purtroppo \n{potential_victim.name} non ha superato la notte")
        #     potential_victim.alive = False
        # else:
        #     print("Nessuno è stato ucciso nella notte")
        
        # # for player in potential_victim:
        # #     player.targeted = False
        # # for player in safe_player:
        # #     player.protected = False

        # potential_victim.targeted = False
        # safe_player.protected = False

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

    def check_game_over(self):
        wolves = [p for p in self.get_alive_players() if p.role == 'Lupo Mannaro']
        villagers = [p for p in self.get_alive_players() if p.role != 'Lupo Mannaro']
        if not wolves:
            print("\nI VILLAGGIATORI VINCONO!")
            return True
        elif len(wolves) >= len(villagers):
            print("\nI LUPI MANNARI VINCONO!")
            return True
        return False

    def play(self):
        round_count = 1
        while not self.check_game_over():
            print(f"\n======= ROUND {round_count} =======")
            self.night_phase()
            if self.check_game_over():
                break
            self.day_phase()
            round_count += 1


# Avvio del gioco
print("Benvenuti a Lupus!")
player_names = ["Albu","Dani","Gabri","Marco","Chiara","Fede"]
"""
for i in range(6):
    name = input(f"Inserisci il nome del giocatore {i + 1}: ")
    player_names.append(name)
"""

game = Game(player_names)
game.play()

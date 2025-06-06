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
        self.just_protected = False
        self.vote = None

    def __str__(self):
        return f"{self.name} ({'Alive' if self.alive else 'Dead'}) - {self.role}"


class Game:

    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        # RUOLI IMPLEMENTATI: Lupo, Guardiano, Veggente, Medium, Indemoniato, Curioso
        # self.roles = ['Lupo', 'Lupo', 'Veggente', 'Guardiano', 'Medium', 'Contadino']
        # self.roles = ['Lupo', 'Lupo', 'Veggente', 'Guardiano', 'Contadino', 'Contadino']
        self.roles = ['Lupo', 'Medium', 'Contadino']
        print(f"Ruoli in gioco: {self.roles}")
        self.assign_roles()

    def assign_roles(self):
        roles = random.sample(self.roles, len(self.players))
        for player, role in zip(self.players, roles):
            player.role = role
            input(f"{player.name}, premi INVIO per vedere il tuo ruolo. (Assicurati che nessuno guardi!)")
            print(f"Il tuo ruolo è: {role}")
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else 'clear')

    def get_alive_players(self):
        return [p for p in self.players if p.alive]
    
    def get_dead_players(self):
        return [p for p in self.players if not p.alive]

    def night_phase(self, round_count):
        print("\n--- NOTTE ---")
        print('Tutti chiudano gli occhi, mentre i lupi discutono su chi uccidere')

        for player in self.players:
            input(f"{player.name}, premi INVIO per proseguire. (Assicurati che nessuno guardi!)")
            print(f"Il tuo ruolo è: {player.role}")

            # CONTADINI, INDEMONIATO, CURIOSO
            inactive_roles = ['Contadino', 'Indemoniato', 'Curioso']
            if player.role in inactive_roles:
                if player.alive is True:
                    try:
                        index = int(input("Torna a dormire. Premi un numero per proseguire :"))
                    except :
                        print("Attendi")
                else:
                    print("Ormai dormi per sempre")
                time.sleep(2)
                os.system('cls' if os.name == 'nt' else 'clear')

            # LUPI MANNARI
            if player.role == 'Lupo':
                if player.alive is True:
                    print("Lupi, scegliete la vittima. (Parlate tra di voi, poi uno solo inserisca)")
                    targets = [p for p in self.get_alive_players() if p.role != 'Lupo']
                    for i, p in enumerate(targets):
                        print(f"{i+1}. {p.name}")
                    try:
                        index = int(input("Inserisci il numero del giocatore da uccidere: "))
                        index -= 1
                    except:
                        print("Input non valido, verrà scelto in automatico il primo")
                        index = 0
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
            
            # # CUPIDO
            # if player.role == 'Cupido':
            #     if player.alive is True:
            #         if round_count == 1 :
            #             others = [p for p in self.get_alive_players()]
            #             print("Cupido, scegli due giocatore da travolgere con la forza dell'amore:")
            #             for i, p in enumerate(others):
            #                 print(f"{i+1}. {p.name}")
            #             lover1 = int(input("Numero del giocatore da scrutare: "))
            #             lover1 -= 1
            #             lover2 = int(input("Numero del giocatore da scrutare: "))
            #             lover2 -= 1
                        
            #         else:
            #             print("Hai già diffuso l'amore")
            #     else:
            #         print("Sei morto")
            #     time.sleep(3)
            #     os.system('cls' if os.name == 'nt' else 'clear')

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


# Avvio del gioco
print("Benvenuti a Lupus!")

# player_names = ["Albu","Gabri","Marco","Chiara", "Dani", "Fede"]
player_names = ["A", "B", "C"]
# for i in range(6):
#     name = input(f"Inserisci il nome del giocatore {i + 1}: ")
#     player_names.append(name)

game = Game(player_names)
game.play()

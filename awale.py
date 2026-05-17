import sys
                 
# Ça dégagera plus tard, mais pour l'instant 
RED     = "\033[91m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
GREY    = "\033[90m"
RESET   = "\033[0m"
GREEN   = "\033[32m"
BOLD    = "\033[1m"

MAX_SEEDS = 48

class AwaleBoard():
    def __init__(self):
        self._board = []
        self._captured = [0,0] # ROUGE - BLEU
        for i in range(12):
            self._board.append(4)

    # Différents getters & setters
    def getBoard(self) -> list:
        """Retourne une copie du plateau (pas le plateau directement, pour éviter les modifications externes)"""
        return self._board.copy()

    def getSeeds(self, index: int) -> int:
        """Retourne le nombre de graines dans la case donnée"""
        return self._board[index]

    def getCapturedRed(self) -> int:
        """Retourne le nombre de graines capturées par le joueur rouge"""
        return self._captured[0]

    def getCapturedBlue(self) -> int:
        """Retourne le nombre de graines capturées par le joueur bleu"""
        return self._captured[1]

    def getCaptured(self, player: str) -> int:
        """Retourne le nombre de graines capturées par le joueur donné"""
        return self._captured[0] if player == "red" else self._captured[1]

    def getBoardSize(self) -> int:
        """Retourne la taille du plateau"""
        return len(self._board)


    # Vu les règles du jeu, je me suis dit que ça serait intéressant 
    # d'avoir cette fonction, histoire de pas se tromper lors des 
    # opérations sur les cases
    def checkValidBoard(self):
        total = 0
        for i in range(len(self._board)):
            total += self._board[i]
        total += self._captured[0]
        total += self._captured[1]

        validBoard = (total == MAX_SEEDS)
        return total, validBoard

    # Pour débugger, j'adore les fstrings de python mais là 
    # j'ai fait une abomination mdr
    def printBoard(self):
        total, isValid = self.checkValidBoard()
        print("| ",end="")
        for i in range(len(self._board)):
            print(f"{RED if i < 6 else BLUE}{self._board[i]}{RESET}",end=" ")
        print(f"| {RED}{self._captured[0]}{RESET} - {BLUE}{self._captured[1]}{RESET} |",end="")
        print(f" {GREEN}{'✔' if isValid else '✕'}{RESET} - {BOLD}{total}{RESET} |",end="")

    # On vérifie que le.a joueur.euse actuel.le a le droit 
    # de faire tel ou tel move
    def isValid(self, hollowSpot: int, turn: str) -> bool:
        """
            On va partir de la convention rouge/bleue pour 
            différentier les joueurs.es. Plus simple
        """
        if turn == "red" and 0 <= hollowSpot <= 5:
            return self._board[hollowSpot] > 0
        elif turn == "blue" and 6 <= hollowSpot <= 11:
            return self._board[hollowSpot] > 0
        return False
 
    # Logique pour bien faire le move donné, en prenant
    # en compte le.a joueur.euse actuel.le & les opés à
    # faire sur les cases
    def makeMove(self, hollowSpot: int, turn: str):
        # Le compteur est incrémenté afin d'avoir la somme des graînes dedans
        count = self._board[hollowSpot]
        self._board[hollowSpot] = 0
        fillSpot = (hollowSpot + 1) % 12

        # Pour expliquer un peu ça : à chaque ajout de graîne sur le plateau,
        # on va en retirer une au compteur
        while count > 0:
            if fillSpot != hollowSpot:
                self._board[fillSpot] += 1
                count -= 1
            fillSpot = (fillSpot + 1) % 12

        # capture — inchangé
        for i in range(len(self._board)):
            if self._board[i] == 2 or self._board[i] == 3:
                if turn == "red" and i > 5:
                    self._captured[0] += self._board[i]
                    self._board[i] = 0
                elif turn == "blue" and i < 6:
                    self._captured[1] += self._board[i]
                    self._board[i] = 0

        total, validity = self.checkValidBoard()
        if not validity:
            raise Exception(f"État non valide : {total} graines trouvées là où nous devrions en avoir {MAX_SEEDS}")

    # Là on implémente la détection de fin de partie/victoire... J'avais zappé 
    # ce détail, oups que des parties infinies ˶•𐃷•˶
    def checkWin(self) -> str | None:
        """
            Retourne 'red', 'blue', ou 'nope' selon qui a gagné ou égalité, et None si la partie n'est pas finie
        """
        if self._captured[0] >= 25:
            return "red"
        if self._captured[1] >= 25:
            return "blue"
            
        red_can_play  = any(self._board[i] > 0 for i in range(6))
        blue_can_play = any(self._board[i] > 0 for i in range(6, 12))
        
        if not red_can_play or not blue_can_play:
            # On implémente le don de graînes si applicable
            for i in range(6):
                self._captured[1] += self._board[i]
                self._board[i] = 0
            for i in range(6,12): 
                self._captured[0] += self._board[i]
                self._board[i] = 0
            
            if self._captured[0] > self._captured[1]:
                return "red"
            elif self._captured[0] < self._captured[1]:
                return "blue"
            else:
                return "nope"

        # Et on continue la partie si aucune des (nombreuses) conditions n'a été remplie
        return None


# Board = AwaleBoard().printBoard()

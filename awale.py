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
        count = self._board[hollowSpot]
        self._board[hollowSpot] = 0
        fillSpot = hollowSpot + 1
        while count > 0:
            if fillSpot == 12:
                fillSpot = 0
            if fillSpot != hollowSpot:
                self._board[fillSpot] += 1
                count -= 1
            fillSpot += 1

            total, validity = self.checkValidBoard()
            # Erreur si l'état n'est pas valide
            if not validity:
                raise Exception(f"État non valide : {total} graines trouvées là où nous devrions en avoir {MAX_SEEDS}")


# Board = AwaleBoard().printBoard()

import sys
                 
# Ça dégagera plus tard, mais pour l'instant 
RED     = "\033[91m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
GREY    = "\033[90m"
RESET   = "\033[0m"
GREEN   = "\033[32m"
BOLD    = "\033[1m"

class AwaleBoard():
    def __init__(self):
        self._board = []
        self._captured = [0,0]
        for i in range(12):
            self._board.append(4)

    # Vu les règles du jeu, je me suis dit que ça serait intéressant d'avoir cett fonction, histoire de pas se tromper lors des opérations sur les cases
    def checkValidBoard(self):
        total = 0
        for i in range(len(self._board)):
            total += self._board[i]
        total += self._captured[0]
        total += self._captured[1]

        validBoard = (total == 48)
        return total, validBoard

    def printBoard(self):
        total, isValid = self.checkValidBoard()
        print("| ",end="")
        for i in range(len(self._board)):
            print(f"{RED if i < 6 else BLUE}{self._board[i]}{RESET}",end=" ")
        print(f"| {RED}{self._captured[0]}{RESET} - {BLUE}{self._captured[1]}{RESET} |",end="")
        print(f" {GREEN}{'✔' if isValid else '✕'}{RESET} - {BOLD}{total}{RESET} |",end="")





Board = AwaleBoard().printBoard()

import pygame
from awale import AwaleBoard

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 60

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
GREEN = (50, 200, 50)
GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)
BROWN = (139, 90, 43)
LIGHT_BROWN = (205, 133, 63)

# Dimensions du plateau
CELL_SIZE = 100
CELL_MARGIN = 10
BOARD_X = 50
BOARD_Y = 100

def get_clicked_cell(mousePos: tuple) -> int | None:
    x, y = mousePos
    for i in range(12):
        row = 0 if i < 6 else 1
        col = i if i < 6 else 11 - i
        cx = BOARD_X + col * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2
        cy = BOARD_Y + row * (CELL_SIZE + CELL_MARGIN) + CELL_SIZE // 2
        if abs(x - cx) < CELL_SIZE // 2 and abs(y - cy) < CELL_SIZE // 2:
            return i
    return None

def draw_board(screen, board: AwaleBoard, font, small_font, turn:str):
    # Fond du plateau
    pygame.draw.rect(
        screen, BROWN,
        (BOARD_X - 10, BOARD_Y - 10, 6 * (CELL_SIZE + CELL_MARGIN) + 30, 2 * (CELL_SIZE + CELL_MARGIN) + 20),
        border_radius=15
    )

    for i in range(12):
        # Ligne 0 = joueur rouge (cases 0-5), Ligne 1 = joueur bleu (cases 6-11)
        row = 0 if i < 6 else 1
        col = i if i < 6 else 11 - i

        x = BOARD_X + col * (CELL_SIZE + CELL_MARGIN)
        y = BOARD_Y + row * (CELL_SIZE + CELL_MARGIN)

        # Dessin de la case (ellipses parce que faut faire un truc joli quand même !)
        pygame.draw.ellipse(screen, LIGHT_BROWN, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.ellipse(screen, DARK_GREY, (x, y, CELL_SIZE, CELL_SIZE), 2)

        # Nombre de graines
        color = RED if i < 6 else BLUE
        seed_text = font.render(str(board.getSeeds(i)), True, color)
        text_rect = seed_text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
        screen.blit(seed_text, text_rect)

        # Numéro de la case (on cachera ça hors dev)
        index_text = small_font.render(f"{i}", True, DARK_GREY)
        screen.blit(index_text, (x - 20, y + 5))

    # Petit check de validité du tableau (au cas où pour plus tard dans le développement)
    total, is_valid = board.checkValidBoard()

    red_score = font.render(f"Rouge : {board.getCapturedRed()}", True, RED)
    blue_score = font.render(f"Bleu  : {board.getCapturedBlue()}", True, BLUE)
    validity_text = small_font.render(
        f"Total : {total} {'✔' if is_valid else '✕'}",
        True, GREEN if is_valid else (255, 0, 0)
    )
    title_text = font.render(
            "Awale - Camille PRADO & Thomas SCHALLER",
            True, 
            BLUE
            )
    # Affichage du tour en cours, pour pas avoir à afficher ça dans le terminal
    turn_text = font.render(f"Tour : {'Rouge' if turn == 'red' else 'Bleu'}", True, RED if turn == "red" else BLUE)
    screen.blit(turn_text, (BOARD_X + 300, WINDOW_HEIGHT - 60))


    screen.blit(red_score, (BOARD_X, WINDOW_HEIGHT - 60))
    screen.blit(blue_score, (BOARD_X + 200, WINDOW_HEIGHT - 60))
    screen.blit(validity_text, (BOARD_X + 450, WINDOW_HEIGHT - 60))
    screen.blit(title_text, (0,0))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Awalé - 3AINT")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 32, bold=True)
    small_font = pygame.font.SysFont("monospace", 16)

    board = AwaleBoard()
    
    current_turn = "red"   # ← avant le while
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                index = get_clicked_cell(event.pos)
                if index is not None and board.isValid(index, current_turn):
                    board.makeMove(index, current_turn)
                    current_turn = "blue" if current_turn == "red" else "red"

        screen.fill(WHITE)
        draw_board(screen, board, font, small_font, current_turn)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

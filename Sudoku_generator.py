import pygame
import numpy as np
import random

# Tamaño de la ventana de Pygame
WINDOW_SIZE = 500
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

def generate_sudoku():
    # Creamos un tablero vacío de 9x9
    sudoku = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    
    # Llenamos las celdas diagonales de 1 a 9 (asegura que el Sudoku sea válido)
    for i in range(0, GRID_SIZE, 3):
        fill_diagonal(sudoku, i, i)
    
    # Resolvemos el Sudoku generado para obtener una solución única
    solve_sudoku(sudoku)
    
    # Eliminamos algunos números para crear un Sudoku para resolver
    remove_numbers(sudoku)
    
    return sudoku

def fill_diagonal(sudoku, row, col):
    nums = list(range(1, GRID_SIZE + 1))
    random.shuffle(nums)
    for i in range(3):
        for j in range(3):
            sudoku[row + i][col + j] = nums.pop()

def is_safe(sudoku, row, col, num):
    return (
        is_safe_row(sudoku, row, num) and
        is_safe_col(sudoku, col, num) and
        is_safe_box(sudoku, row - row % 3, col - col % 3, num)
    )

def is_safe_row(sudoku, row, num):
    return num not in sudoku[row]

def is_safe_col(sudoku, col, num):
    return num not in sudoku[:, col]

def is_safe_box(sudoku, start_row, start_col, num):
    return num not in sudoku[start_row:start_row + 3, start_col:start_col + 3]

def find_empty_cell(sudoku):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if sudoku[row][col] == 0:
                return (row, col)
    return None

def solve_sudoku(sudoku):
    empty_cell = find_empty_cell(sudoku)
    if not empty_cell:
        return True

    row, col = empty_cell
    for num in range(1, GRID_SIZE + 1):
        if is_safe(sudoku, row, col, num):
            sudoku[row][col] = num
            if solve_sudoku(sudoku):
                return True
            sudoku[row][col] = 0

    return False

def remove_numbers(sudoku):
    # Número máximo de celdas para eliminar mientras se mantiene una solución única
    max_cells_to_remove = random.randint(20, 30)
    cells_to_remove = set(range(GRID_SIZE**2))

    while len(cells_to_remove) > max_cells_to_remove:
        cell = random.choice(list(cells_to_remove))
        row, col = cell // GRID_SIZE, cell % GRID_SIZE
        value = sudoku[row][col]
        sudoku[row][col] = 0

        # Verificar si la solución es única después de eliminar el número
        temp_sudoku = sudoku.copy()
        count_solutions = [0]
        if solve_sudoku(temp_sudoku):
            count_solutions[0] += 1

        if count_solutions[0] != 1:
            sudoku[row][col] = value
        else:
            cells_to_remove.remove(cell)

def draw_grid(window, sudoku):
    for i in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(window, BLACK, (0, i), (WINDOW_SIZE, i), 2)
        pygame.draw.line(window, BLACK, (i, 0), (i, WINDOW_SIZE), 2)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = sudoku[row][col]
            if num != 0:
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                draw_text(window, str(num), x, y)

def draw_text(window, text, x, y):
    font = pygame.font.Font(None, 40)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    window.blit(text_surface, text_rect)

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Sudoku Generator")

    sudoku = generate_sudoku()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(WHITE)
        draw_grid(window, sudoku)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

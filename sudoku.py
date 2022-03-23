import time
from selenium import webdriver
import pyautogui as pg


#inserta la solucion en la pagina web
def upload_solution(sudoku):
    for row in sudoku:
        for ele in row:
            pg.press(str(ele))
            pg.press("right")
        pg.press("down")
        pg.press("left", presses=8)


#abre y lee el sudoku de la pagina
def read_page(dif="hard"):
    driver = webdriver.Firefox()
    url = "https://www.nytimes.com/puzzles/sudoku/" + dif
    print("Leyendo SUDOKU desde {}".format(url))
    driver.get(url)
    time.sleep(2)
    sudoku_dict = {}
    grid = driver.find_element_by_class_name("su-board")
    for el in grid.find_elements_by_tag_name("div"):
        cell = el.get_attribute("data-cell")
        val = el.get_attribute("aria-label")
        if cell is None or val is None:
            continue
        sudoku_dict[int(cell)] = 0 if val == "empty" else int(val)
    sudoku= []
    x = y = 0
    for i in range(81):
        if x == 9:
            y += 1
            x = 0
        if x == 0:
            sudoku.append([])
        sudoku[y].append(sudoku_dict[i])
        x += 1
    return sudoku

#abusque ne que coordena se encuentra la casilla
def find_coordinate(val):
    if val <= 2:
        return 0
    elif val <= 5:
        return 1
    else:
        return 2

#toma la celda y regresa el arreglo del sector
def get_cell(x, y, sudoku):
    subgrid_col = find_coordinate(x)
    subgrid_fil = find_coordinate(y)
    grid = []
    for fil in sudoku[subgrid_fil * 3: subgrid_fil * 3 + 3]:
        for col in fil[subgrid_col * 3: subgrid_col * 3 + 3]:
            grid.append(col)
    return grid

#verifica si el numero es posible en esa casiila
def possible(x, y, number, sudoku):
    # revisar la fila
    if number in sudoku[y]:
        return False
    # revisar la columna
    col = [fila[x] for fila in sudoku]
    if number in col:
        return False
    # resivar sub grid 3x3
    grid3x3 = get_cell(x, y, sudoku)
    if number in grid3x3:
        return False
    return True

#Imprime el sudoku
def print_sudoku(sudoku):
    for l in sudoku:
        print(l)
    print("\n")

#resuleve el sudoku
def resolve_sudoku(sudoku):
    for y in range(9):
        for x in range(9):
            cell = sudoku[y][x]
            if cell == 0:
                for number in range(1, 10):
                    if possible(x, y, number, sudoku):
                        sudoku[y][x] = number
                        solution = resolve_sudoku(sudoku)
                        if solution:
                            return True
                        sudoku[y][x] = 0
                return False
    print_sudoku(sudoku)
    return True


sudoku = read_page()
resolved = resolve_sudoku(sudoku)
if resolved:
    print("solucion encontrada")
    print_sudoku(sudoku)
    upload_solution(sudoku)
else:
    print("No encontre solucion")

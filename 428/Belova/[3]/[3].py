import random
from collections import deque
from heapq import heappop, heappush

#считывает файл
maze_file = 'maze-for-u.txt'
def read_maze():
    y_max=0
    maze=[]
    with open('maze-for-u.txt') as maze2:
        for line in maze2:
           maze.append(line.strip('\n'))
        width, height = len(maze[0]), len(maze)
    return width, height, maze

def read(filename): 
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.strip()
            maze.append(list(row))
    return maze

#ставим ключ
def set_coord(coord, sign):
    global maze_list
    #Преобразовывает строку в список
    maze_row = list(maze_list[coord[1]])
    maze_row[coord[0]] = sign
    maze_list[coord[1]] = ''.join(maze_row)

#проверка спавна ключа вне стены
def outside_the_wall(maze, coord):
    if maze[coord[1]][coord[0]] == '#':
        return False
    return True

#Жадный поиск
def greedy_search(maze, start_coord_coord, goal): 
    queue = deque([(start_coord_coord, [])])
    visited = set()

    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path + [current]
        visited.add(current)
        row, col = current
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        neighbors = sorted(neighbors, key=lambda neighbor: abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1]),)

        for neighbor in neighbors:
            n_row, n_col = neighbor
            if ( 0 <= n_row < len(maze) and 0 <= n_col < len(maze[0]) and maze[n_row][n_col] != "#" and neighbor not in visited):
                queue.append((neighbor, path + [current]))
    return None

#A*
def key_search(maze, start_coord, goal, g_weight, h_weight, max_steps): 
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    queue = [(heuristic(start_coord, goal), 0, start_coord, [])]
    visited = set()
    while queue:
        _, cost, current, path = heappop(queue)
        if current == goal:
            return path + [current]
        visited.add(current)
        row, col = current
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if ( 0 <= n_row < len(maze) and 0 <= n_col < len(maze[0]) and maze[n_row][n_col] != "#" and neighbor not in visited):
                new_cost = cost + 1
                priority = new_cost * g_weight + heuristic(neighbor, goal) * h_weight
                if priority <= max_steps:
                    heappush(queue, (priority, new_cost, neighbor, path + [current]))
    return None

#отмечаем путь в лабиринте
def mark(maze, path, symbol): 
    marked_maze = [row.copy() for row in maze]
    for position in path:
        row, col = position
        marked_maze[row][col] = symbol
    return marked_maze

#######################################################################################

#читаем файл
width, height, maze = read_maze()
maze_list = list(maze)
maze = read(maze_file)

#выход и вход
start_coord = (0, 1)
end_coord = (599, 798)
print("Координаты входа:", start_coord)
print("Координаты выхода:", end_coord)

#выбираем рандомом координаты для ключа и отмечаем его на карте
key_is_here = ()
while(not (key_is_here and outside_the_wall(maze, key_is_here))):
    x = random.randint(0,600) 
    y = random.randint(0,800)
    key_is_here = (abs(x) if abs(x) < width-1 else width-1, abs(y) if abs(y) < height-1 else height-1)
set_coord(key_is_here, '*')
print("Координаты ключа:", key_is_here)

#используем жадный алгоритм и отмечаем путь точками
greedy_path = greedy_search(maze, start_coord, key_is_here)
if greedy_path:
    print("Длина пути от входа до ключа:", len(greedy_path))
marked_maze = mark(maze, greedy_path, ".")

#Используем алгоритм А* и отмечаем путь запятыми
g_weight = 1 
h_weight = 1  
max_steps = 1500  
a_star_path = key_search(maze, key_is_here, end_coord, g_weight, h_weight, max_steps)
if a_star_path:
    print("Длина пути от ключа до выхода:", len(a_star_path))
    marked_maze = mark(marked_maze, a_star_path, ",")

#сохраняем файл
marked_combined_maze_file = "maze-for-me-done.txt" 
with open(marked_combined_maze_file, "w") as file:
    for row in marked_maze:
        file.write("".join(row) + "\n")

print("Выход найден!")
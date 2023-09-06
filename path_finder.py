import curses
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]


def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", BLUE)

            else:
                stdscr.addstr(i, j * 2, value, RED)


def find_start(maze, start):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == start:
                return i, j
    return None


def find_path(maze, stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze, start)

    q = queue.Queue()
    q.put((start_pos, [
        start_pos]))  ##the reason of adding two elements is to track the current element and the node we want to proccess next in queue

    visited = set()  ##will contain the path we have already visited

    while not q.empty():
        current_pos, path = q.get()  ##current_pos will give the current position and path will give the second element
        row, col = current_pos  ##breaking down the current postion in row and col so that we can visit all of the neighbors of these rows and colomns

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)
        stdscr.refresh()

        if maze[row][col] == end:
            return path

        neighbors = find_neighbors(maze, row,
                                   col)  # checking the neighbors is a obstacle or not and also it is previously visited or not
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            r, c = neighbor
            if maze[r][c] == "#":
                continue

            new_path = path + [
                neighbor]  # new path is wherever the current path is and the neighbor of the current path

            q.put((neighbor, new_path))
            visited.add(neighbor)


def find_neighbors(maze, row,
                   col):  ##we have to be very carefull here as obstacle will be on the way as we go searching for neighbor
    neighbors = []

    if row > 0:  # go UP
        neighbors.append((row - 1, col))

    if row + 1 < len(maze):  # go Down
        neighbors.append((row + 1, col))

    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
    find_path(maze, stdscr)

    stdscr.getch()


wrapper(main)  ###initializes the cursor module for us
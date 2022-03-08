# This is the CodeChallege6 solution
# Functional requirements
# Given an NxM grid, where each cell in the grid can be empty (0) or an obstacle (-1), find and display the shortest path between two arbitrary cells. The grid can be populated randomly with obstacles, or alternately a list of predefined obstacles can be placed in the grid. "Display the shortest path" can mean whatever you want it to mean: just dump the path coordinates, or plot the path on a grid, or whatever.
# Assume you have an imaginary robot that always has a cardinal orientation N, E, S, W, and that can move forward by one cell, or rotate 90 degrees to the left or right. If the robot starts in an arbitrary cell with arbitrary orientation, find the shortest path from that robot to a different arbitrary cell (the ending orientation of the robot is unimportant). Display the path in the form of a list of RELATIVE direction commands: L (left), R (right), F (forward). This is probably easiest to implement using the path generated in step 1.
# Given the path found in step 2, reverse the path.
import random
from collections import deque

GRID_X = 10
GRID_Y = 10

EMPTY_GRID = 0
OBSTACLE = 1   # Used 1 instead of -1 so my grid looks good when it prints out...


def generate_random_grid(n: int, m: int):
    choice_list = [EMPTY_GRID, EMPTY_GRID, OBSTACLE, EMPTY_GRID, EMPTY_GRID]
    random_grid = []
    for x in range(n):
        temp = []
        for y in range(m):
            temp.append(random.choice(choice_list))
        random_grid.append(temp)
    return random_grid


def print_grid(grid_to_print: []):
    for row in grid_to_print:
        print(row)


# does not have any error correction if you ask for too many points, or if there are not enough empty points to return
def select_random_points(in_grid: [], number_of_points: int):
    # random point must not be selecting an obstacle
    point_list = [divmod(i, GRID_Y) for i in random.sample(range(GRID_X * GRID_Y), number_of_points)]
    for p in point_list:
        if in_grid[p[0]][p[1]] == OBSTACLE:
            point_list = select_random_points(in_grid, number_of_points)
            break
    return point_list


class Node:
    # (x, y) represents coordinates of a cell in the matrix maintain a parent node for the printing path
    def __init__(self, x: int, y: int, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def __repr__(self):
        return str((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def is_valid_move(grid: [], x: int, y: int):
    return (0 <= x < GRID_X) and (0 <= y < GRID_Y) and (grid[x][y] == EMPTY_GRID)


# attempting a breadth-first search...
def find_path(grid: [], start_x: int, start_y: int, stop_x: int, stop_y: int):
    # base case
    if not grid or not len(grid):
        return

    allowed_movement_row = [-1, 0, 0, 1]
    allowed_movement_col = [0, -1, 1, 0]

    # create a queue and enqueue the first node
    q = deque()
    start = Node(start_x, start_y)
    q.append(start)

    # set to check if the matrix cell is visited before or not
    visited = set()

    key = (start.x, start.y)
    visited.add(key)

    # loop till queue is empty
    while q:
        # dequeue front node and process it
        curr = q.popleft()
        i = curr.x
        j = curr.y

        # return if the destination is found
        if i == stop_x and j == stop_y:
            path = []
            get_path(curr, path)
            return path

        # check all four possible movements from the current cell and for each valid movement
        for k in range(len(allowed_movement_row)):
            x = i + allowed_movement_row[k]
            y = j + allowed_movement_col[k]

            # check if it is possible to go to the next position from the current position
            if is_valid_move(grid, x, y):
                # construct the next cell node
                next = Node(x, y, curr)
                key = (next.x, next.y)

                # if it isn't visited yet
                if key not in visited:
                    # enqueue it and mark it as visited
                    q.append(next)
                    visited.add(key)

    # return None if the path is not possible
    return


# recursive function to get the path to stopping point
def get_path(node: Node, path: []):
    if node:
        get_path(node.parent, path)
        path.append(node)

if __name__ == '__main__':
    grid = generate_random_grid(GRID_X, GRID_Y)
    print_grid(grid)
    point_list = select_random_points(grid, 2)
    start_point = point_list[0]
    stop_point = point_list[1]
    print('start = ' + str(start_point))
    print('stop = ' + str(stop_point))
    path = find_path(grid, start_point[0], start_point[1], stop_point[0], stop_point[1])
    print('Solution:')
    if path:
        print(path)
    else:
        print('Path the destination is not possible')


from maze import MAZE, ROWS, COLS


# Heuristic function to estimate cost from current position to the goal
def manhattan_distance(point_a, point_b):
    #Calculate the Manhattan distance between two points on a grid.
    #Manhattan distance is to estimate how far two points are from each other on a grid
    #This distance is the sum of horizontal and vertical moves needed.

      #1     #2    #(1,2)
    row_a, col_a = point_a
      #2     #3    #(2,3)
    row_b, col_b = point_b
    return abs(row_a - row_b) + abs(col_a - col_b)


# Function to get all walkable neighbor cells (up, down, left, right)
def get_walkable_neighbors(current_cell):
    #Find all neighboring cells of current_cell that can be walked on.
    #Args:
        #current_cell (tuple): (row, col) of the current position
    #Returns:
        #list of tuples: Each tuple is a walkable neighboring cell (row, col)
                                # 2,1
    current_row, current_col = current_cell
    neighbors_list = []

    # Possible directions to move: left, right, down, rup
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
           #-1           #0           #-1,0
    for row_offset, col_offset in directions:
             #1            #2           #-1
        neighbor_row = current_row + row_offset
             #1             #1           #0
        neighbor_col = current_col + col_offset

        # Check if neighbor is inside the maze boundaries
        if 0 <= neighbor_row < ROWS and 0 <= neighbor_col < COLS:
            # Check if the neighbor cell/Actual value is 0 then it is an empty path
            if MAZE[neighbor_row][neighbor_col] == 0:
                neighbors_list.append((neighbor_row, neighbor_col))

    return neighbors_list


# A* algorithm to find the shortest path from start to goal in a maze
def a_star(start, goal):
    # List of cells to check: (priority, cost_so_far, current_cell)
    toBeExplored = [(manhattan_distance(start, goal), 0, start)]

    # Track how we got to each cell
    came_from = {start: None}
    # Track cost to reach each cell
    cost_so_far = {start: 0}

    while toBeExplored:
        # Pick cell with lowest total estimated cost
        toBeExplored.sort()
        x, cost, current = toBeExplored.pop(0)

        # Goal reached, build path
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Reverse path

        # Check neighbors of the current cell
        for neighbor in get_walkable_neighbors(current):
            new_cost = cost + 1  # Assume each move costs 1

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + manhattan_distance(neighbor, goal)
                toBeExplored.append((priority, new_cost, neighbor))
                came_from[neighbor] = current

    # No path found
    return []


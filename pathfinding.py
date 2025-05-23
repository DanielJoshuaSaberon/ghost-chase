from maze import MAZE, ROWS, COLS


# Heuristic function to estimate cost from current position to the goal
def manhattan_distance(point_a, point_b):
    #Calculate the Manhattan distance between two points on a grid.
    #Manhattan distance is to estimate how far two points are from each other on a grid
    #This distance is the sum of horizontal and vertical moves needed.

      #4     #1    #(4,1)
    row_a, col_a = point_a
      #6     #3    #(6,3)
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
    # Frontier: list of cells to explore, each as (priority = cost + heuristic, cost so far, cell)
    toBeExplored = [(manhattan_distance(start, goal), 0, start)]

    # Dictionary to track the path: which cell each visited cell came from
    # For the start cell, no previous cell, so value is None
    came_from = {start: None}

    # Dictionary to track the cost (distance) to reach each visited cell from start
    # Cost to reach start is zero
    cost_so_far = {start: 0}

    while toBeExplored:
        # Sort frontier by priority (lowest first), then pick the best candidate
        toBeExplored.sort()
        x, cost, current = toBeExplored.pop(0)

        # If current cell is the goal, reconstruct and return the path
        if current == goal:
            path = []
            while current:
                path.append(current)           # Add current cell to path
                current = came_from[current]   # Move to previous cell
            return path[::-1]  # Reverse path to get start -> goal order

        # Explore each walkable neighbor of the current cell
        for neighbor in get_walkable_neighbors(current):
            new_cost = cost + 1  # Cost to move to neighbor (assumed to be 1)

            # If neighbor is not visited or a cheaper path is found
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost  # Update cost to reach neighbor

                # Calculate priority = cost so far + heuristic estimate to goal
                priority = new_cost + manhattan_distance(neighbor, goal)

                # Add neighbor to frontier to be explored later
                toBeExplored.append((priority, new_cost, neighbor))

                # Record that we reached neighbor from current
                came_from[neighbor] = current


    # No path found
    return []


from maze import MAZE, ROWS, COLS

def heuristic(a, b):
    """
    Heuristic function for A* pathfinding:
    Returns an estimate of distance from node a to node b.
    Here we use Manhattan distance, which works for grid movement.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(node):
    """
    Returns a list of adjacent walkable tiles for a given grid node.
    Only up, down, left, right neighbors are considered (no diagonals).
    Checks boundaries and walls.
    """
    row, col = node
    results = []

    # Possible movements: up, down, left, right
    for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
        r, c = row + dr, col + dc

        # Check if inside grid bounds
        if 0 <= r < ROWS and 0 <= c < COLS:
            # Check if tile is not a wall (0 means empty)
            if MAZE[r][c] == 0:
                results.append((r, c))

    return results

def a_star(start, goal):
    """
    Implementation of the A* search algorithm.
    Finds shortest path from start to goal tile.

    Returns a list of nodes (row, col) from start to goal,
    or an empty list if no path is found.
    """

    # frontier is a list of tuples: (priority, cost_so_far, node)
    # priority = cost_so_far + heuristic estimate to goal
    frontier = []
    frontier.append((heuristic(start, goal), 0, start))

    came_from = {start: None}  # Dictionary to reconstruct path backward
    cost_so_far = {start: 0}   # Cost from start to each node

    while frontier:
        # Sort frontier by priority and pop the lowest priority item
        frontier.sort()
        _, cost, current = frontier.pop(0)

        # Check if reached the goal
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        # Explore neighbors of current node
        for next_node in neighbors(current):
            new_cost = cost_so_far[current] + 1  # Each step costs 1
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                priority = new_cost + heuristic(next_node, goal)
                frontier.append((priority, new_cost, next_node))
                came_from[next_node] = current

    # Return empty list if no path is found
    return []

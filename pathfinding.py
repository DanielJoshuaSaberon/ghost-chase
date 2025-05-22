from maze import MAZE, ROWS, COLS
from collections import deque


# Heuristic function for A* (Manhattan distance)
def heuristic(a, b):
    # Calculate the Manhattan distance between points a and b
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Returns walkable neighboring cells of a given node
def neighbors(node):
    row, col = node
    results = []
    # Check up, down, left, right neighbors
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        r, c = row + dr, col + dc
        # Check if neighbor is inside maze boundaries
        if 0 <= r < ROWS and 0 <= c < COLS:
            # Check if neighbor cell is walkable (0 means empty)
            if MAZE[r][c] == 0:
                results.append((r, c))
    return results


# A* pathfinding algorithm implementation
def a_star(start, goal):
    # frontier holds tuples of (priority, cost_so_far, node)
    frontier = []
    frontier.append((heuristic(start, goal), 0, start))

    # Dictionaries to track path and costs
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        # Sort frontier to get the node with lowest priority (f = g + h)
        frontier.sort()
        _, cost, current = frontier.pop(0)

        # If reached goal, reconstruct path and return it
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()  # Reverse path from start to goal
            return path

        # Explore neighbors
        for next_node in neighbors(current):
            new_cost = cost_so_far[current] + 1  # Cost to move to neighbor (assumed 1)
            # If neighbor is not visited or found a cheaper path
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                # Calculate priority = cost_so_far + heuristic (estimated distance)
                priority = new_cost + heuristic(next_node, goal)
                frontier.append((priority, new_cost, next_node))
                came_from[next_node] = current

    # No path found
    return []


# Breadth-First Search algorithm implementation (for comparison/testing)
def bfs(start, goal):
    queue = deque([start])  # FIFO queue for BFS
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        # If reached goal, reconstruct path and return
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        # Visit all unvisited neighbors
        for next_node in neighbors(current):
            if next_node not in came_from:
                came_from[next_node] = current
                queue.append(next_node)

    # No path found
    return []


# Selector function to choose which algorithm to use
def find_path(start, goal, algorithm="a_star"):
    if algorithm == "a_star":
        return a_star(start, goal)
    elif algorithm == "bfs":
        return bfs(start, goal)
    else:
        # Raise error if unknown algorithm requested
        raise ValueError(f"Unknown algorithm: {algorithm}")

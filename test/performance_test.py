import time
import tracemalloc
import psutil
import os
from pathfinding import a_star
from maze import MAZE, ROWS, COLS

def measure_computation_time(start, goal, iterations=100):
    """
    Measures the average time taken by the A* algorithm to find a path
    from 'start' to 'goal' over a specified number of iterations.

    Args:
        start (tuple): Starting coordinate (row, col).
        goal (tuple): Goal coordinate (row, col).
        iterations (int): Number of times to run the test to average time.

    Returns:
        float: Average computation time in milliseconds.
        list: The last path found by A* (list of coordinates).
    """
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()  # Start high precision timer
        path = a_star(start, goal)         # Run the A* pathfinding algorithm
        end_time = time.perf_counter()    # Stop timer after completion
        total_time += (end_time - start_time)  # Accumulate total elapsed time

    avg_time_ms = (total_time / iterations) * 1000  # Convert average time to milliseconds
    return avg_time_ms, path


def check_path_optimality(path, start, goal):
    """
    Validates the optimality of the found path by comparing its length
    to the expected Manhattan distance between start and goal.

    Args:
        path (list): List of coordinates representing the path.
        start (tuple): Starting coordinate (row, col).
        goal (tuple): Goal coordinate (row, col).

    Returns:
        bool: True if path length equals Manhattan distance + 1 (inclusive), False otherwise.
    """
    if not path:
        return False  # No path found means path is not optimal

    # Calculate Manhattan distance (minimum steps in a grid without obstacles)
    expected_length = abs(start[0] - goal[0]) + abs(start[1] - goal[1]) + 1
    # Path is optimal if its length equals the Manhattan distance plus 1 (including start node)
    return len(path) == expected_length


def measure_resource_utilization(start, goal):
    """
    Measures the CPU and memory usage during a single run of the A* algorithm.

    Uses 'tracemalloc' to track memory allocations and 'psutil' to measure CPU usage percentage.

    Args:
        start (tuple): Starting coordinate (row, col).
        goal (tuple): Goal coordinate (row, col).

    Returns:
        float: Approximate CPU usage percentage during the run.
        float: Current memory usage in kilobytes.
        float: Peak memory usage in kilobytes during the run.
        list: The path found by A* (list of coordinates).
    """
    tracemalloc.start()                     # Begin memory allocation tracking
    process = psutil.Process(os.getpid())  # Get process handle for CPU measurement

    cpu_before = process.cpu_percent(interval=None)  # CPU usage before pathfinding

    path = a_star(start, goal)              # Execute pathfinding algorithm

    cpu_after = process.cpu_percent(interval=0.1)   # Measure CPU usage shortly after

    current_mem, peak_mem = tracemalloc.get_traced_memory()  # Get memory usage stats

    tracemalloc.stop()                      # Stop memory tracking

    # Calculate approximate CPU usage during pathfinding run
    cpu_usage = cpu_after - cpu_before

    # Convert memory usage from bytes to kilobytes for readability
    mem_usage_kb = current_mem / 1024
    peak_mem_kb = peak_mem / 1024

    return cpu_usage, mem_usage_kb, peak_mem_kb, path


def get_start_goal(rows, cols):
    """
    Returns predefined start and goal coordinates based on maze size.

    Args:
        rows (int): Number of rows in the maze.
        cols (int): Number of columns in the maze.

    Returns:
        tuple: Start coordinate (row, col).
        tuple: Goal coordinate (row, col).
    """
    # Customize start/goal positions based on maze dimensions
    if rows == 10 and cols == 10:
        return (1, 1), (8, 8)
    elif rows == 15 and cols == 15:
        return (1, 1), (13, 13)
    elif rows == 20 and cols == 20:
        return (1, 1), (18, 18)
    else:
        # Default positions for unknown maze sizes
        return (1, 1), (rows - 2, cols - 2)


def run_tests():
    """
    Runs all performance tests on the A* algorithm for the current maze size.
    Prints average computation time, path optimality, CPU usage, and memory usage.
    """
    # Get start and goal positions dynamically based on maze size
    start, goal = get_start_goal(ROWS, COLS)

    print(f"Running A* performance tests on maze size {ROWS}x{COLS}...\n")

    # Measure average computation time over multiple runs
    avg_time, path = measure_computation_time(start, goal)
    print(f"Average computation time over 100 runs: {avg_time:.3f} ms")

    # Validate path optimality
    optimal = check_path_optimality(path, start, goal)
    print(f"Path optimality test: {'PASS' if optimal else 'FAIL'}")

    # Measure CPU and memory usage during one A* run
    cpu, mem_current, mem_peak, _ = measure_resource_utilization(start, goal)
    print(f"CPU usage during pathfinding: {cpu:.2f}%")
    print(f"Memory usage (current): {mem_current:.2f} KB")
    print(f"Memory usage (peak): {mem_peak:.2f} KB")


if __name__ == "__main__":
    run_tests()

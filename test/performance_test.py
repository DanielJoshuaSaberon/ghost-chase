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
        start_time = time.perf_counter()  # High precision timer start
        path = a_star(start, goal)         # Run pathfinding
        end_time = time.perf_counter()    # Timer end
        total_time += (end_time - start_time)  # Accumulate elapsed time

    avg_time_ms = (total_time / iterations) * 1000  # Convert seconds to milliseconds
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

    # Calculate Manhattan distance (minimum possible steps in grid)
    expected_length = abs(start[0] - goal[0]) + abs(start[1] - goal[1]) + 1
    return len(path) == expected_length

def measure_resource_utilization(start, goal):
    """
    Measures the CPU and memory usage during a single run of the A* algorithm.

    Uses 'tracemalloc' to track memory allocation and 'psutil' to measure CPU percent.

    Args:
        start (tuple): Starting coordinate (row, col).
        goal (tuple): Goal coordinate (row, col).

    Returns:
        float: Approximate CPU usage percentage during the run.
        float: Current memory usage in kilobytes.
        float: Peak memory usage in kilobytes during the run.
        list: The path found by A* (list of coordinates).
    """
    tracemalloc.start()                     # Begin tracking memory allocations
    process = psutil.Process(os.getpid())  # Get current process for CPU stats

    cpu_before = process.cpu_percent(interval=None)  # CPU usage before pathfinding

    path = a_star(start, goal)              # Execute pathfinding

    cpu_after = process.cpu_percent(interval=0.1)   # CPU usage measured shortly after

    current_mem, peak_mem = tracemalloc.get_traced_memory()  # Memory usage stats

    tracemalloc.stop()                      # Stop memory tracking

    # Calculate approximate CPU usage during pathfinding run
    cpu_usage = cpu_after - cpu_before

    # Convert memory bytes to kilobytes for readability
    mem_usage_kb = current_mem / 1024
    peak_mem_kb = peak_mem / 1024

    return cpu_usage, mem_usage_kb, peak_mem_kb, path

def run_tests():
    start = (1, 1)    # Example start position in the maze
    goal = (13, 13)   # Example goal position in the maze

    print("Running A* performance tests...\n")

    # Test average computation time over multiple runs
    avg_time, path = measure_computation_time(start, goal)
    print(f"Average computation time over 100 runs: {avg_time:.3f} ms")

    # Test if the path found is optimal based on Manhattan distance
    optimal = check_path_optimality(path, start, goal)
    print(f"Path optimality test: {'PASS' if optimal else 'FAIL'}")

    # Test CPU and memory resource usage during a single A* run
    cpu, mem_current, mem_peak, _ = measure_resource_utilization(start, goal)
    print(f"CPU usage during pathfinding: {cpu:.2f}%")
    print(f"Memory usage (current): {mem_current:.2f} KB")
    print(f"Memory usage (peak): {mem_peak:.2f} KB")

if __name__ == "__main__":
    run_tests()

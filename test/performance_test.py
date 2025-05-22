import time
import tracemalloc
import psutil
import os
from pathfinding import a_star
from maze import ROWS, COLS

def measure_computation_time(start, goal, iterations=100):
    """
    Measures the average execution time of the A* pathfinding algorithm over multiple iterations.

    Args:
        start (tuple): Coordinates of the starting node in the grid (row, col).
        goal (tuple): Coordinates of the goal node in the grid (row, col).
        iterations (int): Number of repetitions for averaging to mitigate timing variability.

    Returns:
        float: Average computation time per run in milliseconds.
        list: Path returned from the last A* execution (sequence of grid nodes).
    """
    total_time = 0
    for _ in range(iterations):
        start_time = time.perf_counter()  # High-resolution timer to capture precise elapsed time
        path = a_star(start, goal)         # Execute A* algorithm for path calculation
        end_time = time.perf_counter()    # End timer immediately after path is found
        total_time += (end_time - start_time)  # Aggregate cumulative duration for all runs

    avg_time_ms = (total_time / iterations) * 1000  # Convert average time from seconds to milliseconds
    return avg_time_ms, path


def check_path_optimality(path, start, goal):
    """
    Assesses path optimality by comparing the A*-computed path length to the theoretical shortest distance.

    The metric used is the Manhattan distance, which represents the minimum possible path length
    on a grid without obstacles, considering only horizontal and vertical moves.

    Args:
        path (list): Ordered list of nodes representing the computed path.
        start (tuple): Start node coordinates.
        goal (tuple): Goal node coordinates.

    Returns:
        bool: True if the path length matches the Manhattan distance plus one (including start node),
              indicating an optimal path; False otherwise.
    """
    if not path:
        return False  # No path found indicates failure or unsolvability, hence non-optimal

    # Manhattan distance calculation: sum of absolute differences of row and column indices
    expected_length = abs(start[0] - goal[0]) + abs(start[1] - goal[1]) + 1
    # Path length includes all nodes traversed, so optimal if equal to expected minimal distance + start node
    return len(path) == expected_length


def measure_resource_utilization(start, goal):
    """
    Profiles system resource consumption during a single execution of the A* pathfinding algorithm.

    Utilizes Python's 'tracemalloc' to trace memory allocations and peak memory footprint,
    and 'psutil' to capture CPU usage statistics specifically for the current Python process.

    Args:
        start (tuple): Starting node coordinates.
        goal (tuple): Goal node coordinates.

    Returns:
        float: Percentage of CPU utilization attributed to the A* execution.
        float: Current memory usage in kilobytes at the time of measurement.
        float: Peak memory usage in kilobytes during the pathfinding run.
        list: The computed path from start to goal.
    """
    tracemalloc.start()                     # Initiate memory tracking to monitor allocations during runtime
    process = psutil.Process(os.getpid())  # Obtain process object for accurate CPU usage measurement

    cpu_before = process.cpu_percent(interval=None)  # Record CPU usage baseline before pathfinding begins

    path = a_star(start, goal)              # Run A* pathfinding algorithm (compute shortest path)

    cpu_after = process.cpu_percent(interval=0.1)   # Sample CPU usage after a short interval post-execution

    current_mem, peak_mem = tracemalloc.get_traced_memory()  # Retrieve current and peak memory allocation snapshots

    tracemalloc.stop()                      # Terminate memory tracking to conserve resources

    # Calculate approximate CPU utilization by subtracting baseline from post-execution sample
    cpu_usage = cpu_after - cpu_before

    # Convert bytes to kilobytes (KB) for easier interpretation of memory usage metrics
    mem_usage_kb = current_mem / 1024
    peak_mem_kb = peak_mem / 1024

    return cpu_usage, mem_usage_kb, peak_mem_kb, path


def get_start_goal(rows, cols):
        # Generic fallback: start near top-left, goal near bottom-right, avoiding edges
        return (1, 1), (rows - 2, cols - 2)


def run_tests():
    """
    Coordinates execution of the A* performance and resource profiling tests,
    displaying detailed outputs for computational efficiency and pathfinding quality.

    Tests are contextualized to the current maze dimensions provided by global settings.
    """
    start, goal = get_start_goal(ROWS, COLS)

    print(f"Running A* performance tests on maze size {ROWS}x{COLS}...\n")

    avg_time, path = measure_computation_time(start, goal)
    print(f"Average computation time over 100 runs: {avg_time:.3f} ms")

    optimal = check_path_optimality(path, start, goal)
    print(f"Path optimality test: {'PASS' if optimal else 'FAIL'}")

    cpu, mem_current, mem_peak, _ = measure_resource_utilization(start, goal)
    print(f"CPU usage during pathfinding: {cpu:.2f}%")
    print(f"Memory usage (current): {mem_current:.2f} KB")
    print(f"Memory usage (peak): {mem_peak:.2f} KB")


if __name__ == "__main__":
    run_tests()

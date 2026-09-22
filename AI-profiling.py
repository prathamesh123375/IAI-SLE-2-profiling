"""
BFS vs DFS profiling experiment: shortest-path / path-finding in a maze.

Problem: Given a perfect maze (exactly one path between any two cells,
generated as a spanning tree so there are no loops), find a path from the
top-left cell to the bottom-right cell using:
  Algorithm A: plain DFS (stack-based, fixed neighbour order)
  Algorithm B: BFS (queue-based, fixed neighbour order)

Nodes expanded = number of times a cell is popped off the frontier and
visited for the first time (counted directly inside each function).
"""
import random
import time
from collections import deque

# Fixed neighbour exploration order used by BOTH algorithms so that any
# difference in node counts comes from the search strategy (stack vs queue),
# not from move ordering. Order chosen so DFS commits to a direction that is
# NOT generally the shortest way toward the goal (bottom-right), so it has to
# backtrack out of dead-end branches -- a realistic worst case for DFS.
NEIGHBOR_ORDER = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Up, Left, Down, Right


def generate_maze(size, seed):
    """Randomized-DFS ('recursive backtracker') perfect maze generator.
    Returns a dict: passages[(x,y)] = set of (nx,ny) cells reachable directly
    from (x,y) (i.e., the wall between them has been carved away)."""
    rng = random.Random(seed)
    passages = {(x, y): set() for x in range(size) for y in range(size)}
    visited = [[False] * size for _ in range(size)]
    stack = [(0, 0)]
    visited[0][0] = True
    while stack:
        x, y = stack[-1]
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        rng.shuffle(dirs)
        carved = False
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and not visited[nx][ny]:
                passages[(x, y)].add((nx, ny))
                passages[(nx, ny)].add((x, y))
                visited[nx][ny] = True
                stack.append((nx, ny))
                carved = True
                break
        if not carved:
            stack.pop()
    return passages


def neighbors(cell, passages):
    x, y = cell
    for dx, dy in NEIGHBOR_ORDER:
        n = (x + dx, y + dy)
        if n in passages.get(cell, ()):
            yield n


def dfs_solve(start, goal, passages):
    """Iterative DFS using an explicit stack."""
    visited = set()
    stack = [(start, [start])]
    nodes = 0
    while stack:
        cur, path = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        nodes += 1
        if cur == goal:
            return path, nodes
        # push in reverse so NEIGHBOR_ORDER's first choice is popped first
        for n in reversed(list(neighbors(cur, passages))):
            if n not in visited:
                stack.append((n, path + [n]))
    return None, nodes


def bfs_solve(start, goal, passages):
    """BFS using a queue -- guarantees the shortest path in an unweighted graph."""
    visited = {start}
    queue = deque([(start, [start])])
    nodes = 0
    while queue:
        cur, path = queue.popleft()
        nodes += 1
        if cur == goal:
            return path, nodes
        for n in neighbors(cur, passages):
            if n not in visited:
                visited.add(n)
                queue.append((n, path + [n]))
    return None, nodes


def time_it(fn, *args, runs=5):
    times = []
    result = None
    for _ in range(runs):
        t0 = time.perf_counter()
        result = fn(*args)
        times.append((time.perf_counter() - t0) * 1000)  # ms
    return sum(times) / len(times), result
if __name__ == "__main__":
    size = 20
    seed = 42

    start = (0, 0)
    goal = (size - 1, size - 1)

    maze = generate_maze(size, seed)

    dfs_time, (dfs_path, dfs_nodes) = time_it(
        dfs_solve, start, goal, maze
    )

    bfs_time, (bfs_path, bfs_nodes) = time_it(
        bfs_solve, start, goal, maze
    )

    print("BFS vs DFS Profiling")
    print("--------------------")

    print("DFS:")
    print("Path length:", len(dfs_path))
    print("Nodes expanded:", dfs_nodes)
    print("Average time:", dfs_time, "ms")

    print("\nBFS:")
    print("Path length:", len(bfs_path))
    print("Nodes expanded:", bfs_nodes)
    print("Average time:", bfs_time, "ms")

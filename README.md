# BFS vs DFS Maze Pathfinding — Profiling Study

## 📌 Project Overview

This project compares **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** for solving a randomly generated maze.

The main goal is to study how both search algorithms perform as the maze size increases by measuring:

* Execution time
* Number of nodes expanded
* Path length
* Profiling information
* Performance differences between DFS and BFS

The experiment uses a **perfect maze**, which is a spanning-tree maze where exactly one path exists between any two cells. Therefore, both algorithms find the same final path.

---

## 🧠 Algorithms Used

### 1. Depth-First Search (DFS)

DFS explores one branch as deeply as possible before backtracking.

**Implementation:**

* Iterative
* Stack-based
* Fixed neighbour order
* Returns the path and number of nodes expanded

### 2. Breadth-First Search (BFS)

BFS explores the maze level by level, starting from the source cell.

**Implementation:**

* Queue-based
* Same fixed neighbour order as DFS
* Returns the path and number of nodes expanded

---

## 🗺️ Problem Statement

A randomly generated perfect maze is given.

The task is to find a path from:

**Start:** Top-left cell
**Goal:** Bottom-right cell

The maze is generated using a randomized DFS backtracking approach. Since it is a spanning tree, there is exactly one path between any two cells.

---

## ⚙️ Profiling Method

The following Python tools were used:

* `py-spy` — profiling and call-graph/flame-graph analysis
* `time.perf_counter()` — accurate execution-time measurement
* Manual node counter — counts cells visited for the first time

Three maze sizes were tested:

| Case         | Maze Size |
| ------------ | --------: |
| Best Case    |     5 × 5 |
| Average Case |   12 × 12 |
| Worst Case   |   25 × 25 |

Each algorithm was executed **5 times per test case**, giving **15 runs per algorithm**.

---

## 📊 Results

### Summary

| Metric                 |       DFS |       BFS |
| ---------------------- | --------: | --------: |
| Best-case time         | 0.0206 ms | 0.0121 ms |
| Average-case time      | 0.1525 ms | 0.1279 ms |
| Worst-case time        | 0.9340 ms | 0.2284 ms |
| Average nodes expanded |     251.7 |     120.7 |

BFS was faster in all three measured cases, with the largest difference occurring on the 25 × 25 maze.

### Detailed Results

| Test Case | Algorithm | Avg. Time | Nodes Expanded | Path Length |
| --------- | --------- | --------: | -------------: | ----------: |
| 5 × 5     | DFS       | 0.0206 ms |             15 |          11 |
| 5 × 5     | BFS       | 0.0121 ms |             13 |          11 |
| 12 × 12   | DFS       | 0.1525 ms |            129 |          65 |
| 12 × 12   | BFS       | 0.1279 ms |            136 |          65 |
| 25 × 25   | DFS       | 0.9340 ms |            611 |         165 |
| 25 × 25   | BFS       | 0.2284 ms |            213 |         165 |

---

## 🔍 Observations

### Small Maze — 5 × 5

Both algorithms completed the search very quickly.

* DFS: 0.0206 ms
* BFS: 0.0121 ms
* Both found a path of length 11.

### Medium Maze — 12 × 12

DFS expanded slightly fewer nodes than BFS:

* DFS: 129 nodes
* BFS: 136 nodes

However, BFS was slightly faster:

* DFS: 0.1525 ms
* BFS: 0.1279 ms

This demonstrates that **fewer expanded nodes does not always mean lower execution time**, because implementation overhead also affects runtime.

### Large Maze — 25 × 25

The performance difference became much larger:

* DFS expanded 611 nodes.
* BFS expanded 213 nodes.
* DFS took 0.9340 ms.
* BFS took 0.2284 ms.

DFS therefore expanded about **2.9× more nodes** and took about **4.1× more time** in this test. Both algorithms still found the same path of length 165.

---

## 🔬 Profiling

The worst-case workload used a 25 × 25 maze with **200 repeated solves per algorithm**.

The profiling showed that:

* DFS accounted for approximately **76%** of the captured runtime.
* BFS accounted for approximately **22%**.
* The `neighbors()` helper was the most expensive shared function.
* `neighbors()` was called approximately 2.3× more often inside DFS than BFS for this workload.

To reproduce the flame graph using `py-spy` on a normal machine:

```bash
py-spy record -o flamegraph.svg --rate 100 -- python run_experiments.py
```

---

## 📈 Key Findings

1. Both DFS and BFS successfully solved every tested maze.
2. Because the mazes are spanning trees, both algorithms always returned the same path.
3. DFS can perform well on small or shallow search spaces.
4. BFS expanded significantly fewer nodes on the largest test maze.
5. BFS was approximately 4.1× faster than DFS in the 25 × 25 test.
6. The performance difference increases as the search space becomes larger.
7. Node count and execution time do not always have a direct relationship.
8. Profiling helped identify where the program spent most of its execution time.

---

## 🛠️ Technologies Used

* **Python**
* **DFS (Depth-First Search)**
* **BFS (Breadth-First Search)**
* **py-spy**
* **time.perf_counter()**
* Maze generation using randomized DFS backtracking

---

## 🤖 AI Contribution

AI tools were used to help with:

* Maze-generation code
* Neighbour-lookup code
* DFS/BFS implementation
* Profiling and experiment scripts
* Chart and flame-graph generation
* Report formatting

The experiments, results, validation of the output, and final analysis were performed and checked by the student.

---

## 📝 Conclusion

This experiment demonstrates that the performance of DFS and BFS depends on the structure and size of the search space.

For the tested perfect mazes, both algorithms always found the same path because there was only one possible route. However, as the maze became larger, BFS expanded considerably fewer nodes and required less execution time in the tested cases.

The 25 × 25 experiment showed the largest difference, where BFS expanded about **2.9× fewer nodes** and ran about **4.1× faster** than DFS.

---

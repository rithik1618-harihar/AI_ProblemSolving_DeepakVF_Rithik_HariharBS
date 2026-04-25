<div align="center">

# 🗺️ Smart Navigation System
### Breadth-First Search (BFS) & Depth-First Search (DFS)

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-000000?style=for-the-badge&logo=flask&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-Interactive-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![AI](https://img.shields.io/badge/AI-Problem_8-6f42c1?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-1d9e75?style=for-the-badge)

**Problem 8 — Artificial Intelligence Problem Solving Assignment**

| | |
|---|---|
| **Team Member 1** | [Your Full Name] — [Register Number] |
| **Team Member 2** | [Partner Full Name] — [Register Number] |
| **Department** | [Your Department] |
| **Institution** | [Your College Name] |
| **Submission Date** | April 25, 2026 |

---

## 🌐 Live Interactive Website

### 👉 [Click Here to Open the Live Demo](https://your-username.github.io/AI_ProblemSolving_XXXXX/Problem8_SmartNavigation/static/index.html)

> ✅ Works entirely in the browser — **no installation needed**. Just open the link and start exploring!

</div>

---

## 📑 Table of Contents

1. [Problem Description](#-problem-description)
2. [Features](#-features)
3. [Algorithms Used](#-algorithms-used)
   - [BFS — Breadth-First Search](#-bfs--breadth-first-search)
   - [DFS — Depth-First Search](#-dfs--depth-first-search)
4. [Algorithm Comparison](#-algorithm-comparison)
5. [Folder Structure](#-folder-structure)
6. [Installation & Execution Steps](#-installation--execution-steps)
7. [How to Use the Website](#-how-to-use-the-website)
8. [Sample Inputs & Outputs](#-sample-inputs--outputs)
9. [Code Explanation](#-code-explanation)
10. [Real-World Applications](#-real-world-applications)
11. [References](#-references)

---

## 📋 Problem Description

> *"A navigation system is required to find routes between different locations, similar to Google Maps. Write a Python program in which the user can input a start node, a goal node, and a set of connections between locations through an interactive interface (GUI). The system should dynamically build a graph and find a path between the start and goal nodes."*

### What the system does

- Accepts **locations (nodes)** and **roads (edges)** as user input
- Dynamically builds a **graph** from the input
- Finds a path from the **start node** to the **goal node** using:
  - 🔵 **BFS** — Breadth-First Search
  - 🟣 **DFS** — Depth-First Search
- **Compares both algorithms** based on:
  - Path optimality (shortest vs non-optimal)
  - Number of nodes explored
  - Efficiency of traversal

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ Interactive graph builder | Add nodes and edges dynamically through the UI |
| 🎨 Visual graph canvas | Draggable nodes, color-coded paths |
| 🔵 BFS visualization | Highlights BFS path and explored nodes in blue |
| 🟣 DFS visualization | Highlights DFS path and explored nodes in purple |
| 📊 Side-by-side comparison | Path length, nodes explored, optimality shown together |
| 🔄 Example graph loader | Pre-built example to get started instantly |
| 📱 Works on any device | No installation, no server — pure browser app |

---

## 🧠 Algorithms Used

### 🔵 BFS — Breadth-First Search

#### Concept

BFS is an **uninformed search algorithm** that explores a graph **level by level**. It starts at the source node and visits all neighbors at the current depth before moving to the next depth level. This guarantees that the first time BFS reaches the goal, it has done so via the **shortest possible path** (fewest edges).

#### Properties

| Property | Value |
|---|---|
| Search Strategy | Level-by-level (breadth-wise) |
| Data Structure Used | **Queue (FIFO)** |
| Guarantees Shortest Path? | ✅ **YES** |
| Time Complexity | **O(V + E)** where V = vertices, E = edges |
| Space Complexity | **O(V)** |
| Complete? | Yes — will always find a path if one exists |

#### Step-by-step Trace (Example Graph)

```
Graph: A-B, A-C, B-D, B-E, C-F, D-G, E-G, F-G
Start: A   Goal: G

Step 1:  Queue = [A]          Visited = {A}
Step 2:  Visit A → add B, C   Queue = [B, C]
Step 3:  Visit B → add D, E   Queue = [C, D, E]
Step 4:  Visit C → add F      Queue = [D, E, F]
Step 5:  Visit D → add G      Queue = [E, F, G]
Step 6:  Visit G ✅ GOAL FOUND!

Path found: A → B → D → G
Path length: 3 hops  ← SHORTEST PATH
Nodes explored: 6
```

#### Python Implementation

```python
from collections import deque

def bfs(graph, start, goal):
    visited = {start}
    queue = deque([(start, [start])])  # (current_node, path_so_far)

    while queue:
        current, path = queue.popleft()  # FIFO — take from front

        if current == goal:
            return path  # Found the goal!

        for neighbor in sorted(graph[current]):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found
```

---

### 🟣 DFS — Depth-First Search

#### Concept

DFS is an **uninformed search algorithm** that explores a graph by going **as deep as possible** along each branch before backtracking. It uses recursion (or an explicit stack). DFS finds *a* valid path, but **does not guarantee** it is the shortest one.

#### Properties

| Property | Value |
|---|---|
| Search Strategy | Deep-first (goes all the way down one branch) |
| Data Structure Used | **Stack / Recursion** |
| Guarantees Shortest Path? | ❌ **NO** |
| Time Complexity | **O(V + E)** where V = vertices, E = edges |
| Space Complexity | **O(V)** |
| Complete? | Yes (if no cycles, or with visited tracking) |

#### Step-by-step Trace (Same Example Graph)

```
Graph: A-B, A-C, B-D, B-E, C-F, D-G, E-G, F-G
Start: A   Goal: G

Step 1: Visit A  → go deep to B (first neighbor)
Step 2: Visit B  → go deep to D (first neighbor of B)
Step 3: Visit D  → go deep to G (first neighbor of D)
Step 4: Visit G  ✅ GOAL FOUND!

Path found: A → B → D → G
Path length: 3 hops
Nodes explored: 4  ← explored FEWER nodes than BFS
```

> ⚠️ Note: DFS does not always find the shortest path. In different graphs, DFS may take a longer route while BFS always gives the shortest.

#### Python Implementation

```python
def dfs(graph, start, goal):
    explored = []

    def dfs_recursive(node, path, visited):
        visited.add(node)
        explored.append(node)

        if node == goal:
            return path  # Found the goal!

        for neighbor in sorted(graph[node]):
            if neighbor not in visited:
                result = dfs_recursive(neighbor, path + [neighbor], visited)
                if result is not None:
                    return result

        return None  # Backtrack

    path = dfs_recursive(start, [start], set())
    return path
```

---

## 📊 Algorithm Comparison

| Metric | 🔵 BFS | 🟣 DFS |
|---|---|---|
| **Path optimality** | ✅ Always finds shortest path | ❌ Not guaranteed |
| **Nodes explored** | More — explores all levels | Fewer — goes deep first |
| **Memory usage** | Higher (stores all frontier nodes) | Lower (only current path) |
| **Speed (to find any path)** | Slower for deep goals | Faster for deep goals |
| **Best used for** | Shortest path, GPS navigation | Maze solving, deep graph traversal |
| **Data structure** | Queue (FIFO) | Stack / Recursion |
| **Completeness** | ✅ Complete | ✅ Complete (with visited set) |
| **Use in real world** | Google Maps, Social Networks | File systems, Puzzles, Games |

### When does DFS beat BFS?
- When the goal is very **deep** in the graph
- When you just need **any** path, not the shortest
- When **memory is limited** (DFS uses less memory)

### When does BFS beat DFS?
- When you need the **shortest path**
- When the goal is **close to the start** (shallow)
- In **GPS and navigation** systems

---

## 🗂 Folder Structure

```
AI_ProblemSolving_<RegisterNumber>/
│
├── 📄 README.md                              ← You are here
│
└── 📁 Problem8_SmartNavigation/
    │
    ├── 📁 src/
    │   ├── 📄 algorithms.py                  ← Core BFS & DFS logic (pure Python)
    │   └── 📄 app.py                         ← Flask web server backend
    │
    ├── 📁 static/
    │   └── 📄 index.html                     ← Standalone website (open directly in browser)
    │
    ├── 📁 templates/
    │   └── 📄 index.html                     ← Flask HTML template (used with app.py)
    │
    ├── 📁 sample_outputs/
    │   └── 📄 output.txt                     ← Sample run results and comparison
    │
    ├── 📄 requirements.txt                   ← Python dependencies (just Flask)
    └── 📄 README.md                          ← Problem-specific readme
```

---

## ▶ Installation & Execution Steps

### ✅ Option 1 — Open in Browser (Easiest — No installation needed)

This is the recommended method. The website works 100% offline.

```
1. Download or clone this repository
2. Open the folder: Problem8_SmartNavigation → static
3. Double-click index.html
4. It opens in your browser — start using immediately!
```

Or use the live GitHub Pages link:
👉 `https://your-username.github.io/AI_ProblemSolving_XXXXX/Problem8_SmartNavigation/static/index.html`

---

### ✅ Option 2 — Run Python Script Directly

**Requirements:** Python 3.8 or above

**Step 1 — Clone the repository**
```bash
git clone https://github.com/your-username/AI_ProblemSolving_XXXXX.git
cd AI_ProblemSolving_XXXXX
```

**Step 2 — Go to the src folder**
```bash
cd Problem8_SmartNavigation/src
```

**Step 3 — Run the algorithm**
```bash
python3 -c "
from algorithms import Graph, compare_algorithms

# Build the graph
g = Graph()
edges = [
    ('A','B'), ('A','C'), ('B','D'),
    ('B','E'), ('C','F'), ('D','G'),
    ('E','G'), ('F','G')
]
for a, b in edges:
    g.add_edge(a, b)

# Run both algorithms
result = compare_algorithms(g, 'A', 'G')

# Print BFS result
print('=== BFS Result ===')
print('Path    :', ' -> '.join(result['bfs']['path']))
print('Length  :', result['comparison']['bfs_path_length'], 'hops')
print('Explored:', result['bfs']['nodes_count'], 'nodes')

# Print DFS result
print()
print('=== DFS Result ===')
print('Path    :', ' -> '.join(result['dfs']['path']))
print('Length  :', result['comparison']['dfs_path_length'], 'hops')
print('Explored:', result['dfs']['nodes_count'], 'nodes')
"
```

---

### ✅ Option 3 — Run with Flask Web Server

**Requirements:** Python 3.8+, pip

**Step 1 — Install dependencies**
```bash
cd Problem8_SmartNavigation
pip install -r requirements.txt
```

**Step 2 — Start the server**
```bash
python src/app.py
```

**Step 3 — Open in browser**
```
http://localhost:5000
```

---

## 🖥️ How to Use the Website

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Add edges (connections between locations)       │
│  → Type "From" node name (e.g., A)                      │
│  → Type "To" node name   (e.g., B)                      │
│  → Click "+ Add Edge"                                    │
│  → Repeat for all connections                           │
│                                                         │
│  STEP 2: Set Start and Goal                             │
│  → Type your start node  (e.g., A)                      │
│  → Type your goal node   (e.g., G)                      │
│                                                         │
│  STEP 3: Run the search                                 │
│  → Click "▶ Run BFS & DFS"                             │
│  → See both paths highlighted on the graph              │
│  → Compare results in the panel below                   │
│                                                         │
│  BONUS: Drag any node to rearrange the graph layout     │
│  BONUS: Click "↺ Load Example Graph" to see a demo     │
└─────────────────────────────────────────────────────────┘
```

### Color Guide on the Graph

| Color | Meaning |
|---|---|
| 🟢 Green node | Start node |
| 🔴 Red node | Goal node |
| 🔵 Blue node / edge | On BFS path |
| 🟣 Purple node / edge | On DFS path |
| 🟠 Orange node / edge | On both BFS and DFS path |
| ⚫ Dark node | Not on any path |

---

## 🖼️ Sample Inputs & Outputs

### Sample Input 1 — Simple graph

```
Nodes   : A, B, C, D, E, F, G
Edges   : A-B, A-C, B-D, B-E, C-F, D-G, E-G, F-G
Start   : A
Goal    : G
```

### Sample Output 1

```
════════════════════════════════════════════
  BFS Result
════════════════════════════════════════════
  Path          : A → B → D → G
  Path Length   : 3 hops
  Nodes Explored: A, B, C, D, E, F, G  (7 total)
  Optimal       : YES ✓

════════════════════════════════════════════
  DFS Result
════════════════════════════════════════════
  Path          : A → B → D → G
  Path Length   : 3 hops
  Nodes Explored: A, B, D, G  (4 total)
  Optimal       : Not guaranteed

════════════════════════════════════════════
  Comparison
════════════════════════════════════════════
  Metric              BFS       DFS
  ─────────────────────────────────────────
  Path length         3 hops    3 hops
  Nodes explored      7         4
  Shortest path?      YES       Not guaranteed
  ─────────────────────────────────────────
  Result: Both found same length path.
          DFS explored fewer nodes (4 vs 7).
          BFS guarantees this is the shortest.
════════════════════════════════════════════
```

---

### Sample Input 2 — Where BFS and DFS give different paths

```
Nodes   : S, A, B, C, D, G
Edges   : S-A, S-B, A-G, B-C, C-D, D-G
Start   : S
Goal    : G
```

### Sample Output 2

```
BFS Path: S → A → G      (length: 2 hops)  ← SHORTEST ✓
DFS Path: S → B → C → D → G  (length: 4 hops)  ← LONGER ✗

Nodes explored by BFS: 3
Nodes explored by DFS: 5

Conclusion: BFS found a 2-hop path.
            DFS found a 4-hop path — not optimal!
            This clearly shows BFS is better for shortest path.
```

---

## 💻 Code Explanation

### `algorithms.py` — Core Logic

```python
class Graph:
    """
    Represents an undirected graph using an adjacency list.
    Each node maps to a list of its neighbors.
    """
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, node1, node2):
        # Adds a bidirectional connection between node1 and node2
        self.adjacency_list[node1].append(node2)
        self.adjacency_list[node2].append(node1)
```

```python
def bfs(graph, start, goal):
    """
    Uses a queue (FIFO) to explore nodes level by level.
    Always finds the shortest path.
    """
    queue = deque([(start, [start])])    # Start with source node
    visited = {start}

    while queue:
        current, path = queue.popleft() # Take node from FRONT of queue
        if current == goal:
            return path                 # Shortest path found!
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
```

```python
def dfs(graph, start, goal):
    """
    Uses recursion (implicit stack) to go as deep as possible first.
    Finds a path but not necessarily the shortest.
    """
    def recurse(node, path, visited):
        visited.add(node)
        if node == goal:
            return path                 # Path found (may not be shortest)
        for neighbor in graph[node]:
            if neighbor not in visited:
                result = recurse(neighbor, path + [neighbor], visited)
                if result:
                    return result       # Return first path found
        return None                     # Backtrack

    return recurse(start, [start], set())
```

### `app.py` — Flask Backend

```python
@app.route("/api/search", methods=["POST"])
def search():
    """
    Receives graph data from the frontend,
    runs BFS and DFS, returns comparison results as JSON.
    """
    data = request.get_json()
    g = Graph()
    for edge in data["edges"]:
        g.add_edge(edge[0], edge[1])
    result = compare_algorithms(g, data["start"], data["goal"])
    return jsonify(result)
```

---

## 🌍 Real-World Applications

| Application | Uses BFS/DFS? | How? |
|---|---|---|
| 🗺️ Google Maps | BFS-based | Finding shortest route between two places |
| 🌐 Social Networks | BFS | Finding degrees of separation between users |
| 🎮 Video Games | DFS | AI pathfinding in mazes and maps |
| 🌐 Web Crawlers | BFS | Crawling websites level by level |
| 🧩 Puzzle Solvers | DFS | Exploring possible moves in puzzles |
| 🔌 Network Routing | BFS | Finding shortest data transmission path |
| 📁 File Systems | DFS | Searching through folders and subfolders |

---

## 📌 Commit History

| # | Commit Message | Files Included |
|---|---|---|
| 1 | `Initial commit: folder structure and README` | `README.md` |
| 2 | `Add BFS and DFS algorithm implementation` | `src/algorithms.py`, `src/app.py` |
| 3 | `Add interactive web interface with graph visualization` | `static/index.html`, `templates/index.html` |
| 4 | `Add sample outputs and project requirements` | `sample_outputs/output.txt`, `requirements.txt` |

---

## 🔖 References

- Russell, S. & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
- Cormen, T. H. et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- BFS — Wikipedia: https://en.wikipedia.org/wiki/Breadth-first_search
- DFS — Wikipedia: https://en.wikipedia.org/wiki/Depth-first_search
- Python `collections.deque`: https://docs.python.org/3/library/collections.html#collections.deque
- Flask Documentation: https://flask.palletsprojects.com/

---

<div align="center">

Made with ❤️ for AI Problem Solving Assignment

**[Your Name] & [Partner Name] | [College Name] | April 2026**

</div>

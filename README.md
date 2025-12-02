### Warsaw Route Optimization using Dijkstra's Algorithm

## 1. Description of Our Approach

### City Selection

We chose Warsaw, Poland as our test city for several reasons. First, Warsaw has a well-developed road network with clear landmarks that make it easy to validate our results. Second, the city offers a good mix of infrastructure types (airports, sports stadiums, universities, parks, and cultural sites) which let us build a realistic graph that represents actual urban navigation patterns. 

### Node Definition

We selected 10 locations (labeled A through J) across Warsaw that serve as nodes in our graph. The starting point (A) is Warsaw Chopin Airport, and the destination (J) is PGE Narodowy Stadium. The eight internal nodes (B through I) include:
- B: Sluzewiec Horse Racetrack
- C: Szczesliwicki Park
- D: SGH Warsaw School of Economics
- E: Warsaw West Train Station
- F: Legia Warsaw Stadium
- G: Warsaw University Library
- H: Palace of Culture and Science
- I: National Museum in Warsaw


### Map Construction

Each location was mapped using real GPS coordinates obtained from Google Maps. Each node connects to 2-4 neighboring locations based on actual road geography, creating 16 bidirectional edges in total. Travel times between connected nodes were measured using Google Maps under typical traffic conditions, ranging from 3 to 14 minutes. These times were stored as edge weights in our graph, representing the cost (in minutes) to travel between locations.

### Base Case Scenario Design

For the base case, we assumed no  traffic conditions. All travel times came directly from Google Maps. As we mapped then, there was 3 am in Poland, which suggests no traffic on the streets.

---

## 2. Graph Structure & Algorithm Implementation

### Graph Representation

Our implementation uses a dictionary-based adjacency matrix as the core data structure. The `WeightedGraph` class maintains two primary structures:

1. A list of `Vertex` objects indexed sequentially (where node A is index 0, node B is index 1, etc.).
2. A hash table where edge weights are stored using vertex index tuples as keys.

For example, the entry `(0, 1): 9` means traveling from node A to node B takes 9 minutes. This approach gives us O(1) lookup time for edge weights while staying memory-efficient—we only store the 32 directional edges we actually have, not all 100 possible edges in a 10-node graph.

### Dijkstra's Algorithm Implementation

We implemented Dijkstra's algorithm using Python's `heapq` module for the priority queue. The algorithm maintains two dictionaries:

- `dist`: tracks the minimum travel time to reach each node (initialized to infinity except for the starting node)
- `parent`: stores which node we came from to reach each location, allowing path reconstruction


## Key Assumptions

**Graph Structure:**
- Weight = travel time (minutes)
- Each node connected to 2-4 neighbors
- Bidirectional edges: same travel time in both directions

**Data Collection:**
- Travel mode: car only
- Travel times from Google Maps
- Base case: no traffic conditions assumed
- Traffic case: random factor between 1 and 3 applied to Base edge times; traffic factors change each time t_edgeWeight() is executed
- Traffic & Base: all edges available for travel

**Node Selection:**
- Selected locations represent key landmarks and famous infrastructure in Warsaw
- 10 nodes distributed across the city

**Time Precision:**
- Travel times without decimals for base; with decimals for traffic
- Base case range: 3-14 minutes between connected nodes

---

## 3. Code-Based Verification — Base and Rush Hour Scenarios

We used our Python/Jupyter Notebook implementation to verify that the algorithm correctly computes shortest paths under both base and traffic conditions, including uncertainty and extreme events.

### Base Case with Uncertainty
- Applied ±10% random variation to all edge weights to simulate minor delays or fluctuations (e.g., traffic lights, weather conditions)
- Run the algorithm from A → J and J → A
- Results were consistent with expected travel times, with minor deviations due to random variation

### Traffic Case with Uncertainty
- Introduced a traffic multiplier (1–3×) to simulate rush hour conditions
- Applied ±10% random variation again
- Shortest path recalculated considering inflated travel times
- Verified algorithm correctly updated edge times and produced expected paths

### Traffic Case with Extreme Events
- Randomly selected three edges per run to simulate extreme disruptions (80% normal, 20% major delay ×10)
- Observed that extreme events dramatically altered optimal paths in some runs
- Console logs clearly report which edges were disrupted and the inflated travel times

This process confirms the robustness of our Dijkstra implementation and demonstrates realistic route variation under uncertainty.

---

## 4. Discussion and Analysis

### Route Changes
- Base case vs. traffic: Rush hour and random traffic multipliers caused the shortest path to deviate from the original route (A→B→D→F→J) to longer but faster alternatives (A→B→D→H→I→J)
- Extreme events produced the largest deviations, sometimes bypassing multiple nodes to avoid severely delayed edges

### Impact of Uncertainty
- Minor ±10% fluctuations rarely change routes but provide realistic travel-time variability
- Extreme events (×10 delay on selected edges) highlight the sensitivity of route selection to rare but significant disruptions

### Interpretation of Results
- The algorithm dynamically adapts to changing conditions, mimicking real GPS behavior
- Even in a small 10-node network, accounting for uncertainty and extreme events demonstrates how robust navigation planning must handle both predictable and rare disruptions

### Assumptions and Limitations
- Travel times are based on Google Maps estimates; actual conditions may differ
- Only car travel is considered; pedestrian or public transit routes are excluded
- Extreme events are randomly assigned; repeated runs may yield different disrupted edges
- Network size is small (10 nodes); scalability for larger cities may require optimizations

### Conclusion

Our implementation successfully integrates both typical uncertainty and rare extreme events into route planning. The implemented system demonstrates that Dijkstra’s algorithm, augmented with uncertainty and extreme-event simulation, can effectively model realistic urban navigation scenarios. Minor fluctuations affect travel times slightly, while rare extreme events can dramatically alter route choice. Each simulation run provides a unique result, reflecting the inherent unpredictability of real-world traffic networks.

---

## Results 

Base Case:

**Shortest Path A→J:**
- Route: A → B → D → F → J
- Locations:
  - A: Warsaw Chopin Airport
  - B: Sluzewiec Horse Racetrack
  - D: SGH Warsaw School of Economics
  - F: Legia Warsaw Stadium
  - J: PGE Narodowy Stadium
- **Total Travel Time: 32 minutes**

Traffic Case:

**Shortest Path A→J:**
- Route: A → B → D → H → I → J
- Locations:
  - A: Warsaw Chopin Airport (start)
  - B: Sluzewiec Horse Racetrack (13.0 mins)
  - D: SGH Warsaw School of Economics (20.1 mins)
  - H: Palace of Culture and Science (10.6 mins)
  - I: National Museum in Warsaw (7.5 mins)
  - J: PGE Narodowy Stadium (6.8 mins)
- **Total Travel Time: 58.2 minutes**



---

Few Vizualizations:
<img width="1022" height="613" alt="image" src="https://github.com/user-attachments/assets/247710ee-3cba-4d9d-b6e4-c7aa790bace8" />

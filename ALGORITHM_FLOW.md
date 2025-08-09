# K-Medoids Algorithm Flow for Optimal Resource Center Placement

## High-Level Overview

```
Input Data → Data Loading → Constraint Filtering → K-Medoids Optimization → Output Results
```

## Detailed Computation Flow

### 1. INPUT PHASE

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT PARAMETERS                         │
├─────────────────────────────────────────────────────────────────┤
│ • resource_points.csv (id, lat, lon, quantity)                 │
│ • zone_features.csv (id, slope, elevation, land_type)          │
│ • road_network.csv (distance matrix between all points)        │
│ • num_centers (k = number of centers to select)                │
│ • min_dist_km (minimum distance between centers)               │
│ • exclude_land_types (comma-separated list)                    │
│ • max_slope (maximum allowed slope in degrees)                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. DATA LOADING PHASE

```
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LOADING                              │
├─────────────────────────────────────────────────────────────────┤
│ read_resource_points():                                         │
│   ├─ Parse CSV → vector<ResourcePoint>                         │
│   └─ Store: {id, lat, lon, quantity}                           │
│                                                                 │
│ read_zone_features():                                           │
│   ├─ Parse CSV → vector<ZoneFeature>                           │
│   └─ Store: {id, slope, elevation, land_type}                  │
│                                                                 │
│ read_road_network():                                            │
│   ├─ Parse CSV → 2D matrix[point_i][point_j]                   │
│   └─ Store: real road distances between all point pairs        │
└─────────────────────────────────────────────────────────────────┘
```

### 3. CONSTRAINT FILTERING PHASE

```
┌─────────────────────────────────────────────────────────────────┐
│                   CANDIDATE ZONE FILTERING                      │
├─────────────────────────────────────────────────────────────────┤
│ merge_candidates():                                             │
│   FOR each resource_point:                                     │
│     ├─ Find matching zone_feature by ID                        │
│     ├─ APPLY CONSTRAINTS:                                       │
│     │   ├─ IF land_type ∈ exclude_land_types → SKIP            │
│     │   └─ IF slope > max_slope → SKIP                         │
│     └─ IF passes constraints → ADD to candidates[]             │
│                                                                 │
│ RESULT: vector<CandidateZone> (valid centers only)             │
└─────────────────────────────────────────────────────────────────┘
```

### 4. K-MEDOIDS OPTIMIZATION PHASE

```
┌─────────────────────────────────────────────────────────────────┐
│                    K-MEDOIDS ALGORITHM                          │
├─────────────────────────────────────────────────────────────────┤
│ OUTER LOOP: Multiple Random Trials (10 trials)                 │
│   │                                                             │
│   FOR trial = 1 to 10:                                         │
│     │                                                           │
│     ├─ INITIALIZATION:                                          │
│     │   ├─ Randomly shuffle candidate indices                   │
│     │   ├─ Select first k candidates as initial medoids        │
│     │   └─ CHECK: min_distance_ok() using haversine distance   │
│     │                                                           │
│     ├─ ITERATIVE OPTIMIZATION:                                  │
│     │   │                                                       │
│     │   WHILE (changed && iter < max_iter):                    │
│     │     │                                                     │
│     │     ├─ ASSIGNMENT STEP:                                   │
│     │     │   FOR each resource_point:                         │
│     │     │     ├─ Find nearest medoid using road_matrix[][]   │
│     │     │     └─ Assign point to nearest medoid              │
│     │     │                                                     │
│     │     ├─ UPDATE STEP (Medoid Swapping):                    │
│     │     │   FOR each current_medoid:                         │
│     │     │     FOR each non_medoid_candidate:                 │
│     │     │       ├─ Create new_medoids by swapping            │
│     │     │       ├─ CHECK: min_distance_ok()                  │
│     │     │       ├─ REASSIGN all points to nearest medoids    │
│     │     │       ├─ CALCULATE: new_total_cost                 │
│     │     │       └─ IF new_cost < current_cost → ACCEPT swap  │
│     │     │                                                     │
│     │     └─ iter++                                             │
│     │                                                           │
│     └─ SAVE: best_medoids if final_cost < global_best_cost     │
│                                                                 │
│ RESULT: Global best medoids across all trials                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5. COST CALCULATION DETAILS

```
┌─────────────────────────────────────────────────────────────────┐
│                      COST CALCULATION                           │
├─────────────────────────────────────────────────────────────────┤
│ total_cost():                                                   │
│   total_cost = 0                                               │
│   FOR each resource_point:                                     │
│     ├─ min_distance = infinity                                 │
│     ├─ FOR each selected_center:                               │
│     │   ├─ distance = road_matrix[point_idx][center_idx]       │
│     │   └─ min_distance = min(min_distance, distance)          │
│     └─ total_cost += min_distance × point.quantity             │
│                                                                 │
│ RETURN: total_cost (weighted sum of distances)                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6. CONSTRAINT VALIDATION

```
┌─────────────────────────────────────────────────────────────────┐
│                  CONSTRAINT VALIDATION                          │
├─────────────────────────────────────────────────────────────────┤
│ min_distance_ok():                                              │
│   FOR each pair of centers (i,j):                              │
│     ├─ distance = haversine(center_i.lat, center_i.lon,        │
│     │                       center_j.lat, center_j.lon)        │
│     └─ IF distance < min_dist_km → RETURN false                │
│   RETURN true                                                   │
│                                                                 │
│ Land Type Filtering:                                            │
│   IF zone.land_type ∈ exclude_land_types → EXCLUDE             │
│                                                                 │
│ Slope Filtering:                                                │
│   IF zone.slope > max_slope → EXCLUDE                          │
└─────────────────────────────────────────────────────────────────┘
```

### 7. OUTPUT PHASE

```
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUT RESULTS                          │
├─────────────────────────────────────────────────────────────────┤
│ Best Centers:                                                   │
│   FOR each selected_center:                                    │
│     PRINT: id, lat, lon, land_type, slope, elevation           │
│                                                                 │
│ Total Cost: final_optimized_cost                                │
│                                                                 │
│ Assignments (Optional):                                         │
│   FOR each resource_point:                                     │
│     PRINT: resource_point_id → assigned_center_id              │
└─────────────────────────────────────────────────────────────────┘
```

## Algorithm Characteristics

### Complexity Analysis

```
Time Complexity: O(T × I × k × n × (k + n))
Where:
  T = Number of trials (10)
  I = Max iterations per trial (100)
  k = Number of centers to select
  n = Number of candidate zones

Space Complexity: O(n² + n×k)
Where:
  n² = Road network distance matrix
  n×k = Assignment and medoid storage
```

### Key Features

```
✓ Uses real road network distances (not Euclidean)
✓ Incorporates terrain constraints (slope, land type)
✓ Enforces minimum distance between centers
✓ Multiple random restarts to avoid local optima
✓ Weighted cost function (distance × resource quantity)
✓ Spatial optimization suitable for geographic data
```

### Why K-Medoids for This Problem?

```
1. Medoids are actual candidate locations (not centroids)
2. Robust to outliers in spatial data
3. Works with non-Euclidean distance metrics (road networks)
4. Handles constraints naturally during medoid selection
5. Scales well for moderate-sized facility location problems
```

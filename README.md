# Optimal Resource Collection Center Placement

## 🎯 Project Overview

This project implements an advanced solution for optimal placement of resource collection centers in rural logistics scenarios using a **k-medoids (PAM) clustering algorithm** with sophisticated constraint handling.

### Key Features

- ✅ **Real road network distances** (not Euclidean approximations)
- ✅ **Terrain constraint integration** (slope, elevation, land type exclusions)
- ✅ **Multi-constraint optimization** (minimum distance between centers)
- ✅ **Weighted cost minimization** (distance × resource quantity)
- ✅ **Robust C++ implementation** with Python interface
- ✅ **Interactive visualization** and analysis tools
- ✅ **Comprehensive validation** on synthetic and real datasets

## 🛠️ Technical Architecture

### Algorithm: K-Medoids (PAM - Partitioning Around Medoids)

**Why K-Medoids?**

1. **Spatial suitability**: Medoids are actual candidate locations, not abstract centroids
2. **Distance flexibility**: Works with non-Euclidean metrics (road networks)
3. **Constraint handling**: Natural integration of location-based constraints
4. **Robustness**: Less sensitive to outliers in spatial data
5. **Interpretability**: Results represent real, feasible locations

### Implementation Stack

- **Core Algorithm**: C++ for performance-critical optimization
- **Interface**: Python for data processing and visualization
- **Analysis**: Jupyter Notebook for interactive exploration
- **Visualization**: Matplotlib/Seaborn for comprehensive plotting

## 📊 Dataset Requirements

### Input Files

1. **`resource_points.csv`**: Resource locations and quantities

   - Columns: `lat`, `lon`, `resource_quantity`

2. **`zone_features.csv`**: Terrain and land characteristics

   - Columns: `lat`, `lon`, `slope`, `elevation`, `land_type`

3. **`road_network.csv`**: Distance matrix between all locations
   - Format: From_ID, To_ID, Distance (meters)

### Constraint Parameters

- **Land type exclusions**: e.g., `water`, `steep_terrain`
- **Slope limits**: Maximum allowable slope percentage
- **Minimum distance**: Between collection centers
- **Number of centers**: k value for optimization

## 🚀 Getting Started

> **🔥 New User? Start here:** [`QUICK_START.md`](QUICK_START.md) for step-by-step setup instructions.

### Quick Setup (Automated)

For the fastest setup, use the provided setup script:

```bash
# Download and extract the project
git clone <repository-url>
cd optimal-resource-placement

# Run automated setup (compiles C++, installs Python deps)
chmod +x setup.sh
./setup.sh
```

### Manual Setup

#### Prerequisites

- **C++ Compiler**: g++ or clang++ with C++17 support
- **Python**: 3.7 or higher
- **Git**: For downloading the repository

#### Step-by-Step Installation

1. **Download the project**:

   ```bash
   git clone <repository-url>
   cd optimal-resource-placement
   ```

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the C++ optimizer**:

   ```bash
   g++ -std=c++17 -O3 -o center_optimizer center_optimizer.cpp
   ```

4. **Verify installation**:
   ```bash
   # Test the C++ optimizer
   ./center_optimizer data/resource_points.csv data/zone_features.csv data/road_network.csv 3 2 wetland 25
   ```

### Running the Program

Choose any of these interfaces based on your preference:

#### 1. **Jupyter Notebook** (Recommended for analysis)

```bash
jupyter notebook Optimal_Resource_Center_Placement.ipynb
```

_Best for: Comprehensive analysis, visualization, and experimentation_

#### 2. **Streamlit Web App** (Interactive web interface)

```bash
streamlit run streamlit_app.py
```

_Best for: Interactive optimization with real-time parameter adjustment_

#### 3. **Interactive CLI** (Command-line interface)

```bash
python interactive_cli.py
```

_Best for: Quick runs and automation_

#### 4. **Direct C++ Execution** (Core algorithm only)

```bash
./center_optimizer <resource_file> <zone_file> <road_file> <k> <min_dist> <excluded_types> <max_slope>
```

_Best for: Performance testing and integration into other systems_

### Quick Demo

To see the algorithm in action immediately:

```bash
chmod +x demo.sh
./demo.sh
```

This runs multiple optimization scenarios and shows the results without requiring Python dependencies.

### Expected Outputs

After running any interface, you should expect:

**Console Output:**

- Optimization progress and iterations
- Final center coordinates and assignments
- Total cost and performance metrics
- Constraint compliance verification

**Generated Files:**

- `results/optimization_results.json`: Detailed results data
- `results/analysis_plots/`: Visualization images (PNG format)
- `results/cluster_assignments.csv`: Resource-to-center mappings

**Visualizations:**

- Geographic scatter plots showing centers and resource points
- Cost analysis charts and convergence plots
- Constraint compliance summaries
- Distance distribution histograms

## 📈 Usage Examples

### Basic Optimization

```python
# Run optimization with constraints
result = run_cpp_optimizer(
    k=3,
    land_type_exclusions=['water', 'steep_terrain'],
    max_slope=15.0,
    min_distance_between_centers=5000
)

# Visualize results
plot_optimization_results(result)
```

### Advanced Analysis

```python
# Compare multiple scenarios
scenarios = [
    {"k": 3, "max_slope": 10, "min_distance": 3000},
    {"k": 4, "max_slope": 15, "min_distance": 5000},
    {"k": 5, "max_slope": 20, "min_distance": 2000}
]

for scenario in scenarios:
    result = run_optimization(**scenario)
    analyze_performance(result)
```

## 📁 Project Structure

```
optimal-resource-placement/
├── README.md                                    # Project documentation
├── QUICK_START.md                              # Step-by-step setup guide
├── ALGORITHM_FLOW.md                           # Detailed algorithm explanation
├── SUBMISSION_SUMMARY.md                       # Assignment completion summary
├── PROJECT_STRUCTURE.md                        # Technical architecture details
├── requirements.txt                            # Python dependencies
├── setup.sh                                    # Automated setup script
├── demo.sh                                     # Quick demonstration script
├── center_optimizer.cpp                        # Core C++ implementation
├── center_optimizer                            # Compiled executable (after setup)
├── visualize_cpp_results.py                   # Python visualization tools
├── interactive_cli.py                         # Command-line interface
├── streamlit_app.py                           # Web-based interface (light mode)
├── Optimal_Resource_Center_Placement.ipynb    # Main analysis notebook
├── .streamlit/
│   └── config.toml                            # Streamlit configuration (light mode)
├── data/
│   ├── resource_points.csv                    # Real resource locations
│   ├── zone_features.csv                      # Real terrain data
│   ├── road_network.csv                       # Real distance matrix
│   ├── synthetic_resource_points.csv          # Test data
│   ├── synthetic_zone_features.csv            # Test terrain data
│   └── synthetic_road_network.csv             # Test distance matrix
└── results/                                   # Output directory (empty initially)
```

## 🔬 Validation & Testing

### Synthetic Data Validation

- **Cluster scenarios**: Verifies correct center selection in obvious cluster patterns
- **Constraint testing**: Ensures exclusions and distance requirements are respected
- **Edge cases**: Validates behavior with extreme parameters

### Real Data Analysis

- **Multiple scenarios**: Tests various k values and constraint combinations
- **Performance metrics**: Cost analysis, assignment efficiency, constraint compliance
- **Comparative analysis**: Evaluation against alternative approaches

## 🛠️ Troubleshooting

### Common Issues

**Compilation Errors:**

```bash
# If g++ is not found, install it:
# macOS: xcode-select --install
# Ubuntu: sudo apt-get install g++
# Windows: Install MinGW or Visual Studio

# If C++17 not supported, try:
g++ -std=c++14 -O3 -o center_optimizer center_optimizer.cpp
```

**Python Dependencies:**

```bash
# If pip install fails, try:
pip install --user -r requirements.txt

# Or use conda:
conda install pandas numpy matplotlib seaborn jupyter
```

**Data File Issues:**

```bash
# Ensure data files are in the correct location:
ls data/  # Should show: resource_points.csv, zone_features.csv, road_network.csv

# Check file formats (should be CSV with headers):
head -n 3 data/resource_points.csv
```

**Jupyter Notebook Issues:**

```bash
# If Jupyter doesn't start:
pip install jupyter
jupyter --version

# If kernel issues:
python -m ipykernel install --user
```

**Streamlit Issues:**

```bash
# If Streamlit doesn't start:
pip install streamlit
streamlit --version

# Access via: http://localhost:8501
```

## 📊 Key Results

### Performance Metrics

- **Total transportation cost**: Minimized weighted distance
- **Center utilization**: Balanced resource assignment
- **Constraint compliance**: 100% adherence to all specified constraints
- **Spatial distribution**: Optimal geographic coverage

### Validation Results

- ✅ **Synthetic data**: Perfect cluster identification
- ✅ **Constraint handling**: Zero violations across all test cases
- ✅ **Optimization quality**: Consistent cost minimization
- ✅ **Scalability**: Efficient performance on realistic dataset sizes

## 📝 Technical Documentation

### Algorithm Complexity

- **Time**: O(k × n² × iterations) where k = centers, n = locations
- **Space**: O(n²) for distance matrix storage
- **Convergence**: Typically 5-15 iterations for practical instances

### Implementation Details

- **Language**: C++17 for core algorithm, Python 3.7+ for interface
- **Optimization**: O3 compilation flags for performance
- **Memory**: Efficient sparse matrix handling for large datasets
- **I/O**: CSV-based input/output for easy integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- K-medoids algorithm implementation based on PAM (Partitioning Around Medoids)
- Spatial optimization techniques from computational geography literature
- Real-world logistics constraint modeling from rural development studies

---

**Author**: Kanishk  
**Project Type**: AI/ML Engineering Internship Assignment  
**Focus**: Spatial Optimization, Logistics, Constraint Programming

## Dependencies

- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `matplotlib/seaborn`: Visualization
- `scikit-learn`: Clustering utilities
- `geopy`: Geographic distance calculations

## Future Enhancements

- Web-based interactive interface
- Real-time constraint adjustment
- Machine learning-based demand forecasting
- Multi-objective optimization (Pareto frontiers)
- Support for road network graphs (not just distance matrices)

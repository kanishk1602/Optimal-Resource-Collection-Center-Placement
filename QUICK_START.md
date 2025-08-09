# 🚀 Quick Start Guide

This guide helps you get the Optimal Resource Center Placement project running immediately after downloading from GitHub.

## Step 1: Download and Setup

```bash
# Clone the repository
git clone <repository-url>
cd optimal-resource-placement

# Make setup script executable and run it
chmod +x setup.sh
./setup.sh
```

The setup script will:

- ✅ Check for C++ compiler and Python
- ✅ Compile the C++ optimizer
- ✅ Install Python dependencies
- ✅ Verify data files are present
- ✅ Create results directory

## Step 2: Choose Your Interface

### Option A: Jupyter Notebook (Recommended)

**Best for: Complete analysis and experimentation**

```bash
jupyter notebook Optimal_Resource_Center_Placement.ipynb
```

Then:

1. Run all cells sequentially (Cell → Run All)
2. Explore different scenarios by modifying parameters
3. View interactive visualizations and results

### Option B: Streamlit Web App

**Best for: Interactive parameter tuning**

```bash
streamlit run streamlit_app.py
```

Then:

1. Open your browser to http://localhost:8501 (or http://localhost:8502 if 8501 is busy)
2. The app will automatically open in light mode for optimal viewing
3. Adjust parameters using the sidebar controls
4. Click "Run Optimization" to see results
5. Download results and visualizations

### Option C: Interactive CLI

**Best for: Quick command-line access**

```bash
python interactive_cli.py
```

Then:

1. Follow the prompts to set parameters
2. View results in the terminal
3. Check the `results/` folder for saved outputs

### Option D: Direct C++ (Advanced)

**Best for: Integration and performance testing**

```bash
./center_optimizer data/resource_points.csv data/zone_features.csv data/road_network.csv 3 2 wetland 25
```

Parameters: `k_centers min_distance excluded_land_types max_slope`

## Step 3: View Results

After running any interface, check these locations:

- **Console**: Immediate optimization results
- **`results/optimization_results.json`**: Detailed data
- **`results/analysis_plots/`**: Visualization images
- **`results/cluster_assignments.csv`**: Resource assignments

## Quick Demo (No Python Required)

To see the core algorithm in action immediately:

```bash
chmod +x demo.sh
./demo.sh
```

This demonstrates the C++ optimizer with multiple scenarios.

## Troubleshooting

**If setup fails:**

```bash
# Check individual components
g++ --version          # Should show C++17 support
python3 --version      # Should be 3.7+
ls data/              # Should show CSV files
```

**If Jupyter doesn't start:**

```bash
pip install jupyter
jupyter --version
```

**If Streamlit doesn't start:**

```bash
pip install streamlit
streamlit --version
```

**If compilation fails:**

```bash
# Try alternative compiler flags
g++ -std=c++14 -O3 -o center_optimizer center_optimizer.cpp
```

## What to Expect

**Successful run should show:**

- ✅ Optimization progress and convergence
- ✅ Final center coordinates
- ✅ Total cost and assignments
- ✅ Constraint compliance verification
- ✅ Generated visualizations and data files

**Example output:**

```
Optimization completed in 8 iterations
Total cost: 245,678.5
Centers found: 3
All constraints satisfied: ✅
Results saved to: results/optimization_results.json
```

## Next Steps

1. **Experiment** with different parameters (k, constraints, slopes)
2. **Analyze** the generated visualizations and metrics
3. **Compare** multiple scenarios using the Jupyter notebook
4. **Export** results for use in other applications

## Support

For detailed information:

- **Algorithm details**: See `ALGORITHM_FLOW.md`
- **Technical specs**: See `PROJECT_STRUCTURE.md`
- **Assignment context**: See `SUBMISSION_SUMMARY.md`
- **Full documentation**: See `README.md`

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


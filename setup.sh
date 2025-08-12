#!/bin/bash

# Setup script for Optimal Resource Center Placement project
# This script sets up the environment and compiles the C++ optimizer

echo "🎯 Setting up Optimal Resource Center Placement project..."
echo "=================================================="

# Check if C++ compiler is available
echo "🔍 Checking for C++ compiler..."
if command -v g++ &> /dev/null; then
    echo "✅ g++ found"
    COMPILER="g++"
elif command -v clang++ &> /dev/null; then
    echo "✅ clang++ found"
    COMPILER="clang++"
else
    echo "❌ No C++ compiler found! Please install g++ or clang++"
    exit 1
fi

# Compile the C++ optimizer
echo "🔨 Compiling C++ optimizer..."
if $COMPILER -std=c++17 -O3 -o center_optimizer center_optimizer.cpp; then
    echo "✅ C++ optimizer compiled successfully"
else
    echo "❌ Failed to compile C++ optimizer"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python 3 found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    if [[ $PYTHON_VERSION == 3.* ]]; then
        echo "✅ Python 3 found: $PYTHON_VERSION"
        PYTHON_CMD="python"
    else
        echo "❌ Python 3 required, found $PYTHON_VERSION"
        exit 1
    fi
else
    echo "❌ Python not found! Please install Python 3.7+"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
if $PYTHON_CMD -m pip install -r requirements.txt; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    echo "   Try: pip install --user -r requirements.txt"
fi

# Check if data files exist and are in correct location
echo "📁 Checking data files..."
if [ -f "data/resource_points.csv" ] || [ -f "resource_points (1).csv" ]; then
    echo "✅ Resource points data found"
else
    echo "⚠️ Resource points data not found in expected locations"
fi

if [ -f "data/zone_features.csv" ] || [ -f "zone_features.csv" ]; then
    echo "✅ Zone features data found"
else
    echo "⚠️ Zone features data not found in expected locations"
fi

if [ -f "data/road_network.csv" ] || [ -f "road_network.csv" ]; then
    echo "✅ Road network data found"
else
    echo "⚠️ Road network data not found in expected locations"
fi

# Create results directory
echo "📂 Creating results directory..."
mkdir -p results
echo "✅ Results directory created"

echo ""
echo " Setup completed successfully!"
echo "=================================================="
echo ""
echo " Quick Start Options:"
echo ""
echo "   Run Streamlit Web App:"
echo "   streamlit run app.py"
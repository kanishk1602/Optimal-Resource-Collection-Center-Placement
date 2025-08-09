#!/usr/bin/env python3
"""
Comprehensive validation script for the Optimal Resource Center Placement project.
This script tests all components and ensures everything is working correctly.
"""

import os
import sys
import subprocess
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (NOT FOUND)")
        return False

def check_python_package(package_name: str) -> bool:
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        print(f"✅ Python package: {package_name}")
        return True
    except ImportError:
        print(f"❌ Python package: {package_name} (NOT INSTALLED)")
        return False

def test_cpp_compilation() -> bool:
    """Test if C++ optimizer compiles and runs"""
    try:
        # Check if already compiled
        if os.path.exists('./center_optimizer'):
            print("✅ C++ optimizer executable exists")
            return True
        
        # Try to compile
        result = subprocess.run(['g++', '-std=c++17', '-O3', '-o', 'center_optimizer', 'center_optimizer.cpp'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ C++ optimizer compiled successfully")
            return True
        else:
            print(f"❌ C++ compilation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ C++ compilation error: {e}")
        return False

def test_data_loading() -> Optional[Dict]:
    """Test loading of all required datasets"""
    data_files = {
        'resources': ['data/resource_points.csv', 'resource_points (1).csv'],
        'zones': ['data/zone_features.csv', 'zone_features.csv'],
        'roads': ['data/road_network.csv', 'road_network.csv']
    }
    
    datasets = {}
    all_loaded = True
    
    for name, file_paths in data_files.items():
        loaded = False
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    datasets[name] = df
                    print(f"✅ Loaded {name}: {file_path} ({len(df)} records)")
                    loaded = True
                    break
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        if not loaded:
            print(f"❌ Could not load {name} from any of: {file_paths}")
            all_loaded = False
    
    return datasets if all_loaded else None

def test_optimizer_execution(datasets: Dict) -> bool:
    """Test running the C++ optimizer"""
    try:
        # Determine file paths
        if os.path.exists('data/resource_points.csv'):
            cmd = ['./center_optimizer', 'data/resource_points.csv', 'data/zone_features.csv', 'data/road_network.csv', '2', '1', 'wetland', '30']
        else:
            cmd = ['./center_optimizer', 'resource_points (1).csv', 'zone_features.csv', 'road_network.csv', '2', '1', 'wetland', '30']
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ C++ optimizer executed successfully")
            
            # Parse output to verify it's working
            lines = result.stdout.strip().split('\n')
            centers_found = False
            for line in lines:
                if line.startswith('Best Centers'):
                    centers_found = True
                    break
            
            if centers_found:
                print("✅ Optimizer found valid centers")
                return True
            else:
                print("⚠️ Optimizer ran but no centers found in output")
                return False
        else:
            print(f"❌ Optimizer execution failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Optimizer execution timed out")
        return False
    except Exception as e:
        print(f"❌ Optimizer execution error: {e}")
        return False

def test_python_scripts() -> bool:
    """Test Python scripts can import and run basic functions"""
    scripts_to_test = [
        'visualize_cpp_results.py',
        'interactive_cli.py'
    ]
    
    all_passed = True
    
    for script in scripts_to_test:
        if os.path.exists(script):
            try:
                # Test basic import (syntax check)
                result = subprocess.run([sys.executable, '-m', 'py_compile', script], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ Python script syntax: {script}")
                else:
                    print(f"❌ Python script syntax error: {script}")
                    all_passed = False
            except Exception as e:
                print(f"❌ Error testing {script}: {e}")
                all_passed = False
        else:
            print(f"⚠️ Script not found: {script}")
    
    return all_passed

def test_streamlit_app() -> bool:
    """Test if Streamlit app can be imported"""
    try:
        if os.path.exists('streamlit_app.py'):
            result = subprocess.run([sys.executable, '-m', 'py_compile', 'streamlit_app.py'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Streamlit app syntax check passed")
                return True
            else:
                print(f"❌ Streamlit app syntax error: {result.stderr}")
                return False
        else:
            print("⚠️ Streamlit app not found")
            return False
    except Exception as e:
        print(f"❌ Error testing Streamlit app: {e}")
        return False

def test_notebook_files() -> bool:
    """Test if Jupyter notebook exists and is valid"""
    notebook_path = 'Optimal_Resource_Center_Placement.ipynb'
    
    if os.path.exists(notebook_path):
        try:
            import json
            with open(notebook_path, 'r') as f:
                notebook_data = json.load(f)
            
            if 'cells' in notebook_data and len(notebook_data['cells']) > 0:
                print(f"✅ Jupyter notebook valid: {len(notebook_data['cells'])} cells")
                return True
            else:
                print("❌ Jupyter notebook appears to be empty or invalid")
                return False
        except Exception as e:
            print(f"❌ Error reading notebook: {e}")
            return False
    else:
        print("❌ Jupyter notebook not found")
        return False

def main():
    """Run comprehensive validation"""
    print("🔍 Comprehensive Project Validation")
    print("=" * 50)
    
    # Test checklist
    tests = []
    
    # File existence checks
    print("\n📁 File Structure Validation:")
    tests.append(check_file_exists('center_optimizer.cpp', 'C++ optimizer source'))
    tests.append(check_file_exists('README.md', 'README documentation'))
    tests.append(check_file_exists('ALGORITHM_FLOW.md', 'Algorithm documentation'))
    tests.append(check_file_exists('requirements.txt', 'Python requirements'))
    tests.append(check_file_exists('setup.sh', 'Setup script'))
    tests.append(check_file_exists('LICENSE', 'License file'))
    
    # Python package checks
    print("\n📦 Python Dependencies:")
    required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn']
    for package in required_packages:
        tests.append(check_python_package(package))
    
    # Optional packages
    optional_packages = ['streamlit', 'plotly', 'jupyter']
    for package in optional_packages:
        check_python_package(package)  # Don't add to tests (optional)
    
    # C++ compilation test
    print("\n🔨 C++ Compilation:")
    tests.append(test_cpp_compilation())
    
    # Data loading test
    print("\n📊 Data Loading:")
    datasets = test_data_loading()
    tests.append(datasets is not None)
    
    # Optimizer execution test
    if datasets:
        print("\n⚡ Optimizer Execution:")
        tests.append(test_optimizer_execution(datasets))
    
    # Python scripts test
    print("\n🐍 Python Scripts:")
    tests.append(test_python_scripts())
    
    # Streamlit app test
    print("\n🌐 Web Application:")
    test_streamlit_app()  # Don't add to tests (optional)
    
    # Notebook test
    print("\n📓 Jupyter Notebook:")
    tests.append(test_notebook_files())
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(tests)
    total = len(tests)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("\n✅ Your project is ready for submission!")
        print("\n🚀 Quick start commands:")
        print("   • Setup: ./setup.sh")
        print("   • Notebook: jupyter notebook Optimal_Resource_Center_Placement.ipynb")
        print("   • Web app: streamlit run streamlit_app.py")
        print("   • CLI: python3 interactive_cli.py")
        return True
    else:
        print(f"⚠️ {passed}/{total} tests passed")
        print("\n❌ Some issues need to be resolved before submission.")
        print("   Run ./setup.sh to try fixing common issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

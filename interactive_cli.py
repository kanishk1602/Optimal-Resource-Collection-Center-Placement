#!/usr/bin/env python3
"""
Interactive CLI for Resource Center Optimization
Allows easy modification of constraints and re-running the optimization.
"""

import json
import os
import sys
from optimal_placement_solver import ResourceCenterOptimizer

def display_menu():
    """Display the main menu options."""
    print("\n" + "="*50)
    print("RESOURCE CENTER OPTIMIZATION - INTERACTIVE CLI")
    print("="*50)
    print("1. Run optimization with current constraints")
    print("2. View current constraints")
    print("3. Modify constraints")
    print("4. Reset constraints to default")
    print("5. Run optimization with visualization")
    print("6. Exit")
    print("-"*50)

def view_constraints(constraints_file='constraints.json'):
    """Display current constraints."""
    try:
        with open(constraints_file, 'r') as f:
            constraints = json.load(f)
        print("\nCurrent Constraints:")
        print("-"*20)
        for key, value in constraints.items():
            print(f"  {key}: {value}")
    except FileNotFoundError:
        print(f"Constraints file '{constraints_file}' not found.")

def modify_constraints(constraints_file='constraints.json'):
    """Allow user to modify constraints."""
    try:
        with open(constraints_file, 'r') as f:
            constraints = json.load(f)
    except FileNotFoundError:
        constraints = {
            "exclude_land_types": ["wetland"],
            "max_slope": 25,
            "min_distance_from_each_other_km": 2
        }
    
    print("\nModifying Constraints:")
    print("-"*20)
    
    # Modify exclude_land_types
    print(f"Current excluded land types: {constraints.get('exclude_land_types', [])}")
    print("Available land types: agricultural, urban, barren, forest, wetland")
    exclude_input = input("Enter land types to exclude (comma-separated, or press Enter to keep current): ").strip()
    if exclude_input:
        constraints['exclude_land_types'] = [t.strip() for t in exclude_input.split(',')]
    
    # Modify max_slope
    print(f"Current max slope: {constraints.get('max_slope', 25)}°")
    slope_input = input("Enter maximum slope (degrees, or press Enter to keep current): ").strip()
    if slope_input:
        try:
            constraints['max_slope'] = float(slope_input)
        except ValueError:
            print("Invalid slope value. Keeping current value.")
    
    # Modify min_distance
    print(f"Current minimum distance between centers: {constraints.get('min_distance_from_each_other_km', 2)} km")
    distance_input = input("Enter minimum distance between centers (km, or press Enter to keep current): ").strip()
    if distance_input:
        try:
            constraints['min_distance_from_each_other_km'] = float(distance_input)
        except ValueError:
            print("Invalid distance value. Keeping current value.")
    
    # Save updated constraints
    with open(constraints_file, 'w') as f:
        json.dump(constraints, f, indent=2)
    
    print(f"\nConstraints updated and saved to {constraints_file}")
    view_constraints(constraints_file)

def reset_constraints(constraints_file='constraints.json'):
    """Reset constraints to default values."""
    default_constraints = {
        "exclude_land_types": ["wetland"],
        "max_slope": 25,
        "min_distance_from_each_other_km": 2
    }
    
    with open(constraints_file, 'w') as f:
        json.dump(default_constraints, f, indent=2)
    
    print(f"\nConstraints reset to default values:")
    view_constraints(constraints_file)

def run_optimization(visualize=False):
    """Run the optimization process."""
    print("\nRunning optimization...")
    print("-"*20)
    
    # Check if required files exist
    required_files = [
        'resource_points (1).csv',
        'zone_features.csv',
        'road_network.csv',
        'constraints.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: Required file '{file}' not found.")
            return
    
    try:
        # Initialize optimizer
        optimizer = ResourceCenterOptimizer('constraints.json')
        
        # Load data
        optimizer.load_data('resource_points (1).csv', 'zone_features.csv', 'road_network.csv')
        
        # Apply constraints
        optimizer.apply_constraints()
        
        # Find optimal centers
        results = optimizer.find_optimal_centers(3)
        
        if results:
            # Explain results
            optimizer.explain_results()
            
            # Generate visualization if requested
            if visualize:
                optimizer.visualize_results()
                
            print(f"\nOptimization completed successfully!")
            
            # Offer to save results
            save_results = input("\nSave detailed results to file? (y/n): ").strip().lower()
            if save_results == 'y':
                save_results_to_file(optimizer)
        else:
            print("Failed to find optimal solution. Please check constraints.")
            
    except Exception as e:
        print(f"Error during optimization: {str(e)}")

def save_results_to_file(optimizer):
    """Save optimization results to a text file."""
    filename = "optimization_results.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("RESOURCE CENTER OPTIMIZATION RESULTS\n")
            f.write("="*50 + "\n\n")
            
            # Write constraints
            f.write("Applied Constraints:\n")
            f.write("-"*20 + "\n")
            for key, value in optimizer.constraints.items():
                f.write(f"  {key}: {value}\n")
            
            # Write optimal centers
            f.write(f"\nOptimal Center Locations:\n")
            f.write("-"*25 + "\n")
            for i, center_id in enumerate(optimizer.results['best_centers'], 1):
                details = optimizer.get_zone_details(center_id)
                f.write(f"\nRank {i}: Zone {center_id}\n")
                f.write(f"  Location: ({details['latitude']:.4f}, {details['longitude']:.4f})\n")
                f.write(f"  Land Type: {details['land_type']}\n")
                f.write(f"  Slope: {details['slope']:.1f}°\n")
                f.write(f"  Elevation: {details['elevation']:.1f}m\n")
                f.write(f"  Resource Quantity: {details['resource_quantity']}\n")
                f.write(f"  Accessibility Score: {details['accessibility_score']:.3f}\n")
            
            # Write alternative solutions
            f.write(f"\nAlternative Solutions (Top 5):\n")
            f.write("-"*30 + "\n")
            for i, eval_data in enumerate(optimizer.results['all_evaluations'][:5], 1):
                f.write(f"{i}. Centers {eval_data['centers']}\n")
                f.write(f"   Transportation Cost: {eval_data['transportation_cost']:.2f}\n")
                f.write(f"   Accessibility Score: {eval_data['accessibility_score']:.3f}\n")
                f.write(f"   Combined Score: {eval_data['combined_score']:.2f}\n\n")
        
        print(f"Results saved to '{filename}'")
        
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def main():
    """Main CLI loop."""
    print("Welcome to the Resource Center Optimization Tool!")
    
    while True:
        display_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                run_optimization(visualize=False)
            elif choice == '2':
                view_constraints()
            elif choice == '3':
                modify_constraints()
            elif choice == '4':
                reset_constraints()
            elif choice == '5':
                run_optimization(visualize=True)
            elif choice == '6':
                print("Thank you for using the Resource Center Optimization Tool!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()

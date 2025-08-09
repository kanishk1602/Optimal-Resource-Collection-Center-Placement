import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# Run the C++ optimizer and parse output
def run_cpp():
    # Try new data structure first, fallback to old
    if os.path.exists('data/resource_points.csv'):
        resource_file = 'data/resource_points.csv'
        zone_file = 'data/zone_features.csv'
        road_file = 'data/road_network.csv'
    else:
        resource_file = 'resource_points (1).csv'
        zone_file = 'zone_features.csv'
        road_file = 'road_network.csv'
    
    cmd = ['./center_optimizer', resource_file, zone_file, road_file, '3', '2', 'wetland', '25']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        return None, None
    lines = result.stdout.strip().split('\n')
    centers = []
    reading = False
    for line in lines:
        if line.startswith('Best Centers'):
            reading = True
            continue
        if line.startswith('Assignments:') or line.startswith('Total Cost:'):
            if line.startswith('Total Cost:'):
                total_cost = float(line.split(':')[1].strip())
            break
        if reading and line.strip():
            parts = line.split(',')
            if len(parts) >= 6:  # Ensure we have all required parts
                centers.append({
                    'id': int(parts[0]),
                    'lat': float(parts[1]),
                    'lon': float(parts[2]),
                    'land_type': parts[3],
                    'slope': float(parts[4]),
                    'elevation': float(parts[5])
                })
    
    # Find total cost if not found yet
    if 'total_cost' not in locals():
        for line in lines:
            if line.startswith('Total Cost:'):
                total_cost = float(line.split(':')[1].strip())
                break
    
    return centers, total_cost

def main():
    # Load data - try new structure first
    if os.path.exists('data/resource_points.csv'):
        resource_df = pd.read_csv('data/resource_points.csv')
        zone_df = pd.read_csv('data/zone_features.csv')
    else:
        resource_df = pd.read_csv('resource_points (1).csv')
        zone_df = pd.read_csv('zone_features.csv')
    centers, total_cost = run_cpp()
    if not centers:
        print('No centers found.')
        return
    center_ids = [c['id'] for c in centers]
    center_df = resource_df[resource_df['id'].isin(center_ids)]

    # Plot
    plt.figure(figsize=(10, 8))
    plt.scatter(resource_df['longitude'], resource_df['latitude'], s=resource_df['resource_quantity']/5, c='lightblue', label='Resource Points', alpha=0.6)
    plt.scatter(center_df['longitude'], center_df['latitude'], s=200, c='red', marker='*', label='Optimal Centers', edgecolors='black')
    for _, row in center_df.iterrows():
        plt.annotate(f"Center {row['id']}", (row['longitude'], row['latitude']), xytext=(5, 5), textcoords='offset points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Optimal Collection Centers (Total Cost: {total_cost:.0f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('cpp_optimal_centers.png', dpi=200)
    plt.show()

if __name__ == '__main__':
    main()

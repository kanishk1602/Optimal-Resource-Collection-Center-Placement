import streamlit as st
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from typing import List, Dict, Tuple, Optional

# Set page config with light theme
st.set_page_config(
    page_title="Optimal Resource Center Placement",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to force light mode and improve styling
st.markdown("""
<style>
    /* Force light mode */
    .stApp {
        background-color: white !important;
        color: black !important;
    }
    
    /* Force sidebar to light mode */
    .css-1d391kg {
        background-color: #f8f9fa !important;
    }
    
    /* Force main content area to light mode */
    .main > div {
        padding-top: 2rem;
        background-color: white !important;
        color: black !important;
    }
    
    /* Style metrics */
    .stMetric {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        color: black !important;
    }
    
    /* Success box styling */
    .success-box {
        background-color: #d4edda !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #155724 !important;
    }
    
    /* Force text colors */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
    
    /* Force dataframe styling */
    .stDataFrame {
        background-color: white !important;
        color: black !important;
    }
    
    /* Force button styling */
    .stButton > button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        border-radius: 0.375rem;
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        background-color: #0056b3 !important;
    }
    
    /* Force sidebar styling */
    .stSidebar {
        background-color: #f8f9fa !important;
    }
    
    .stSidebar .stMarkdown, .stSidebar .stText, .stSidebar p, .stSidebar h1, .stSidebar h2, .stSidebar h3 {
        color: black !important;
    }
    
    /* Force input styling */
    .stSlider, .stCheckbox, .stSelectbox {
        color: black !important;
    }
    
    /* Ensure tabs are visible */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f8f9fa !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: black !important;
        background-color: white !important;
    }
    
    /* Force expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: black !important;
    }
    
    /* Chart container styling */
    .stPlotlyChart {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

class OptimizationApp:
    def __init__(self):
        self.data_dir = "data"
        self.results_dir = "results"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure required directories exist"""
        for dir_path in [self.data_dir, self.results_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def load_data(self):
        """Load all required datasets"""
        try:
            resource_path = os.path.join(self.data_dir, "resource_points.csv")
            zone_path = os.path.join(self.data_dir, "zone_features.csv")
            road_path = os.path.join(self.data_dir, "road_network.csv")
            
            if os.path.exists(resource_path):
                resources = pd.read_csv(resource_path)
            else:
                # Fallback to old name
                resources = pd.read_csv("resource_points (1).csv")
                
            zones = pd.read_csv(zone_path)
            roads = pd.read_csv(road_path)
            
            return resources, zones, roads
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            return None, None, None
    
    def run_cpp_optimizer(self, k: int, min_distance: float, exclude_types: List[str], max_slope: float):
        """Run the C++ optimizer with specified parameters"""
        try:
            # Build command
            exclude_str = ",".join(exclude_types) if exclude_types else "none"
            cmd = [
                "./center_optimizer",
                os.path.join(self.data_dir, "resource_points.csv"),
                os.path.join(self.data_dir, "zone_features.csv"), 
                os.path.join(self.data_dir, "road_network.csv"),
                str(k),
                str(int(min_distance)),
                exclude_str,
                str(int(max_slope))
            ]
            
            # Fallback to old filename if new one doesn't exist
            if not os.path.exists(os.path.join(self.data_dir, "resource_points.csv")):
                cmd[1] = "resource_points (1).csv"
                cmd[2] = "zone_features.csv"
                cmd[3] = "road_network.csv"
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                st.error(f"Optimizer failed: {result.stderr}")
                return None, None, None
                
            return self.parse_cpp_output(result.stdout)
            
        except Exception as e:
            st.error(f"Error running optimizer: {str(e)}")
            return None, None, None
    
    def parse_cpp_output(self, output: str):
        """Parse C++ optimizer output"""
        lines = output.strip().split('\n')
        centers = []
        assignments = []
        total_cost = 0
        
        reading_centers = False
        reading_assignments = False
        
        for line in lines:
            if line.startswith('Best Centers'):
                reading_centers = True
                reading_assignments = False
                continue
            elif line.startswith('Assignments'):
                reading_centers = False
                reading_assignments = True
                continue
            elif line.startswith('Total Cost:'):
                total_cost = float(line.split(':')[1].strip())
                break
                
            if reading_centers and line.strip():
                parts = line.split(',')
                if len(parts) >= 6:
                    centers.append({
                        'id': int(parts[0]),
                        'lat': float(parts[1]),
                        'lon': float(parts[2]),
                        'land_type': parts[3],
                        'slope': float(parts[4]),
                        'elevation': float(parts[5])
                    })
            elif reading_assignments and line.strip():
                parts = line.split(' -> ')
                if len(parts) == 2:
                    resource_id = int(parts[0].split(':')[1].strip())
                    center_id = int(parts[1].split(':')[1].strip())
                    assignments.append({'resource_id': resource_id, 'center_id': center_id})
        
        return centers, assignments, total_cost
    
    def create_optimization_plot(self, resources_df, centers, assignments):
        """Create an interactive plot of optimization results"""
        if not centers:
            return None
            
        # Create subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Optimal Center Placement', 'Resource Distribution by Center', 
                          'Terrain Analysis', 'Assignment Statistics'),
            specs=[[{"secondary_y": False}, {"type": "pie"}],
                   [{"secondary_y": False}, {"type": "bar"}]]
        )
        
        # Main map plot
        fig.add_trace(
            go.Scatter(
                x=resources_df['longitude'],
                y=resources_df['latitude'],
                mode='markers',
                marker=dict(
                    size=resources_df['resource_quantity']/20,
                    color='lightblue',
                    opacity=0.6,
                    line=dict(width=1, color='darkblue')
                ),
                name='Resource Points',
                text=resources_df.apply(lambda x: f"ID: {x['id']}<br>Quantity: {x['resource_quantity']}", axis=1),
                hovertemplate='%{text}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Center locations
        center_df = pd.DataFrame(centers)
        if not center_df.empty:
            fig.add_trace(
                go.Scatter(
                    x=center_df['lon'],
                    y=center_df['lat'],
                    mode='markers+text',
                    marker=dict(
                        size=20,
                        color='red',
                        symbol='star',
                        line=dict(width=2, color='black')
                    ),
                    text=[f"C{c['id']}" for c in centers],
                    textposition="top center",
                    name='Optimal Centers',
                    hovertemplate='Center ID: %{text}<br>Location: (%{x:.4f}, %{y:.4f})<extra></extra>'
                ),
                row=1, col=1
            )
        
        # Resource distribution pie chart
        if assignments:
            assignment_df = pd.DataFrame(assignments)
            center_counts = assignment_df['center_id'].value_counts()
            fig.add_trace(
                go.Pie(
                    labels=[f"Center {cid}" for cid in center_counts.index],
                    values=center_counts.values,
                    name="Resource Distribution"
                ),
                row=1, col=2
            )
        
        # Terrain analysis (slope vs elevation)
        if 'slope' in resources_df.columns and 'elevation' in resources_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=resources_df['slope'],
                    y=resources_df['elevation'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=resources_df['resource_quantity'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Resource Quantity")
                    ),
                    name='Terrain Points',
                    hovertemplate='Slope: %{x}°<br>Elevation: %{y}m<extra></extra>'
                ),
                row=2, col=1
            )
        
        # Assignment statistics
        if assignments:
            stats_data = assignment_df['center_id'].value_counts().sort_index()
            fig.add_trace(
                go.Bar(
                    x=[f"Center {cid}" for cid in stats_data.index],
                    y=stats_data.values,
                    name='Points per Center',
                    marker_color='green'
                ),
                row=2, col=2
            )
        
        # Update layout for light mode
        fig.update_layout(
            height=800,
            title_text="Optimization Results Dashboard",
            showlegend=True,
            template="plotly_white",  # Force light theme
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="black"),
            title_font=dict(color="black", size=16)
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Longitude", row=1, col=1)
        fig.update_yaxes(title_text="Latitude", row=1, col=1)
        fig.update_xaxes(title_text="Slope (degrees)", row=2, col=1)
        fig.update_yaxes(title_text="Elevation (meters)", row=2, col=1)
        fig.update_xaxes(title_text="Centers", row=2, col=2)
        fig.update_yaxes(title_text="Number of Points", row=2, col=2)
        
        return fig

def main():
    app = OptimizationApp()
    
    # Title and header
    st.title("Optimal Resource Collection Center Placement")
    st.markdown("### Advanced K-Medoids Optimization with Terrain Constraints")
    
    # Sidebar for parameters
    with st.sidebar:
        st.header("Optimization Parameters")
        
        # Number of centers
        k = st.slider("Number of Centers (k)", min_value=1, max_value=10, value=3, 
                     help="Number of collection centers to place")
        
        # Minimum distance between centers
        min_distance = st.slider("Minimum Distance Between Centers (km)", 
                                min_value=0.5, max_value=20.0, value=2.0, step=0.5,
                                help="Minimum distance required between any two centers")
        
        # Maximum slope
        max_slope = st.slider("Maximum Slope (degrees)", 
                            min_value=5, max_value=45, value=25, step=5,
                            help="Maximum allowable slope for center placement")
        
        # Land type exclusions
        st.subheader("Land Type Exclusions")
        exclude_wetland = st.checkbox("Exclude Wetland", value=True)
        exclude_water = st.checkbox("Exclude Water Bodies", value=False)
        exclude_steep = st.checkbox("Exclude Steep Terrain", value=False)
        exclude_urban = st.checkbox("Exclude Urban Areas", value=False)
        
        exclude_types = []
        if exclude_wetland:
            exclude_types.append("wetland")
        if exclude_water:
            exclude_types.append("water")
        if exclude_steep:
            exclude_types.append("steep_terrain")
        if exclude_urban:
            exclude_types.append("urban")
        
        # Run optimization button
        run_optimization = st.button("Run Optimization", type="primary")
    
    
    # Optimization results
    if run_optimization:
        st.header("Optimization Results")
        
        with st.spinner("Running optimization algorithm..."):
            centers, assignments, total_cost = app.run_cpp_optimizer(
                k=k,
                min_distance=min_distance,
                exclude_types=exclude_types,
                max_slope=max_slope
            )
        
        if centers:
            # Success message
            st.markdown(f"""
            <div class="success-box">
                <h3>Optimization Completed Successfully!</h3>
                <p><strong>Total Transportation Cost:</strong> {total_cost:,.0f} units</p>
                <p><strong>Centers Found:</strong> {len(centers)}</p>
                <p><strong>Assignments Made:</strong> {len(assignments) if assignments else 0}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Results tabs
            tab1, tab2, tab3 = st.tabs(["Center Locations", "Visualization", "Detailed Results"])
            
            with tab1:
                st.subheader("Optimal Center Locations")
                centers_df = pd.DataFrame(centers)
                st.dataframe(centers_df, use_container_width=True)
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_slope = centers_df['slope'].mean()
                    st.metric("Average Slope", f"{avg_slope:.1f}°")
                with col2:
                    avg_elevation = centers_df['elevation'].mean()
                    st.metric("Average Elevation", f"{avg_elevation:.1f}m")
                with col3:
                    land_types = centers_df['land_type'].unique()
                    st.metric("Land Types Used", len(land_types))
            
            with tab2:
                st.subheader("Interactive Visualization")
                
                # Ensure resources_df is loaded before use
                resources_df, zones_df, roads_df = app.load_data()

                if resources_df is None or zones_df is None or roads_df is None:
                    st.error("Failed to load required data files. Please check the data directory.")
                    return

                fig = app.create_optimization_plot(resources_df, centers, assignments)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                st.subheader("Detailed Assignment Results")
                if assignments:
                    assignments_df = pd.DataFrame(assignments)
                    
                    # Merge with resource data for detailed view
                    detailed_assignments = assignments_df.merge(
                        resources_df[['id', 'latitude', 'longitude', 'resource_quantity']], 
                        left_on='resource_id', right_on='id', how='left'
                    )
                    
                    st.dataframe(detailed_assignments, use_container_width=True)
                    
        else:
            st.error("Optimization failed. Please check parameters and try again.")
    
    # Add explanation for cost calculation
    st.markdown("### Basis of Cost Calculation")
    st.markdown("""
    The cost in the k-medoids algorithm is calculated based on the following factors:

    1. **Distance Metric**: The algorithm uses real road network distances to compute the cost. This ensures that the placement of resource collection centers is optimized based on actual travel distances.

    2. **Constraints**: Terrain and land constraints are factored into the cost calculation. If a medoid is placed in an area that violates constraints, a penalty is added to the cost.

    3. **Cluster Assignment**: Each resource point is assigned to the nearest medoid based on the distance metric. The cost for each cluster is the sum of distances from all resource points in the cluster to the medoid.

    4. **Total Cost**: The total cost is the sum of costs for all clusters, including penalties for constraint violations.
    """)
    

    # Footer
    st.markdown("---")
    st.markdown("### About This Application")
    st.markdown("""
    This application uses a **K-Medoids (PAM) clustering algorithm** implemented in C++ for optimal placement 
    of resource collection centers. The algorithm considers:
    
    - Terrain constraints (slope, elevation, land type)
    - Minimum distance requirements between centers
    - Weighted transportation cost optimization
    
    **Algorithm Complexity:** O(k × n² × iterations) where k = centers, n = locations
    """)

if __name__ == "__main__":
    main()

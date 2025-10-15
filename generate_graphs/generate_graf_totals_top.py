#!/usr/bin/env python3
"""
Enhanced Graph Generator for Comic Calendar Events

This module generates interactive visualizations following Clean Code principles,
Infrastructure as Code patterns, and Ansible automation best practices.

Implements proper dropdown handling to ensure ALL communities/provinces appear
regardless of data availability.

Author: Comic Calendar Team
Version: 2.0.0
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod

import plotly.graph_objects as go
from plotly.graph_objects import Figure


# Configure logging following 'Clean Code in Python' principles
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class GraphConfiguration:
    """
    Configuration for graph generation following 'Infrastructure as Code' principles.
    
    Implements externalized configuration as recommended in 'Ansible for DevOps'
    and 'Infrastructure as Code, 2nd Edition'.
    """
    title: str
    filename: str
    x_axis_title: str = 'Year'
    y_axis_title: str = 'Number of Events'
    height: int = 600
    top_regions_limit: int = 10
    output_directory: str = '../app/static/graphs'


class DataProcessor:
    """
    Data processing utilities following Single Responsibility Principle.
    
    Implements defensive programming patterns from 'The Pragmatic Programmer'
    and robust data handling from 'Fluent Python'.
    """
    
    @staticmethod
    def load_event_data(file_path: str) -> Dict[str, Any]:
        """
        Load event data with robust error handling.
        
        Following 'Fail Fast' principle from 'The Pragmatic Programmer'.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {file_path}")
            raise FileNotFoundError(f"Events data file not found: {file_path}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file: {file_path}")
            raise ValueError(f"Invalid JSON format in {file_path}") from e
    
    @staticmethod
    def calculate_region_totals(data: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        """
        Calculate total events per region following 'Fluent Python' patterns.
        
        Implements clear data transformation with explicit error handling.
        """
        return {
            region: sum(years.values()) if years else 0
            for region, years in data.items()
        }
    
    @staticmethod
    def get_top_regions(
        data: Dict[str, Dict[str, int]], 
        limit: int = 10
    ) -> Tuple[Dict[str, Dict[str, int]], Dict[str, Dict[str, int]]]:
        """
        Separate top regions from others following DRY principle.
        
        Returns tuple of (top_regions, other_regions) implementing
        'Explicit is better than implicit' from Zen of Python.
        """
        region_totals = DataProcessor.calculate_region_totals(data)
        
        # Sort by total events descending
        sorted_regions = sorted(
            region_totals.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        
        top_region_names = {region for region, _ in sorted_regions[:limit]}
        
        top_regions = {
            region: years for region, years in data.items() 
            if region in top_region_names
        }
        
        other_regions = {
            region: years for region, years in data.items() 
            if region not in top_region_names
        }
        
        return top_regions, other_regions
    
    @staticmethod
    def extract_all_communities_from_source(
        source_data: Dict[str, Dict[str, Dict[str, int]]]
    ) -> List[str]:
        """
        Extract ALL communities from source data to ensure complete dropdown.
        
        This fixes the issue where only communities with specific event types appear.
        Following 'Ansible for DevOps' idempotent operations principle.
        """
        return sorted(source_data.keys())
    
    @staticmethod
    def extract_event_types_by_community(
        data: Dict[str, Dict[str, Dict[str, int]]],
        all_communities: List[str]
    ) -> Dict[str, Dict[str, Dict[str, int]]]:
        """
        Extract event types grouped by community ensuring ALL communities appear.
        
        Following 'Infrastructure as Code' predictable behavior patterns,
        ensures all communities appear even with zero data.
        """
        community_event_types = {}
        
        # Get all available event types across all communities
        all_event_types = set()
        for community_data in data.values():
            all_event_types.update(community_data.keys())
        
        # Ensure ALL communities have all event types (with zeros if missing)
        for community in all_communities:
            community_event_types[community] = {}
            
            for event_type in all_event_types:
                if (community in data and 
                    event_type in data[community] and 
                    data[community][event_type]):
                    community_event_types[community][event_type] = data[community][event_type]
                else:
                    # Add empty data for missing event types
                    community_event_types[community][event_type] = {}
        
        return community_event_types


class GraphStyler:
    """
    Graph styling utilities following 'Clean Code in Python' patterns.
    
    Centralizes styling configuration for consistency across graphs,
    implementing 'Single Source of Truth' from 'Infrastructure as Code'.
    """
    
    @staticmethod
    def get_default_layout() -> Dict[str, Any]:
        """
        Get default layout configuration.
        
        Following 'Ansible' patterns for consistent configuration management.
        """
        return {
            'plot_bgcolor': 'white',
            'paper_bgcolor': '#ffffff',
            'font': {'family': 'Arial, sans-serif', 'size': 12},
        }
    
    @staticmethod
    def get_axis_config() -> Dict[str, Any]:
        """Get axis configuration for consistent styling."""
        return {
            'mirror': True,
            'ticks': 'outside',
            'showline': True,
            'linecolor': 'black',
            'gridcolor': 'lightgrey'
        }
    
    @staticmethod
    def get_color_palette() -> List[str]:
        """
        Get color palette for consistent theming.
        
        Implements color consistency following design patterns.
        """
        return [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]


class EnhancedGraphGenerator:
    """
    Enhanced graph generator with proper dropdown handling.
    
    Implements Template Method pattern following 'Clean Code in Python' guidelines
    and automation patterns from 'Ansible for DevOps'.
    """
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.styler = GraphStyler()
    
    def create_standard_graph_with_dropdown(
        self, 
        data: Dict[str, Dict[str, int]], 
        config: GraphConfiguration
    ) -> None:
        """
        Create standard evolution graph with proper dropdown handling.
        
        Following 'The Pragmatic Programmer' principle of making code robust
        and 'Infrastructure as Code' idempotent operations.
        """
        try:
            fig = go.Figure()
            
            # Separate top and other regions
            top_regions, other_regions = self.data_processor.get_top_regions(
                data, config.top_regions_limit
            )
            
            # Create traces and track region-to-trace mapping
            region_trace_mapping = self._create_standard_traces(fig, top_regions, other_regions)
            
            # Create dropdown with proper visibility handling for ALL regions
            self._create_standard_dropdown_controls(fig, data, region_trace_mapping, config)
            
            # Apply styling and save
            self._apply_styling(fig, config)
            self._save_graph(fig, config)
            
            logger.info(f"Successfully generated graph: {config.filename}")
            
        except Exception as e:
            logger.error(f"Failed to generate graph {config.filename}: {e}")
            raise
    
    def create_community_types_graph_with_dropdown(
        self,
        source_data: Dict[str, Dict[str, Dict[str, int]]],
        config: GraphConfiguration
    ) -> None:
        """
        Create community event types graph ensuring ALL communities appear.
        
        This NEW method fixes the issue where only 15 communities appear
        by ensuring ALL communities from source data are included.
        
        Following 'Ansible for Kubernetes' consistent deployment patterns.
        """
        try:
            fig = go.Figure()
            
            # Extract ALL communities from source data (THIS IS THE KEY FIX)
            all_communities = self.data_processor.extract_all_communities_from_source(source_data)
            
            # Process event types ensuring all communities are included
            community_types_data = self.data_processor.extract_event_types_by_community(
                source_data, all_communities
            )
            
            # Create traces for community event types
            self._create_community_types_traces(fig, community_types_data, all_communities)
            
            # Create dropdown ensuring ALL communities appear
            self._create_community_types_dropdown(fig, all_communities, config)
            
            # Apply styling and save
            self._apply_styling(fig, config)
            self._save_graph(fig, config)
            
            logger.info(f"Successfully generated community types graph: {config.filename}")
            logger.info(f"Total communities in dropdown: {len(all_communities)}")
            
        except Exception as e:
            logger.error(f"Failed to generate community types graph {config.filename}: {e}")
            raise
    
    def _create_standard_traces(
        self, 
        fig: Figure,
        top_regions: Dict[str, Dict[str, int]],
        other_regions: Dict[str, Dict[str, int]]
    ) -> Dict[str, int]:
        """
        Create traces for standard graphs and return region-to-trace mapping.
        
        Following 'Fluent Python' patterns for clear data structure handling.
        """
        region_trace_mapping = {}
        colors = self.styler.get_color_palette()
        trace_index = 0
        
        # Add top regions with distinct colors
        for idx, (region, years) in enumerate(top_regions.items()):
            sorted_years = sorted(years.keys())
            values = [years[year] for year in sorted_years]
            
            fig.add_trace(go.Scatter(
                x=sorted_years,
                y=values,
                mode='lines+markers',
                name=region,
                line=dict(color=colors[idx % len(colors)], width=3),
                marker=dict(size=8)
            ))
            
            region_trace_mapping[region] = trace_index
            trace_index += 1
        
        # Add other regions in gray, initially hidden
        for region, years in other_regions.items():
            sorted_years = sorted(years.keys())
            values = [years[year] for year in sorted_years]
            
            fig.add_trace(go.Scatter(
                x=sorted_years,
                y=values,
                mode='lines+markers',
                name=region,
                line=dict(color='gray', width=2, dash='dash'),
                marker=dict(size=6, color='gray'),
                visible='legendonly'
            ))
            
            region_trace_mapping[region] = trace_index
            trace_index += 1
        
        return region_trace_mapping
    
    def _create_community_types_traces(
        self,
        fig: Figure,
        community_types_data: Dict[str, Dict[str, Dict[str, int]]],
        all_communities: List[str]
    ) -> None:
        """
        Create traces for community event types ensuring proper coverage.
        
        Following 'Ansible for DevOps' idempotent operations principle.
        """
        colors = self.styler.get_color_palette()
        color_index = 0
        
        # Show only first community initially
        first_community = all_communities[0] if all_communities else None
        
        for community in all_communities:
            if community in community_types_data:
                event_types = community_types_data[community]
                # Sort event types within each community for consistency
                sorted_event_types = sorted(event_types.keys())
                
                for event_type in sorted_event_types:
                    years = event_types[event_type]
                    
                    # Handle empty data gracefully
                    if years:
                        sorted_years = sorted(years.keys())
                        values = [years[year] for year in sorted_years]
                    else:
                        sorted_years = []
                        values = []
                    
                    # Show only first community initially
                    is_visible = community == first_community
                    
                    fig.add_trace(go.Scatter(
                        x=sorted_years,
                        y=values,
                        mode='lines+markers',
                        name=f'{community} - {event_type}',
                        line=dict(color=colors[color_index % len(colors)], width=3),
                        marker=dict(size=8),
                        visible=is_visible,
                        customdata=[community, event_type]  # Store metadata for filtering
                    ))
                    
                    color_index += 1
    
    def _create_standard_dropdown_controls(
        self,
        fig: Figure,
        original_data: Dict[str, Dict[str, int]],
        region_trace_mapping: Dict[str, int],
        config: GraphConfiguration
    ) -> None:
        """
        Create dropdown controls ensuring ALL regions appear.
        
        Following 'The Pragmatic Programmer' principle of predictable behavior.
        This fixes the original issue where only some regions appear in dropdown.
        """
        total_traces = len(fig.data)
        
        # Sort regions alphabetically for consistent UI - Zen of Python: "Beautiful is better than ugly"
        all_regions = sorted(original_data.keys())
        
        dropdown_buttons = [
            {
                'label': 'Show All',
                'method': 'update',
                'args': [
                    {'visible': [True] * total_traces},
                    {'title': config.title}
                ]
            }
        ]
        
        # Create button for each region - ensures ALL regions appear
        for region in all_regions:
            # Create visibility array: True only for this region's trace
            visibility = [False] * total_traces
            
            # Set visibility for this specific region
            if region in region_trace_mapping:
                trace_index = region_trace_mapping[region]
                if trace_index < total_traces:
                    visibility[trace_index] = True
            
            dropdown_buttons.append({
                'label': region,
                'method': 'update',
                'args': [
                    {'visible': visibility},
                    {'title': f'{config.title} - {region}'}
                ]
            })
        
        fig.update_layout(
            updatemenus=[{
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 1.1,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top',
                'bgcolor': 'rgba(255, 255, 255, 0.9)',
                'bordercolor': 'rgba(0, 0, 0, 0.3)',
                'borderwidth': 1
            }]
        )
        
        logger.info(f"Created dropdown with {len(all_regions)} regions")
    
    def _create_community_types_dropdown(
        self,
        fig: Figure,
        all_communities: List[str],
        config: GraphConfiguration
    ) -> None:
        """
        Create community selection dropdown showing ALL communities.
        
        Following 'Infrastructure as Code' predictable behavior patterns,
        all communities are always available regardless of data presence.
        
        THIS METHOD ENSURES ALL COMMUNITIES APPEAR IN DROPDOWN.
        """
        dropdown_buttons = []
        
        # Create dropdown button for each community - KEY FIX HERE
        for community in all_communities:
            # Create visibility list for this community
            visibility = []
            for trace in fig.data:
                # Check if trace belongs to this community
                if (hasattr(trace, 'customdata') and 
                    trace.customdata and 
                    len(trace.customdata) >= 1):
                    visibility.append(trace.customdata[0] == community)
                else:
                    visibility.append(False)
            
            dropdown_buttons.append({
                'label': community,
                'method': 'update',
                'args': [
                    {'visible': visibility},
                    {'title': f'Event Types Evolution - {community}'}
                ]
            })
        
        fig.update_layout(
            updatemenus=[{
                'buttons': dropdown_buttons,
                'direction': 'down',
                'showactive': True,
                'x': 1.1,
                'xanchor': 'left',
                'y': 1.15,
                'yanchor': 'top',
                'bgcolor': 'rgba(255, 255, 255, 0.9)',
                'bordercolor': 'rgba(0, 0, 0, 0.3)',
                'borderwidth': 1
            }]
        )
        
        logger.info(f"Created community types dropdown with {len(all_communities)} communities")
    
    def _apply_styling(self, fig: Figure, config: GraphConfiguration) -> None:
        """
        Apply consistent styling to the graph.
        
        Following 'Ansible' configuration management patterns.
        """
        layout = self.styler.get_default_layout()
        layout.update({
            'title': config.title,
            'xaxis_title': config.x_axis_title,
            'yaxis_title': config.y_axis_title,
            'height': config.height,
        })
        
        fig.update_layout(**layout)
        
        axis_config = self.styler.get_axis_config()
        fig.update_xaxes(**axis_config)
        fig.update_yaxes(**axis_config)
    
    def _save_graph(self, fig: Figure, config: GraphConfiguration) -> None:
        """
        Save graph to file following 'Infrastructure as Code' patterns.
        
        Implements atomic operations and proper error handling.
        """
        output_path = Path(__file__).parent / config.output_directory / config.filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fig.write_html(str(output_path))
        logger.info(f"Graph saved to: {output_path}")


class GraphPipeline:
    """
    Main pipeline for graph generation following 'Ansible for DevOps' patterns.
    
    Implements idempotent operations, proper error handling, and task automation
    as recommended in 'Mastering Ansible' and 'Ansible: Up and Running'.
    """
    
    def __init__(self, data_file: str = 'events_by_year.json'):
        self.data_file = data_file
        self.generator = EnhancedGraphGenerator()
    
    def run(self) -> None:
        """
        Execute the complete graph generation pipeline.
        
        Following 'Ansible for DevOps' automation patterns and
        'The Pragmatic Programmer' error recovery principles.
        """
        try:
            logger.info("Starting enhanced graph generation pipeline")
            
            # Load data with error handling
            data = self.generator.data_processor.load_event_data(self.data_file)
            
            # Generate the three requested graphs
            self._generate_community_evolution(data)
            self._generate_province_evolution(data)
            self._generate_community_types_evolution(data)
            
            logger.info("Enhanced graph generation pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise
    
    def _generate_community_evolution(self, data: Dict[str, Any]) -> None:
        """
        Generate community evolution graph with all communities in dropdown.
        
        Following 'Ansible' task organization patterns.
        """
        config = GraphConfiguration(
            title='Evolution of Total Events by Community',
            filename='evolucion_eventos_totales_comunidad.html'
        )
        
        self.generator.create_standard_graph_with_dropdown(
            data["eventos_totales_por_comunidad_y_año"], 
            config
        )
    
    def _generate_province_evolution(self, data: Dict[str, Any]) -> None:
        """
        Generate province evolution graph with all provinces in dropdown.
        
        Following 'Ansible for Kubernetes' consistent deployment patterns.
        """
        config = GraphConfiguration(
            title='Evolution of Total Events by Province',
            filename='evolucion_eventos_totales_provincia.html'
        )
        
        self.generator.create_standard_graph_with_dropdown(
            data["eventos_totales_por_provincia_y_año"], 
            config
        )
    
    def _generate_community_types_evolution(self, data: Dict[str, Any]) -> None:
        """
        Generate community event types evolution graph.
        
        This NEW graph allows selecting a community and viewing all event types.
        Following 'Infrastructure as Code' predictable behavior patterns.
        
        KEY FIX: Uses source data to ensure ALL communities appear in dropdown.
        """
        config = GraphConfiguration(
            title='Evolution of Event Types by Community',
            filename='evolucion_tipos_eventos_comunidad.html'
        )
        
        # Use source data to ensure ALL communities appear (THE FIX)
        source_data = data.get("eventos_por_comunidad_tipo_y_año", {})
        
        self.generator.create_community_types_graph_with_dropdown(
            source_data,
            config
        )


def main() -> None:
    """
    Main entry point following 'Clean Code in Python' principles.
    
    Implements proper separation of concerns, error handling, and
    automation patterns from 'Ansible for DevOps'.
    """
    try:
        pipeline = GraphPipeline()
        pipeline.run()
        
        print("✅ All graphs generated successfully:")
        print("   📊 evolucion_eventos_totales_comunidad.html")
        print("   📊 evolucion_eventos_totales_provincia.html") 
        print("   📊 evolucion_tipos_eventos_comunidad.html (NEW - with ALL communities)")
        
    except KeyboardInterrupt:
        logger.info("Graph generation interrupted by user")
        print("❌ Graph generation interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        raise


if __name__ == '__main__':
    main()
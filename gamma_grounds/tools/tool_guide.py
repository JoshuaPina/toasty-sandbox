#!/usr/bin/env python3
# tools/tool_guide.py
# ---------------------------------------------------------
# DESCRIPTION: Auto-generates a Rich table guide for all EDA tools
# USAGE: from tools import tool_guide; tool_guide.show_guide()
# ---------------------------------------------------------

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Define all available tools and their metadata
TOOL_REGISTRY = {
    "check_eda_env": {
        "category": "Env Setup",
        "functions": [
            {
                "name": "eda_env()",
                "description": "Check EDA Environment for essential packages"
            }
        ]
    },
    "eda_starter": {
        "category": "EDA Util",
        "functions": [
            {
                "name": "set_styles()",
                "description": "Set Global Config (pandas, seaborn)"
            },
            {
                "name": "check_missing(df)",
                "description": "Check for missing values in DF"
            },
            {
                "name": "visualize_missing(df)",
                "description": "Visualize missing data patterns in DF"
            },
            {
                "name": "check_sparsity(df, target_col)",
                "description": "Check DF to determine if 0-inflated"
            },
            {
                "name": "inspect_categories(df, top_n=10)",
                "description": "Shows top values for cat-features (NPU, Zone)"
            },
            {
                "name": "plot_distributions(df, numeric_cols=None)",
                "description": "Plots histograms for numerical data"
            },
            {
                "name": "plot_correlation_matrix(df)",
                "description": "Plot correlation mat for num-features in DF"
            },
            {
                "name": "plot_boxplots(df, numeric_cols=None)",
                "description": "Plots boxplots for num-data to identify outliers"
            }
        ]
    },
    "eda_data_quality": {
        "category": "Data Quality",
        "functions": [
            {
                "name": "check_duplicates(df, subset=None)",
                "description": "Identify duplicate records in DF"
            },
            {
                "name": "check_date_gaps(df, date_col, freq='D')",
                "description": "Find missing time periods in temporal data"
            },
            {
                "name": "validate_coordinates(df, lat_col, lon_col)",
                "description": "Check if lat/lon are in valid ranges (ATL default)"
            }
        ]
    },
    "eda_crime_analysis": {
        "category": "Crime Analysis",
        "functions": [
            {
                "name": "temporal_patterns(df, date_col, freq='M')",
                "description": "Analyze crime trends over time with visualization"
            },
            {
                "name": "spatial_summary(df, groupby_col='npu')",
                "description": "Crime counts by geography (NPU, Zone, Beat)"
            },
            {
                "name": "crime_type_distribution(df, crime_col)",
                "description": "Distribution of crime types with pie/bar charts"
            }
        ]
    },
    "eda_feature_engineering": {
        "category": "Feature Eng",
        "functions": [
            {
                "name": "create_time_features(df, date_col)",
                "description": "Extract year, month, day, hour, cyclical features"
            },
            {
                "name": "flag_outliers(df, cols, method='iqr')",
                "description": "Flag outliers using IQR or Z-score method"
            },
            {
                "name": "encode_categories(df, cols, method='onehot')",
                "description": "One-hot or label encode categorical variables"
            },
            {
                "name": "create_interaction_features(df, col1, col2)",
                "description": "Create interaction terms (multiply, add, etc.)"
            }
        ]
    }
}

def show_guide(detailed=False):
    """
    Displays a Rich table of all available EDA functions.
    
    Args:
        detailed (bool): If True, shows extended descriptions and usage tips
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Tool/Script", style="dim", width=20)
    table.add_column("Category", style="italic", width=13)
    table.add_column("Function", style="italic", width=35)
    table.add_column("Description", style="bold cyan", justify="left")
    
    for tool_name, tool_data in TOOL_REGISTRY.items():
        category = tool_data["category"]
        for func in tool_data["functions"]:
            table.add_row(
                tool_name,
                category,
                func["name"],
                func["description"]
            )
    
    console.print(Panel(table, title="Available Tools in 'tools' Folder", subtitle="Function Key", border_style="green"))
    
    if detailed:
        console.print("\n[bold cyan]Usage Tips:[/bold cyan]")
        console.print("• Import: [yellow]from tools import eda_starter, eda_crime_analysis[/yellow]")
        console.print("• Run missing check: [yellow]eda_starter.check_missing(df)[/yellow]")
        console.print("• Temporal analysis: [yellow]eda_crime_analysis.temporal_patterns(df, 'occur_date')[/yellow]")
        console.print("• Feature engineering: [yellow]eda_feature_engineering.create_time_features(df, 'occur_date')[/yellow]")
        console.print("• Visualizations automatically display inline in Jupyter\n")

def add_function(tool_name, category, function_name, description):
    """
    Dynamically add a new function to the registry.
    
    Args:
        tool_name (str): Name of the tool module
        category (str): Category (e.g., "EDA Util", "Modeling")
        function_name (str): Function signature (e.g., "my_func(df)")
        description (str): What the function does
    """
    if tool_name not in TOOL_REGISTRY:
        TOOL_REGISTRY[tool_name] = {
            "category": category,
            "functions": []
        }
    
    TOOL_REGISTRY[tool_name]["functions"].append({
        "name": function_name,
        "description": description
    })
    
    console.print(f"[green]✔ Added {function_name} to {tool_name}[/green]")

def list_categories():
    """Quick view of available categories."""
    categories = set(tool["category"] for tool in TOOL_REGISTRY.values())
    console.print("[bold]Available Categories:[/bold]")
    for cat in sorted(categories):
        console.print(f"  • {cat}")

def list_tools():
    """List all available tool modules."""
    console.print("[bold]Available Tool Modules:[/bold]")
    for tool in sorted(TOOL_REGISTRY.keys()):
        func_count = len(TOOL_REGISTRY[tool]["functions"])
        console.print(f"  • [cyan]{tool}[/cyan] ({func_count} functions)")

# Convenience alias
display = show_guide
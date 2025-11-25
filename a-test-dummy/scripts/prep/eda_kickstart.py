#!/usr/bin/env python3
# eda_starter.py
# ---------------------------------------------------------
# DESCRIPTION: [EDA Boilerplate] Standard imports and helper functions for initial data analysis.
# NOTE: Used in "Burglary Risk" and "Ticket Prediction" projects.
# ---------------------------------------------------------
# USAGE: import eda_starter as eda -> eda.check_missing(df)
# ---------------------------------------------------------
# DEPENDENCIES:
#   pip install pandas seaborn matplotlib rich
# ---------------------------------------------------------

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

console = Console()

# --- Standard Configuration ---
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
sns.set_theme(style="whitegrid")

def check_missing(df: pd.DataFrame):
    """
    Calculates missing values and displays a Rich table.
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    
    if missing.empty:
        console.print("[bold green]No missing values found![/bold green]")
        return

    # Calculate percentages
    total_rows = len(df)
    missing_percent = (missing / total_rows) * 100
    
    # Create Rich Table
    table = Table(title=f"Missing Values Report (N={total_rows})", border_style="yellow")
    table.add_column("Column", style="cyan")
    table.add_column("Missing Count", justify="right", style="white")
    table.add_column("Percentage", justify="right", style="magenta")

    for col, count in missing.items():
        pct = missing_percent[col]
        table.add_row(col, str(count), f"{pct:.2f}%")

    console.print(table)

def plot_correlation(df: pd.DataFrame):
    """Quick heatmap of numeric correlations."""
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()
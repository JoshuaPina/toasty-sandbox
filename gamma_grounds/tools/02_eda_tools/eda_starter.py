#!/usr/bin/env python3
# tools/eda_starter.py
# ---------------------------------------------------------
# DESCRIPTION: Standardized EDA Toolkit for Crime Capstone
# FEATURES: Missingness Patterns, Sparsity Checks, Categorical Inspection
# ---------------------------------------------------------

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# --- Global Configuration ---
def set_styles():
    """Sets professional plotting and pandas styles."""
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.float_format', '{:.4f}'.format)
    sns.set_theme(style="whitegrid", context="notebook")
    console.print("[bold green]Visual styles set.[/bold green]")

set_styles()

# --- 1. Missing Value Analysis ---

def check_missing(df: pd.DataFrame):
    """
    QUANTITATIVE: Calculates missing value counts and percentages.
    """
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    total_rows = len(df)
    
    if missing.empty:
        console.print(Panel("[bold green]✔ No missing values found![/bold green]", border_style="green"))
        return

    table = Table(title=f"Missing Values Report (N={total_rows:,})", border_style="yellow")
    table.add_column("Column", style="cyan")
    table.add_column("Missing Count", justify="right")
    table.add_column("Percentage", justify="right", style="magenta")
    
    for col, count in missing.items():
        pct = (count / total_rows) * 100
        # Highlight high missingness in red
        pct_str = f"[red]{pct:.2f}%[/red]" if pct > 5 else f"{pct:.2f}%"
        table.add_row(col, f"{count:,}", pct_str)
        
    console.print(table)

def visualize_missing(df: pd.DataFrame):
    """
    DIAGNOSTIC: Visualizes PATTERNS in missing data using missingno.
    Helps identify if data is 'Missing Not At Random' (Systematic failure).
    """
    missing_cols = df.columns[df.isnull().any()].tolist()
    
    if not missing_cols:
        console.print("[green]No missing data to visualize.[/green]")
        return

    console.print(Panel(f"[bold cyan]Visualizing Missing Patterns for {len(missing_cols)} columns...[/bold cyan]"))
    
    # 1. The Matrix (Temporal/Row gaps)
    plt.figure(figsize=(10, 6))
    msno.matrix(df[missing_cols], sparkline=False, fontsize=10)
    plt.title("Missing Data Matrix (White = Missing)", fontsize=16)
    plt.show()

    # 2. The Heatmap (Correlation of missingness)
    if len(missing_cols) > 1:
        plt.figure(figsize=(10, 6))
        msno.heatmap(df[missing_cols], fontsize=10)
        plt.title("Nullity Correlation Matrix", fontsize=16)
        plt.show()

# --- 2. Crime Specific Checks ---

def check_sparsity(df: pd.DataFrame, target_col: str):
    """
    CRITICAL: Checks if the data is 'Zero-Inflated'.
    High sparsity (>80% zeros) means standard Regression will fail.
    You must use Poisson, Tweedie, or Zero-Inflated models.
    """
    if target_col not in df.columns:
        console.print(f"[red]Column '{target_col}' not found for sparsity check.[/red]")
        return

    total = len(df)
    zeros = (df[target_col] == 0).sum()
    pct = (zeros / total) * 100
    
    console.print(f"\n[bold]Sparsity Analysis for '{target_col}':[/bold]")
    console.print(f"Total Rows: [bold]{total:,}[/bold]")
    console.print(f"Zero Rows:  [bold]{zeros:,}[/bold] ([cyan]{pct:.1f}%[/cyan])")
    
    if pct > 80:
        console.print(Panel("[bold red]⚠ High Sparsity Detected![/bold red]\nRecommendation: Use XGBoost (Objective='count:poisson') or Zero-Inflated Regression.", border_style="red"))
    else:
        console.print(Panel("[bold green]✔ Data Density is Adequate[/bold green]\nStandard regression models may work.", border_style="green"))

def inspect_categories(df: pd.DataFrame, top_n=10):
    """
    Shows top values for Categorical columns (NPU, Zone, Type).
    Helps spot 'Dirty Data' (e.g., 'Zone 1' vs 'ZONE 1').
    """
    # Select Object and Category columns
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    
    if len(cat_cols) == 0:
        console.print("[yellow]No categorical columns found.[/yellow]")
        return

    console.print("\n[bold]Categorical Distribution Snapshot:[/bold]")
    
    for col in cat_cols:
        # Create a mini table for each column
        table = Table(title=f"Column: {col} (Top {top_n})", box=None)
        table.add_column("Value", style="cyan")
        table.add_column("Count", justify="right")
        table.add_column("%", justify="right")
        
        counts = df[col].value_counts().head(top_n)
        total_valid = df[col].count()
        
        for val, count in counts.items():
            pct = (count / total_valid) * 100
            table.add_row(str(val), f"{count:,}", f"{pct:.1f}%")
            
        console.print(table)
        print("---")

# --- 3. Distributions & Correlations ---

def plot_distributions(df: pd.DataFrame, numeric_cols: list = None):
    """Plots histograms for numeric data."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    console.print(f"[bold cyan]Plotting distributions for {len(numeric_cols)} columns...[/bold cyan]")
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
            
        plt.figure(figsize=(10, 4))
        sns.histplot(df[col], kde=True, bins=30, color='teal')
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.show()

def plot_correlation(df: pd.DataFrame):
    """
    Plots correlation matrix for Numeric columns.
    NOTE: Does not capture categorical relationships (NPU vs Crime).
    """
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    if numeric_df.empty:
        console.print("[yellow]No numeric columns for correlation matrix.[/yellow]")
        return

    plt.figure(figsize=(12, 10))
    # Correlation matrix
    corr = numeric_df.corr()
    
    # Mask the upper triangle (it's redundant)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Numeric Correlation Matrix")
    plt.show()
# Alias for backwards compatibility
plot_correlation_matrix = plot_correlation
def plot_boxplots(df: pd.DataFrame, numeric_cols: list = None):
    """
    Plots boxplots for numerical data to identify outliers.
    Useful for spotting extreme values that may need treatment.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) == 0:
        console.print("[yellow]No numeric columns for boxplots.[/yellow]")
        return
    
    console.print(f"[bold cyan]Plotting boxplots for {len(numeric_cols)} columns...[/bold cyan]")
    
    # Calculate subplot grid
    n_cols = min(3, len(numeric_cols))
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
    
    # Handle single subplot case
    if len(numeric_cols) == 1:
        axes = [axes]
    else:
        axes = axes.flatten() if n_rows * n_cols > 1 else [axes]
    
    for idx, col in enumerate(numeric_cols):
        if col not in df.columns:
            continue
        
        sns.boxplot(y=df[col], ax=axes[idx], color='steelblue')
        axes[idx].set_title(f"Boxplot: {col}")
        axes[idx].set_ylabel(col)
    
    # Hide empty subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    plt.show()
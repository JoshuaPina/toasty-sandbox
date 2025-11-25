#!/usr/bin/env python3
# tools/eda_crime_analysis.py
# ---------------------------------------------------------
# DESCRIPTION: Crime-Specific EDA Functions
# FEATURES: Temporal Patterns, Spatial Analysis, Crime Type Distribution
# ---------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def temporal_patterns(df: pd.DataFrame, date_col: str, freq: str = 'M', plot: bool = True):
    """
    Analyzes crime trends over time.
    
    Args:
        df: Input DataFrame
        date_col: Name of datetime column
        freq: Resampling frequency ('D'=daily, 'W'=weekly, 'M'=monthly, 'Y'=yearly)
        plot: Whether to display visualization
    """
    if date_col not in df.columns:
        console.print(f"[red]Column '{date_col}' not found.[/red]")
        return
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    
    # Aggregate by time period
    time_series = df_copy.set_index(date_col).resample(freq).size()
    
    # Calculate statistics
    mean_crimes = time_series.mean()
    median_crimes = time_series.median()
    std_crimes = time_series.std()
    min_crimes = time_series.min()
    max_crimes = time_series.max()
    
    # Identify trend
    if len(time_series) > 1:
        trend_slope = np.polyfit(range(len(time_series)), time_series.values, 1)[0]
        if trend_slope > 0.1:
            trend = "[red]Increasing ↑[/red]"
        elif trend_slope < -0.1:
            trend = "[green]Decreasing ↓[/green]"
        else:
            trend = "[yellow]Stable →[/yellow]"
    else:
        trend = "[dim]Insufficient data[/dim]"
    
    # Display summary
    freq_labels = {'D': 'Daily', 'W': 'Weekly', 'M': 'Monthly', 'Y': 'Yearly'}
    freq_label = freq_labels.get(freq, freq)
    
    console.print(f"\n[bold]Temporal Pattern Analysis ({freq_label}):[/bold]")
    console.print(f"Date Range: [cyan]{df_copy[date_col].min().date()}[/cyan] to [cyan]{df_copy[date_col].max().date()}[/cyan]")
    console.print(f"Total Periods: [bold]{len(time_series)}[/bold]")
    console.print(f"Mean Crimes per Period: [bold]{mean_crimes:.1f}[/bold]")
    console.print(f"Median: {median_crimes:.1f} | Std Dev: {std_crimes:.1f}")
    console.print(f"Range: {min_crimes} - {max_crimes}")
    console.print(f"Trend: {trend}")
    
    # Plot if requested
    if plot and len(time_series) > 1:
        plt.figure(figsize=(14, 6))
        
        # Time series plot
        plt.plot(time_series.index, time_series.values, linewidth=2, color='steelblue', label='Crime Count')
        
        # Add trend line
        z = np.polyfit(range(len(time_series)), time_series.values, 1)
        p = np.poly1d(z)
        plt.plot(time_series.index, p(range(len(time_series))), 
                linestyle='--', color='red', alpha=0.7, label='Trend Line')
        
        # Add mean line
        plt.axhline(y=mean_crimes, color='green', linestyle=':', alpha=0.5, label=f'Mean ({mean_crimes:.1f})')
        
        plt.title(f"Crime Trends Over Time ({freq_label})", fontsize=16, fontweight='bold')
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Crime Count", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    return time_series

def spatial_summary(df: pd.DataFrame, groupby_col: str = 'npu', top_n: int = 15, plot: bool = True):
    """
    Analyzes crime distribution by geographic area.
    
    Args:
        df: Input DataFrame
        groupby_col: Column to group by (e.g., 'npu', 'zone', 'beat')
        top_n: Number of top areas to display
        plot: Whether to display bar chart
    """
    if groupby_col not in df.columns:
        console.print(f"[red]Column '{groupby_col}' not found.[/red]")
        return
    
    # Calculate crime counts by area
    area_counts = df[groupby_col].value_counts().head(top_n)
    total_crimes = len(df)
    
    # Create summary table
    table = Table(title=f"Top {top_n} Areas by Crime Count ({groupby_col.upper()})", border_style="cyan")
    table.add_column("Rank", justify="right", style="dim")
    table.add_column("Area", style="bold cyan")
    table.add_column("Crime Count", justify="right", style="bold")
    table.add_column("% of Total", justify="right", style="magenta")
    
    for rank, (area, count) in enumerate(area_counts.items(), 1):
        pct = (count / total_crimes) * 100
        table.add_row(str(rank), str(area), f"{count:,}", f"{pct:.2f}%")
    
    console.print(table)
    
    # Calculate concentration
    top_10_pct = (area_counts.head(10).sum() / total_crimes) * 100
    console.print(f"\n[bold]Concentration:[/bold] Top 10 areas account for [bold cyan]{top_10_pct:.1f}%[/bold cyan] of all crimes")
    
    # Plot if requested
    if plot:
        plt.figure(figsize=(12, 6))
        
        bars = plt.barh(range(len(area_counts)), area_counts.values, color='steelblue')
        plt.yticks(range(len(area_counts)), area_counts.index)
        plt.xlabel("Crime Count", fontsize=12)
        plt.ylabel(groupby_col.upper(), fontsize=12)
        plt.title(f"Crime Distribution by {groupby_col.upper()} (Top {top_n})", fontsize=16, fontweight='bold')
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, area_counts.values)):
            plt.text(count, i, f' {count:,}', va='center', fontsize=9)
        
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
    
    return area_counts

def crime_type_distribution(df: pd.DataFrame, crime_col: str, top_n: int = 15, plot: bool = True):
    """
    Analyzes distribution of crime types.
    
    Args:
        df: Input DataFrame
        crime_col: Column containing crime type/category
        top_n: Number of top crime types to display
        plot: Whether to display pie chart
    """
    if crime_col not in df.columns:
        console.print(f"[red]Column '{crime_col}' not found.[/red]")
        return
    
    # Calculate crime type distribution
    crime_counts = df[crime_col].value_counts().head(top_n)
    total_crimes = len(df)
    
    # Create summary table
    table = Table(title=f"Top {top_n} Crime Types", border_style="cyan")
    table.add_column("Rank", justify="right", style="dim")
    table.add_column("Crime Type", style="bold cyan", max_width=40)
    table.add_column("Count", justify="right", style="bold")
    table.add_column("% of Total", justify="right", style="magenta")
    
    for rank, (crime_type, count) in enumerate(crime_counts.items(), 1):
        pct = (count / total_crimes) * 100
        table.add_row(str(rank), str(crime_type)[:40], f"{count:,}", f"{pct:.2f}%")
    
    console.print(table)
    
    # Plot if requested
    if plot:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Bar chart
        bars = ax1.barh(range(len(crime_counts)), crime_counts.values, color='steelblue')
        ax1.set_yticks(range(len(crime_counts)))
        ax1.set_yticklabels([str(ct)[:30] for ct in crime_counts.index], fontsize=9)
        ax1.set_xlabel("Crime Count", fontsize=12)
        ax1.set_title(f"Crime Type Distribution (Top {top_n})", fontsize=14, fontweight='bold')
        ax1.invert_yaxis()
        
        # Add value labels
        for i, (bar, count) in enumerate(zip(bars, crime_counts.values)):
            ax1.text(count, i, f' {count:,}', va='center', fontsize=8)
        
        # Pie chart (top 10 + "Other")
        top_10 = crime_counts.head(10)
        other_count = total_crimes - top_10.sum()
        
        pie_data = list(top_10.values) + [other_count] if other_count > 0 else list(top_10.values)
        pie_labels = list(top_10.index) + ['Other'] if other_count > 0 else list(top_10.index)
        pie_labels = [str(lbl)[:25] for lbl in pie_labels]
        
        colors = sns.color_palette("Set3", len(pie_data))
        ax2.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax2.set_title("Crime Type Proportions (Top 10 + Other)", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    return crime_counts
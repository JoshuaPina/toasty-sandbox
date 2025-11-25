#!/usr/bin/env python3
# tools/eda_data_quality.py
# ---------------------------------------------------------
# DESCRIPTION: Data Quality Validation Tools for Crime Data
# FEATURES: Duplicates, Date Gaps, Coordinate Validation
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def check_duplicates(df: pd.DataFrame, subset: list = None, show_samples: bool = True):
    """
    Identifies duplicate records in the DataFrame.
    
    Args:
        df: Input DataFrame
        subset: List of columns to check for duplicates (None = all columns)
        show_samples: If True, displays sample duplicate records
    """
    if subset:
        duplicates = df[df.duplicated(subset=subset, keep=False)]
        dupe_count = df.duplicated(subset=subset).sum()
    else:
        duplicates = df[df.duplicated(keep=False)]
        dupe_count = df.duplicated().sum()
    
    total = len(df)
    pct = (dupe_count / total) * 100
    
    console.print(f"\n[bold]Duplicate Records Analysis:[/bold]")
    console.print(f"Total Rows: [bold]{total:,}[/bold]")
    console.print(f"Duplicate Rows: [bold]{dupe_count:,}[/bold] ([cyan]{pct:.2f}%[/cyan])")
    
    if dupe_count == 0:
        console.print(Panel("[bold green]✔ No duplicates found![/bold green]", border_style="green"))
        return
    
    if dupe_count > 0:
        console.print(Panel(f"[bold yellow]⚠ {dupe_count:,} duplicate records detected[/bold yellow]", border_style="yellow"))
        
        if show_samples and len(duplicates) > 0:
            console.print("\n[bold]Sample Duplicate Records (first 5):[/bold]")
            console.print(duplicates.head(10))
    
    return duplicates

def check_date_gaps(df: pd.DataFrame, date_col: str, freq: str = 'D', threshold: int = 1):
    """
    Identifies gaps in temporal data (missing dates/periods).
    
    Args:
        df: Input DataFrame
        date_col: Name of the datetime column
        freq: Frequency to check ('D'=daily, 'W'=weekly, 'M'=monthly)
        threshold: Number of periods that constitutes a "gap"
    """
    if date_col not in df.columns:
        console.print(f"[red]Column '{date_col}' not found.[/red]")
        return
    
    # Ensure datetime type
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    
    # Create complete date range
    date_range = pd.date_range(
        start=df_copy[date_col].min(),
        end=df_copy[date_col].max(),
        freq=freq
    )
    
    # Resample to check coverage
    if freq == 'D':
        actual_dates = df_copy[date_col].dt.date.unique()
        expected_dates = pd.Series(date_range.date)
    else:
        actual_dates = df_copy.set_index(date_col).resample(freq).size()
        expected_dates = pd.Series(index=date_range, data=0)
    
    # Find gaps
    if freq == 'D':
        missing = set(expected_dates) - set(actual_dates)
    else:
        missing = expected_dates[~expected_dates.index.isin(actual_dates.index)]
    
    gap_count = len(missing)
    total_periods = len(date_range)
    coverage_pct = ((total_periods - gap_count) / total_periods) * 100
    
    console.print(f"\n[bold]Temporal Coverage Analysis:[/bold]")
    console.print(f"Date Range: [cyan]{df_copy[date_col].min()}[/cyan] to [cyan]{df_copy[date_col].max()}[/cyan]")
    console.print(f"Expected Periods ({freq}): [bold]{total_periods:,}[/bold]")
    console.print(f"Missing Periods: [bold]{gap_count:,}[/bold]")
    console.print(f"Coverage: [bold cyan]{coverage_pct:.1f}%[/bold cyan]")
    
    if gap_count == 0:
        console.print(Panel("[bold green]✔ No date gaps found![/bold green]", border_style="green"))
    elif gap_count <= threshold:
        console.print(Panel(f"[bold yellow]⚠ Minor gaps detected ({gap_count} periods)[/bold yellow]", border_style="yellow"))
    else:
        console.print(Panel(f"[bold red]⚠ Significant gaps detected ({gap_count} periods)[/bold red]", border_style="red"))
        
        if gap_count > 0 and gap_count < 50:
            console.print("\n[bold]Missing Periods:[/bold]")
            for period in sorted(list(missing))[:20]:
                console.print(f"  • {period}")
            if gap_count > 20:
                console.print(f"  ... and {gap_count - 20} more")

def validate_coordinates(df: pd.DataFrame, lat_col: str = 'latitude', lon_col: str = 'longitude', 
                        lat_range: tuple = (33.6, 34.0), lon_range: tuple = (-84.6, -84.2)):
    """
    Validates geographic coordinates are within expected ranges.
    Default ranges are set for Atlanta, GA area.
    
    Args:
        df: Input DataFrame
        lat_col: Name of latitude column
        lon_col: Name of longitude column
        lat_range: (min, max) valid latitude
        lon_range: (min, max) valid longitude
    """
    if lat_col not in df.columns or lon_col not in df.columns:
        console.print(f"[red]Coordinate columns '{lat_col}' or '{lon_col}' not found.[/red]")
        return
    
    total = len(df)
    
    # Check for nulls
    null_lat = df[lat_col].isnull().sum()
    null_lon = df[lon_col].isnull().sum()
    
    # Check for invalid ranges
    invalid_lat = ((df[lat_col] < lat_range[0]) | (df[lat_col] > lat_range[1])).sum()
    invalid_lon = ((df[lon_col] < lon_range[0]) | (df[lon_col] > lon_range[1])).sum()
    
    # Check for zeros (common data quality issue)
    zero_coords = ((df[lat_col] == 0) | (df[lon_col] == 0)).sum()
    
    # Summary table
    table = Table(title="Coordinate Validation Report", border_style="cyan")
    table.add_column("Check", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Percentage", justify="right", style="magenta")
    
    table.add_row("Total Records", f"{total:,}", "100.0%")
    table.add_row("Null Latitude", f"{null_lat:,}", f"{(null_lat/total)*100:.2f}%")
    table.add_row("Null Longitude", f"{null_lon:,}", f"{(null_lon/total)*100:.2f}%")
    table.add_row("Out of Range (Lat)", f"{invalid_lat:,}", f"{(invalid_lat/total)*100:.2f}%")
    table.add_row("Out of Range (Lon)", f"{invalid_lon:,}", f"{(invalid_lon/total)*100:.2f}%")
    table.add_row("Zero Coordinates", f"{zero_coords:,}", f"{(zero_coords/total)*100:.2f}%")
    
    console.print(table)
    
    total_issues = null_lat + null_lon + invalid_lat + invalid_lon + zero_coords
    
    if total_issues == 0:
        console.print(Panel("[bold green]✔ All coordinates are valid![/bold green]", border_style="green"))
    else:
        pct_issues = (total_issues / total) * 100
        console.print(Panel(
            f"[bold yellow]⚠ {total_issues:,} coordinate issues found ({pct_issues:.1f}%)[/bold yellow]\n"
            f"Expected ranges:\n"
            f"  • Latitude: {lat_range[0]} to {lat_range[1]}\n"
            f"  • Longitude: {lon_range[0]} to {lon_range[1]}",
            border_style="yellow"
        ))
    
    # Return mask of valid coordinates
    valid_mask = (
        df[lat_col].notna() & 
        df[lon_col].notna() &
        (df[lat_col] >= lat_range[0]) & 
        (df[lat_col] <= lat_range[1]) &
        (df[lon_col] >= lon_range[0]) & 
        (df[lon_col] <= lon_range[1]) &
        (df[lat_col] != 0) & 
        (df[lon_col] != 0)
    )
    
    return valid_mask
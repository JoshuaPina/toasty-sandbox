#!/usr/bin/env python3
# tools/eda_feature_engineering.py
# ---------------------------------------------------------
# DESCRIPTION: Feature Engineering Helper Functions
# FEATURES: Time Features, Outlier Detection, Categorical Encoding
# ---------------------------------------------------------

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from rich.console import Console
from rich.panel import Panel

console = Console()

def create_time_features(df: pd.DataFrame, date_col: str, drop_original: bool = False):
    """
    Extracts temporal features from a datetime column.
    Creates: year, month, day, hour, day_of_week, is_weekend, quarter, day_of_year
    
    Args:
        df: Input DataFrame
        date_col: Name of datetime column
        drop_original: If True, removes the original datetime column
    
    Returns:
        DataFrame with new time features
    """
    if date_col not in df.columns:
        console.print(f"[red]Column '{date_col}' not found.[/red]")
        return df
    
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col])
    
    # Extract features
    df_copy[f'{date_col}_year'] = df_copy[date_col].dt.year
    df_copy[f'{date_col}_month'] = df_copy[date_col].dt.month
    df_copy[f'{date_col}_day'] = df_copy[date_col].dt.day
    df_copy[f'{date_col}_hour'] = df_copy[date_col].dt.hour
    df_copy[f'{date_col}_dayofweek'] = df_copy[date_col].dt.dayofweek  # Monday=0, Sunday=6
    df_copy[f'{date_col}_is_weekend'] = df_copy[date_col].dt.dayofweek.isin([5, 6]).astype(int)
    df_copy[f'{date_col}_quarter'] = df_copy[date_col].dt.quarter
    df_copy[f'{date_col}_dayofyear'] = df_copy[date_col].dt.dayofyear
    
    # Optional: Add cyclical encodings (useful for models that don't handle cyclical data well)
    df_copy[f'{date_col}_month_sin'] = np.sin(2 * np.pi * df_copy[f'{date_col}_month'] / 12)
    df_copy[f'{date_col}_month_cos'] = np.cos(2 * np.pi * df_copy[f'{date_col}_month'] / 12)
    df_copy[f'{date_col}_hour_sin'] = np.sin(2 * np.pi * df_copy[f'{date_col}_hour'] / 24)
    df_copy[f'{date_col}_hour_cos'] = np.cos(2 * np.pi * df_copy[f'{date_col}_hour'] / 24)
    
    new_features = [col for col in df_copy.columns if col.startswith(f'{date_col}_')]
    
    console.print(Panel(
        f"[bold green]✔ Created {len(new_features)} time features from '{date_col}'[/bold green]\n"
        f"Features: {', '.join(new_features[:5])}...",
        border_style="green"
    ))
    
    if drop_original:
        df_copy = df_copy.drop(columns=[date_col])
        console.print(f"[yellow]Dropped original column '{date_col}'[/yellow]")
    
    return df_copy

def flag_outliers(df: pd.DataFrame, cols: list = None, method: str = 'iqr', threshold: float = 1.5):
    """
    Flags outliers in numerical columns using IQR or Z-score method.
    
    Args:
        df: Input DataFrame
        cols: List of columns to check (None = all numeric columns)
        method: 'iqr' (Interquartile Range) or 'zscore'
        threshold: IQR multiplier (1.5 standard) or Z-score threshold (3.0 standard)
    
    Returns:
        DataFrame with new boolean columns: {col}_is_outlier
    """
    if cols is None:
        cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    df_copy = df.copy()
    outlier_summary = {}
    
    for col in cols:
        if col not in df.columns:
            continue
        
        if method == 'iqr':
            Q1 = df_copy[col].quantile(0.25)
            Q3 = df_copy[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outlier_mask = (df_copy[col] < lower_bound) | (df_copy[col] > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs((df_copy[col] - df_copy[col].mean()) / df_copy[col].std())
            outlier_mask = z_scores > threshold
        
        else:
            console.print(f"[red]Unknown method '{method}'. Use 'iqr' or 'zscore'.[/red]")
            return df
        
        df_copy[f'{col}_is_outlier'] = outlier_mask
        outlier_count = outlier_mask.sum()
        outlier_pct = (outlier_count / len(df_copy)) * 100
        outlier_summary[col] = (outlier_count, outlier_pct)
    
    # Display summary
    console.print(f"\n[bold]Outlier Detection Summary (Method: {method.upper()}):[/bold]")
    for col, (count, pct) in outlier_summary.items():
        color = "red" if pct > 5 else "yellow" if pct > 1 else "green"
        console.print(f"  • {col}: [{color}]{count:,} outliers ({pct:.2f}%)[/{color}]")
    
    total_outliers = sum(count for count, _ in outlier_summary.values())
    console.print(f"\nTotal outlier flags created: [bold cyan]{total_outliers:,}[/bold cyan]")
    
    return df_copy

def encode_categories(df: pd.DataFrame, cols: list, method: str = 'onehot', drop_original: bool = True):
    """
    Encodes categorical variables for modeling.
    
    Args:
        df: Input DataFrame
        cols: List of categorical columns to encode
        method: 'onehot' (one-hot encoding) or 'label' (label encoding)
        drop_original: If True, removes original categorical columns
    
    Returns:
        DataFrame with encoded features
    """
    df_copy = df.copy()
    
    if method == 'onehot':
        # One-hot encoding (creates binary columns for each category)
        for col in cols:
            if col not in df_copy.columns:
                console.print(f"[yellow]Column '{col}' not found, skipping...[/yellow]")
                continue
            
            # Get dummies
            dummies = pd.get_dummies(df_copy[col], prefix=col, drop_first=False)
            df_copy = pd.concat([df_copy, dummies], axis=1)
            
            if drop_original:
                df_copy = df_copy.drop(columns=[col])
            
            console.print(f"[green]✔ One-hot encoded '{col}' → {len(dummies.columns)} new columns[/green]")
    
    elif method == 'label':
        # Label encoding (assigns integer to each category)
        for col in cols:
            if col not in df_copy.columns:
                console.print(f"[yellow]Column '{col}' not found, skipping...[/yellow]")
                continue
            
            le = LabelEncoder()
            df_copy[f'{col}_encoded'] = le.fit_transform(df_copy[col].astype(str))
            
            if drop_original:
                df_copy = df_copy.drop(columns=[col])
            
            n_categories = len(le.classes_)
            console.print(f"[green]✔ Label encoded '{col}' → {n_categories} unique values[/green]")
    
    else:
        console.print(f"[red]Unknown method '{method}'. Use 'onehot' or 'label'.[/red]")
        return df
    
    console.print(Panel(
        f"[bold green]Encoding complete![/bold green]\n"
        f"Original shape: {df.shape} → New shape: {df_copy.shape}",
        border_style="green"
    ))
    
    return df_copy

def create_interaction_features(df: pd.DataFrame, col1: str, col2: str, operations: list = ['multiply']):
    """
    Creates interaction features between two columns.
    
    Args:
        df: Input DataFrame
        col1: First column name
        col2: Second column name
        operations: List of operations ('multiply', 'add', 'subtract', 'divide')
    
    Returns:
        DataFrame with new interaction features
    """
    df_copy = df.copy()
    
    if col1 not in df.columns or col2 not in df.columns:
        console.print(f"[red]One or both columns not found.[/red]")
        return df
    
    created_features = []
    
    for op in operations:
        if op == 'multiply':
            new_col = f'{col1}_x_{col2}'
            df_copy[new_col] = df_copy[col1] * df_copy[col2]
            created_features.append(new_col)
        
        elif op == 'add':
            new_col = f'{col1}_plus_{col2}'
            df_copy[new_col] = df_copy[col1] + df_copy[col2]
            created_features.append(new_col)
        
        elif op == 'subtract':
            new_col = f'{col1}_minus_{col2}'
            df_copy[new_col] = df_copy[col1] - df_copy[col2]
            created_features.append(new_col)
        
        elif op == 'divide':
            new_col = f'{col1}_div_{col2}'
            df_copy[new_col] = df_copy[col1] / df_copy[col2].replace(0, np.nan)
            created_features.append(new_col)
    
    console.print(Panel(
        f"[bold green]✔ Created {len(created_features)} interaction features[/bold green]\n"
        f"Features: {', '.join(created_features)}",
        border_style="green"
    ))
    
    return df_copy
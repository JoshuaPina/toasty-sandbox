#!/usr/bin/env python3
# tools/check_eda_env.py
# --------------------------------------------------------
# DESCRIPTION: Checks the environment for Data Cleaning & EDA
# ---------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import missingno as msno
import scipy
import sklearn
import tqdm
import re
import pathlib
import rich
import sys

# --- Phase 1 Critical Imports ---
# We use try/except so the script doesn't crash if they are missing
# It allows the table to report "Not Found" instead of raising an error.
try:
    import geopandas as gpd
except ImportError:
    gpd = None

try:
    import shapely
except ImportError:
    shapely = None

try:
    import openpyxl
except ImportError:
    openpyxl = None

try:
    import pyarrow
except ImportError:
    pyarrow = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def eda_env():
    """
    Generates a Rich table displaying loaded libraries and their versions.
    """
    
    # Create a table
    table = Table(show_header=True, header_style="bold magenta", title="Phase 1: Data Cleaning & EDA Environment")
    table.add_column("Library", style="dim", width=20)
    table.add_column("Category", style="italic", width=15)
    table.add_column("Version", style="bold cyan", justify="right")
    table.add_column("Status", justify="center")

    # Dictionary of libraries to check
    libraries = [
        # --- Core ---
        ("Pandas", pd, "Dataframes"),
        ("NumPy", np, "Math"),
        ("Rich", rich, "UI"),
        ("TQDM", tqdm, "Utils"),
        
        # --- Geospatial (CRITICAL for 01_etl_cleaning.py) ---
        ("GeoPandas", gpd, "Spatial"), 
        ("Shapely", shapely, "Geometry"),

        # --- Viz & Stats ---
        ("Matplotlib", matplotlib, "Visualization"),
        ("Seaborn", sns, "Visualization"),
        ("Missingno", msno, "Data Cleaning"),
        ("SciPy", scipy, "Statistics"),
        ("Scikit-Learn", sklearn, "Imputation"),
        
        # --- I/O & Utils ---
        ("OpenPyXL", openpyxl, "Excel Support"),
        ("PyArrow", pyarrow, "Parquet Support"),
        ("SQLAlchemy", sqlalchemy, "Database I/O"),
        ("RE (Regex)", re, "String Ops"),
        ("Pathlib", pathlib, "File I/O")
    ]

    all_good = True

    for name, lib, category in libraries:
        version = "Not Found"
        status = "[red]✖[/red]"
        
        if lib is not None:
            if hasattr(lib, '__version__'):
                version = lib.__version__
                status = "[green]✔[/green]"
            else:
                # Standard libs like re/pathlib don't always have __version__
                version = "Installed" 
                status = "[green]✔[/green]"
        else:
            all_good = False
            
        table.add_row(name, category, version, status)

    # Print the result
    console.print(table)
    
    if all_good:
        console.print(Panel.fit(
            "[bold green]System Ready for Data Cleaning[/bold green]", 
            border_style="green"
        ))
    else:
         console.print(Panel.fit(
            "[bold red]Missing Dependencies![/bold red]\nPlease run: [yellow]pip install geopandas shapely openpyxl[/yellow]", 
            border_style="red"
        ))

# 3. Execution Block
# This prevents the table from printing if you import this file elsewhere
if __name__ == "__main__":
    eda_env()
# You can call the function using: from check_eda_env import eda_env
# You can check the funcion with:  check_eda_env.eda_env()
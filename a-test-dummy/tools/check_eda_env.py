#!/usr/bin/env python3
# check_eda_env.py
# --------------------------------------------------------
# DESCRIPTION: Checks the environment for EDA testing by importing necessary libraries
# # METHOD: Checks for library versions and displays status using Rich
# # ---------------------------------------------------------
# USAGE: python check_eda_env.py
# DEPS: pandas, numpy, matplotlib, seaborn, missingno, scipy, scikit-learn, tqdm, rich
# NOTE: This script is intended to be imported in Jupyter Notebooks to set up the environment.
# ---------------------------------------------------------

# 0. Imports
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings as wr
import rich
import missingno as msno
import scipy
from scipy import stats
import sklearn
from sklearn.impute import SimpleImputer
import tqdm
import os
import re
import pathlib
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# 1. Setup
wr.filterwarnings('ignore')
console = Console()

def eda_env():
    """
    Generates a Rich table displaying loaded libraries and their versions.
    """
    
    # Create a table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Library", style="dim", width=20)
    table.add_column("Category", style="italic", width=15)
    table.add_column("Version", style="bold cyan", justify="right")
    table.add_column("Status", justify="center")

    # Dictionary of libraries to check
    # (Name, Module Object, Category)
    libraries = [
        ("Pandas", pd, "Dataframes"),
        ("NumPy", np, "Math"),
        ("Matplotlib", matplotlib, "Visualization"),
        ("Seaborn", sns, "Visualization"),
        ("Missingno", msno, "Data Cleaning"),
        ("SciPy", scipy, "Statistics"),
        ("Scikit-Learn", sklearn, "Imputation/ML"),
        ("TQDM", tqdm, "Utils"),
        ("Rich", rich, "UI"),
        ("RE (Regex)", re, "String Ops"),
        ("Pathlib", pathlib, "File I/O")
    ]

    for name, lib, category in libraries:
        try:
            # Check for standard __version__ attribute
            if hasattr(lib, '__version__'):
                version = lib.__version__
            else:
                # Handle standard libraries that don't always expose version
                version = "Standard Lib"
            
            status = "[green]✔[/green]"
        except ImportError:
            version = "Not Found"
            status = "[red]✖[/red]"
            
        table.add_row(name, category, version, status)

    # Print the "Success" panel
    console.print(Panel.fit(
        table, 
        title="[bold green]Environment Initialized[/bold green]", 
        border_style="green"
    ))

# 2. Run the check
eda_env()
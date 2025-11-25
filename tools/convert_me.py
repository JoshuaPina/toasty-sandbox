#!/usr/bin/env python3
# convert_me.py
# ---------------------------------------------------------
# DESCRIPTION: [Conversion Tools] Standard imports and helper functions for file conversion.
# NOTE: Used in "Burglary Risk" and "Ticket Prediction" projects.
# ---------------------------------------------------------
# USAGE: import convert_me as cm -> cm.csv_to_xlsx(input_file, output_file)
# ---------------------------------------------------------
# DEPENDENCIES: pandas, pathlib, numbers_parser, rich
# ---------------------------------------------------------

import pandas as pd
from pathlib import Path
from numbers_parser import Document
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import time

# --- Setup ---
console = Console()

# --- Helpers ---

def get_file_size(path: Path) -> str:
    """Returns human-readable file size."""
    if not path.exists():
        return "0 B"
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def log_success(input_file: Path, output_file: Path, start_time: float) -> dict:
    """Logs success and returns stats for the summary table."""
    duration = time.time() - start_time
    file_size = get_file_size(output_file)
    
    console.print(f"[green]✔[/green] converted [bold]{input_file.name}[/bold] -> [bold cyan]{output_file.name}[/bold]")
    
    return {
        "status": "[green]Success[/green]",
        "input": input_file.name,
        "output": output_file.name,
        "type": output_file.suffix.upper(),
        "size": file_size,
        "time": f"{duration:.2f}s"
    }

def log_error(input_file: Path, output_file: Path, error: str) -> dict:
    """Logs failure and returns stats."""
    console.print(f"[red]✖[/red] Failed: [bold]{input_file.name}[/bold] ({error})")
    
    return {
        "status": "[red]Failed[/red]",
        "input": input_file.name,
        "output": output_file.name if output_file else "-",
        "type": "-",
        "size": "-",
        "time": "-"
    }

# --- Core Converters ---

def csv_to_xlsx(input_file: Path, output_file: Path) -> dict:
    start = time.time()
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with console.status(f"[bold yellow]CSV -> Excel:[/bold yellow] {input_file.name}...", spinner="dots"):
            df = pd.read_csv(input_file)
            df.to_excel(output_file, index=False)
        return log_success(input_file, output_file, start)
    except Exception as e:
        return log_error(input_file, output_file, str(e))

def xlsx_to_csv(input_file: Path, output_file: Path) -> dict:
    start = time.time()
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with console.status(f"[bold green]Excel -> CSV:[/bold green] {input_file.name}...", spinner="dots"):
            df = pd.read_excel(input_file)
            df.to_csv(output_file, index=False)
        return log_success(input_file, output_file, start)
    except Exception as e:
        return log_error(input_file, output_file, str(e))

def csv_to_parquet(input_file: Path, output_file: Path) -> dict:
    start = time.time()
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with console.status(f"[bold blue]CSV -> Parquet:[/bold blue] {input_file.name}...", spinner="dots"):
            df = pd.read_csv(input_file)
            df.to_parquet(output_file, engine="pyarrow", compression="snappy")
        return log_success(input_file, output_file, start)
    except Exception as e:
        return log_error(input_file, output_file, str(e))

def parquet_to_csv(input_file: Path, output_file: Path) -> dict:
    start = time.time()
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with console.status(f"[bold blue]Parquet -> CSV:[/bold blue] {input_file.name}...", spinner="dots"):
            df = pd.read_parquet(input_file, engine="pyarrow")
            df.to_csv(output_file, index=False)
        return log_success(input_file, output_file, start)
    except Exception as e:
        return log_error(input_file, output_file, str(e))

def numbers_to_csv(input_file: Path, output_file: Path) -> dict:
    start = time.time()
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with console.status(f"[bold magenta]Numbers -> CSV:[/bold magenta] {input_file.name}...", spinner="dots"):
            doc = Document(str(input_file))
            sheet = doc.sheets[0]
            table = sheet.tables[0]
            data = table.rows(values_only=True)

            if not data:
                Path(output_file).touch()
            else:
                headers = data[0]
                df = pd.DataFrame(data[1:], columns=headers)
                df.to_csv(output_file, index=False, encoding='utf-8')
        return log_success(input_file, output_file, start)
    except Exception as e:
        return log_error(input_file, output_file, str(e))

# --- Inference ---

def infer_and_run_conversion(input_path: Path, output_path: Path) -> dict:
    """
    Decides which function to call based on file extensions, 
    runs it, and returns the result dictionary.
    """
    i_ext = input_path.suffix.lower()
    o_ext = output_path.suffix.lower()

    # Mapquest
    mapping = {
        ('.csv', '.xlsx'): csv_to_xlsx,
        ('.xlsx', '.csv'): xlsx_to_csv,
        ('.csv', '.parquet'): csv_to_parquet,
        ('.parquet', '.csv'): parquet_to_csv,
        ('.numbers', '.csv'): numbers_to_csv
    }

    # Find the converter
    converter = mapping.get((i_ext, o_ext))

    if converter:
        # Run the specific function
        return converter(input_path, output_path)
    else:
        # Log that no mapping was found
        return log_error(input_path, output_path, "No valid converter found for format pair")


# --- Main Execution ---

if __name__ == "__main__":
    
    # 1. Setup
    console.print(Panel.fit(
        "[bold white]Smart Data Converter[/bold white]\n[dim]Auto-detects format from file extensions[/dim]",
        style="bold blue"
    ))

    data_path = Path("data")
    
    # Generate dummy data for testing
    sample_csv = data_path / "sample.csv"
    if not sample_csv.exists():
        data_path.mkdir(parents=True, exist_ok=True)
        pd.DataFrame({'a': [1,2], 'b': [3,4]}).to_csv(sample_csv, index=False)

    # 2. Define the Pipeline Tasks
    # Notice: We only list Paths. We don't specify the function anymore!
    tasks = [
        (sample_csv, data_path / "converted/smart_sample.xlsx"),
        (sample_csv, data_path / "converted/smart_sample.parquet"),
        (data_path / "converted/smart_sample.xlsx", data_path / "converted/roundtrip.csv"),
        (data_path / "missing.numbers", data_path / "converted/fail_test.csv"),
        (sample_csv, data_path / "converted/unknown_format.xyz") # Should fail gracefully
    ]

    results = []
    console.print(f"\n[bold]Processing {len(tasks)} files...[/bold]\n")

    # 3. Batch Process
    for input_p, output_p in tasks:
        # Skip if input doesn't exist (unless testing error handling)
        if not input_p.exists() and "missing" not in str(input_p):
            continue
            
        # THE MAGIC LINE:
        result = infer_and_run_conversion(input_p, output_p)
        results.append(result)

    # 4. Report
    table = Table(title="Batch Processing Report", box=box.SIMPLE_HEAVY)
    table.add_column("Status", justify="center")
    table.add_column("Input", style="dim")
    table.add_column("Output", style="bold")
    table.add_column("Type", justify="center", style="cyan")
    table.add_column("Size", justify="right")
    table.add_column("Time", justify="right", style="green")

    for res in results:
        table.add_row(
            res["status"], res["input"], res["output"], 
            res["type"], res["size"], res["time"]
        )

    console.print("\n")
    console.print(table)
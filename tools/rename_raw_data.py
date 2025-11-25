import os
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def rename_files():
    # 1. Define Root (Adjust if your script is not in tools/)
    # Assuming script is in /tools, root is one level up
    PROJECT_ROOT = Path(__file__).parent.parent
    RAW_DIR = PROJECT_ROOT / "data" / "raw"

    # 2. define the Mapping
    # Format: "Folder_Name": {"Old_Prefix": "New_Prefix"}
    # If the file is loose in a folder, just map the filename.
    
    renames = [
        # --- Crime CSV/GeoJSON ---
        {
            "dir": RAW_DIR / "apd_csv",
            "old": "OpenDataWebsite_Crime_view_-1943907682062759239.csv",
            "new": "apd_crime_2021_2024.csv"
        },
        {
            "dir": RAW_DIR / "apd_geojson",
            "old": "OpenDataWebsite_Crime_view_8524236547521519883.geojson",
            "new": "apd_crime_2021_2024.geojson"
        },
        # --- Shapefiles (These handle ALL extensions: .shp, .dbf, .shx, etc) ---
        {
            "dir": RAW_DIR / "apd_shapefile",
            "old_stem": "AxonCrimeData_XYTable",
            "new_stem": "apd_crime_2021_2024"
        },
        {
            "dir": RAW_DIR / "shapefiles" / "apd_zone_2019",
            "old_stem": "APD_Zone_2019",
            "new_stem": "apd_police_zones_2019"
        },
        {
            "dir": RAW_DIR / "shapefiles" / "area_landmark_2024",
            "old_stem": "tl_2023_13_arealm",
            "new_stem": "ga_census_landmarks_2023"
        },
        {
            "dir": RAW_DIR / "shapefiles" / "atl_neighborhood",
            "old_stem": "Official_Neighborhoods_-_Open_Data",
            "new_stem": "atl_neighborhoods"
        },
        {
            "dir": RAW_DIR / "shapefiles" / "atl_npu",
            "old_stem": "Official_NPU_-_Open_Data",
            "new_stem": "atl_npu_boundaries"
        },
        {
            "dir": RAW_DIR / "shapefiles" / "census_boundary_2024",
            "old_stem": "cb_2024_13_place_500k",
            "new_stem": "ga_census_places_2024"
        }
    ]

    console.print(f"[bold blue]Starting Batch Rename in {RAW_DIR}...[/bold blue]")

    for task in renames:
        folder = task["dir"]
        
        # Check if it's a simple file rename (CSV/GeoJSON)
        if "old" in task:
            old_file = folder / task["old"]
            new_file = folder / task["new"]
            if old_file.exists():
                old_file.rename(new_file)
                console.print(f"[green]✔ Renamed:[/green] {task['old']} -> {task['new']}")
            else:
                console.print(f"[dim]Skipped (Not found): {task['old']}[/dim]")

        # Check if it's a Shapefile Stem rename (Multiple files)
        elif "old_stem" in task:
            old_stem = task["old_stem"]
            new_stem = task["new_stem"]
            
            # Find all files starting with the old stem
            if folder.exists():
                found_files = list(folder.glob(f"{old_stem}.*"))
                if not found_files:
                    console.print(f"[yellow]⚠ No files found for stem: {old_stem}[/yellow]")
                    continue

                for f in found_files:
                    # preserve extension (e.g., .shp, .shp.xml)
                    # We use string replace on the name to handle .shp.xml correctly
                    new_name = f.name.replace(old_stem, new_stem)
                    f.rename(folder / new_name)
                
                console.print(f"[green]✔ Renamed Group:[/green] {old_stem}.* -> {new_stem}.*")

if __name__ == "__main__":
    rename_files()
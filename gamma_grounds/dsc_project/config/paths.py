# ccds_app/config/paths.py
# In any module, you import: from ccds_app.config.paths import RAW_CRIME_CSV, PROCESSED_DATA_DIR.
from pathlib import Path

def find_project_root() -> Path:
    """
    Locates the project root directory, handling both script and notebook execution.
    Looks for the 'pyproject.toml' file to confirm the root.
    """
    current_path = Path.cwd()
    
    # Simple check for notebooks: if 'notebooks' is in path, assume parent is root
    if 'notebooks' in current_path.parts:
        # Try to find pyproject.toml starting from the current directory
        for p in current_path.parents:
            if (p / 'pyproject.toml').exists():
                return p
        # Fallback if pyproject.toml isn't found, assume one level up from 'notebooks'
        if current_path.name == 'notebooks':
            return current_path.parent

    # Standard check: Find pyproject.toml in current directory or parents
    for p in [current_path] + list(current_path.parents):
        if (p / 'pyproject.toml').exists():
            return p
            
    # Fallback to current working directory
    return current_path 

# --- 1. DYNAMIC ROOT DIRECTORY ---
PROJECT_ROOT = find_project_root()

# --- 2. DATA DIRECTORIES ---
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SHAPEFILES_DIR = DATA_DIR / "shapefiles"
OUTPUT_DIR = PROJECT_ROOT / "output"
VIZ_DIR = OUTPUT_DIR / "viz"

# --- 3. FILE PATHS (The Source of Truth) ---
# Crime Data
RAW_CRIME_CSV = RAW_DATA_DIR / "apd_csv" / "apd_crime_2021_2024.csv"

# Shapefiles
NPU_SHP = SHAPEFILES_DIR / "atl_npu" / "atl_npu_boundaries.shp"
ZONE_SHP = SHAPEFILES_DIR / "apd_zone_2019" / "apd_police_zones_2019.shp"
CITIES_SHP = SHAPEFILES_DIR / "census_boundary_2024" / "ga_census_places_2024.shp"
LANDMARKS_SHP = SHAPEFILES_DIR / "area_landmark_2024" / "ga_census_landmarks_2023.shp"
NEIGHBORHOOD_SHP = SHAPEFILES_DIR / "atl_neighborhood" / "atl_neighborhoods.shp"

# Output Files
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "01_cleaned_crimes.parquet"
MODEL_GRID_PATH = PROCESSED_DATA_DIR / "02_modeling_grid.parquet"
# config.py
from pathlib import Path

# --- 1. DYNAMIC ROOT DIRECTORY ---
# This finds the folder containing config.py, which is your Project Root (anchor point)
PROJECT_ROOT = Path(__file__).parent.absolute()

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

# --- 4. PROJECT CONSTANTS ---
CRS_LATLON = "EPSG:4326"  # For storage/plotting
CRS_METRIC = "EPSG:3857"  # For distance calculations (meters)
CAMPUS_RADIUS_MILES = 1.0

# Campus Locations (Lat, Lon)
SCHOOL_COORDS = {
    'Georgia State University': (33.7530, -84.3863),
    'Georgia Tech': (33.7756, -84.3963),
    'Emory University': (33.7925, -84.3239),
    'Clark Atlanta University': (33.7533, -84.4124),
    'Spelman College': (33.7460, -84.4129),
    'Morehouse College': (33.7483, -84.4126),
}

# Time Blocks (For Consistency across scripts)
TIME_BLOCKS = {
    'Late Night': (0, 4),
    'Early Morning': (4, 8),
    'Morning': (8, 12),
    'Afternoon': (12, 16),
    'Evening': (16, 20),
    'Night': (20, 24)
}
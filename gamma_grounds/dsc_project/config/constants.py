# ccds_app/config/constants.py
from typing import Dict, Any

# --- 1. GENERAL PROJECT CONSTANTS ---
CRS_LATLON: str = "EPSG:4326"
CRS_METRIC: str = "EPSG:3857"
CAMPUS_RADIUS_MILES: float = 1.0

# --- 2. CAMPUS LOCATIONS ---
SCHOOL_COORDS: Dict[str, tuple[float, float]] = {
    'Georgia State University': (33.7530, -84.3863),
    'Georgia Tech': (33.7756, -84.3963),
    'Emory University': (33.7925, -84.3239),
    'Clark Atlanta University': (33.7533, -84.4124),
    'Spelman College': (33.7460, -84.4129),
    'Morehouse College': (33.7483, -84.4126),
}

# --- 3. TIME BLOCKS ---
TIME_BLOCKS: Dict[str, tuple[int, int]] = {
    'Late Night': (0, 4),
    'Early Morning': (4, 8),
    'Morning': (8, 12),
    'Afternoon': (12, 16),
    'Evening': (16, 20),
    'Night': (20, 24)
}

# --- 4. DATA SPLIT DATES ---
TRAIN_START: str = "2021-01-01"
TRAIN_END: str = "2023-01-01"
VAL_END: str = "2024-01-01"
TEST_END: str = "2025-01-01"

# --- 5. MODEL PARAMETER FACTORIES (Function to use RANDOM_SEED) ---
def get_xgb_params(random_seed: int) -> Dict[str, Any]:
    """Returns XGBoost parameters, incorporating the dynamic RANDOM_SEED."""
    return {
        'objective': 'count:poisson',
        'eval_metric': 'rmse',
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': random_seed, # <--- Uses the seed
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'min_child_weight': 1,
    }

def get_catboost_params(random_seed: int) -> Dict[str, Any]:
    """Returns CatBoost parameters, incorporating the dynamic RANDOM_SEED."""
    return {
        'loss_function': 'Poisson',
        'iterations': 100,
        'depth': 6,
        'learning_rate': 0.1,
        'random_state': random_seed, # <--- Uses the seed
        'verbose': False
    }
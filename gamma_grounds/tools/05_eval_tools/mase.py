# MASE calculation
from sklearn.metrics import mean_absolute_error

def calculate_mase(y_true, y_pred, y_naive):
    """
    Mean Absolute Scaled Error.
    Compares your model's MAE against a naive baseline's MAE.
    MASE < 1 = Better than naive
    MASE > 1 = Worse than naive
    """
    mae_model = mean_absolute_error(y_true, y_pred)
    mae_naive = mean_absolute_error(y_true, y_naive)
    
    mase = mae_model / mae_naive
    return mase

# Usage
mase = calculate_mase(test['crime_count'], xgb_predictions, test['naive_seasonal_pred'])
print(f"MASE: {mase:.3f} ({'Better' if mase < 1 else 'Worse'} than naive seasonal)")
# Future testing

# tools/evaluation/time_series_cv.py

def rolling_origin_cv(df, model, features, target='crime_count', origin_dates=['2022-01-01', '2023-01-01']):
    """
    Time series cross-validation with expanding window.
    """
    results = []
    
    for origin_date in origin_dates:
        # Expanding training window
        train = df[df['date'] < origin_date]
        test = df[(df['date'] >= origin_date) & (df['date'] < pd.to_datetime(origin_date) + pd.DateOffset(years=1))]
        
        # Train and evaluate
        model.fit(train[features], train[target])
        predictions = model.predict(test[features])
        
        mae = mean_absolute_error(test[target], predictions)
        rmse = np.sqrt(mean_squared_error(test[target], predictions))
        
        results.append({
            'train_end': origin_date,
            'test_year': pd.to_datetime(origin_date).year,
            'mae': mae,
            'rmse': rmse
        })
    
    return pd.DataFrame(results)

# Example usage
cv_results = rolling_origin_cv(df, xgb_model, feature_cols)
print(cv_results)

# Output:
#   train_end  test_year   mae   rmse
# 0 2022-01-01       2022  0.42  0.81
# 1 2023-01-01       2023  0.38  0.76
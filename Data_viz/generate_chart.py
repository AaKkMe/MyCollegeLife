from datetime import timedelta
import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib as mt

def load_data_to_dataframe(study_logs):
    """Converts a list of study logs to a pandas DataFrame."""
    df = pd.DataFrame(study_logs)
    df['date'] = pd.to_datetime(df['date'])
    return df

def filter_and_aggregate_data(df):
    """Filters data for the 7 days leading up to the latest entry."""
    if df.empty:
        return None

    # Find the latest date in the data
    latest_date = df['date'].max()
    
    # Calculate the start date (7 days before the latest date)
    start_date = latest_date - timedelta(days=6)

    # Filter the DataFrame to this 7-day period
    mask = (df['date'] >= start_date) & (df['date'] <= latest_date)
    recent_df = df.loc[mask].copy()

    if recent_df.empty:
        return None

    # Group by date and sum the duration
    daily_summary = recent_df.groupby(recent_df['date'].dt.date)['duration'].sum().reset_index()
    daily_summary.columns = ['date', 'total_duration']
    return daily_summary.sort_values(by='date')

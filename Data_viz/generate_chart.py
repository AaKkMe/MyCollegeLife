from datetime import timedelta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64

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

def plot_chart(daily_summary):
    """Creates and returns a matplotlib figure of the study data."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=daily_summary,
        x='date',
        y='total_duration',
        ax=ax,
        palette='plasma',
        hue='date',
        legend=False
    )

    ax.set_title('Total Study Time in the Last 7 Days', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Duration (minutes)', fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate()

    for container in ax.containers:
        ax.bar_label(container, fmt='%d min')

    plt.tight_layout()
    return fig


def get_chart_as_base64(study_logs):
    """Main function to generate a base64-encoded chart from study logs."""
    df = load_data_to_dataframe(study_logs)
    daily_summary = filter_and_aggregate_data(df)

    if daily_summary is None or daily_summary.empty:
        return None

    fig = plot_chart(daily_summary)
    
    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Encode the image to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_base64

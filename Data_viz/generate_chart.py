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
    """Filters data for the 7 days leading up to the latest entry and aggregates it."""
    if df.empty:
        return None, None, None

    latest_date = df['date'].max()
    start_date = latest_date - timedelta(days=6)

    mask = (df['date'] >= start_date) & (df['date'] <= latest_date)
    recent_df = df.loc[mask].copy()

    if recent_df.empty:
        return None, None, None

    # Calculate total study time
    total_duration_minutes = recent_df['duration'].sum()
    total_hours = int(total_duration_minutes // 60)
    total_minutes = int(total_duration_minutes % 60)
    total_study_time = f"{total_hours}h {total_minutes}m"

    # Find the top subject
    top_subject = recent_df.groupby('subject')['duration'].sum().idxmax()

    # Group by date and subject for the stacked bar chart
    daily_summary = recent_df.groupby([recent_df['date'].dt.date, 'subject'])['duration'].sum().reset_index()
    daily_summary.columns = ['date', 'subject', 'duration']
    
    return daily_summary.sort_values(by=['date', 'subject']), total_study_time, top_subject

def plot_chart(daily_summary, total_study_time, top_subject):
    """Creates and returns a matplotlib figure of the study data as a stacked bar chart."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 7))

    # Pivot the data to get subjects as columns
    pivot_df = daily_summary.pivot(index='date', columns='subject', values='duration').fillna(0)

    # Plot the stacked bar chart
    pivot_df.plot(kind='bar', stacked=True, ax=ax, colormap='plasma')

    ax.set_title(
        f'Study Log for the Last 7 Days\nTotal Study Time: {total_study_time} | Top Subject: {top_subject}',
        fontsize=16
    )
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Duration (minutes)', fontsize=12)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    fig.autofmt_xdate(rotation=45)
    
    # Add labels to the bars
    for c in ax.containers:
        labels = [f'{int(v.get_height())}' if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', fontsize=8, color='white', fontweight='bold')

    ax.legend(title='Subjects', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    return fig


def get_chart_as_base64(study_logs):
    """Main function to generate a base64-encoded chart from study logs."""
    df = load_data_to_dataframe(study_logs)
    daily_summary, total_study_time, top_subject = filter_and_aggregate_data(df)

    if daily_summary is None or daily_summary.empty:
        return None

    fig = plot_chart(daily_summary, total_study_time, top_subject)
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_base64


if __name__ == '__main__':
    # Example usage with dummy data
    dummy_data = [
        {'date': '2023-01-01', 'subject': 'Math', 'duration': 120},
        {'date': '2023-01-01', 'subject': 'Physics', 'duration': 60},
        {'date': '2023-01-02', 'subject': 'Math', 'duration': 90},
        {'date': '2023-01-03', 'subject': 'History', 'duration': 45},
        {'date': '2023-01-04', 'subject': 'Physics', 'duration': 75},
        {'date': '2023-01-05', 'subject': 'Math', 'duration': 150},
        {'date': '2023-01-06', 'subject': 'History', 'duration': 60},
        {'date': '2023-01-07', 'subject': 'Physics', 'duration': 90},
        {'date': '2023-01-08', 'subject': 'Math', 'duration': 120},
    ]
    
    base64_image = get_chart_as_base64(dummy_data)
    
    if base64_image:
        print("Chart generated successfully.")
    else:
        print("No data to display.")
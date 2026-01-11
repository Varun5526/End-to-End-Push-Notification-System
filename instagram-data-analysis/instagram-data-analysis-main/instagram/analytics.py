"""
Instagram Notification Analytics Dashboard
Generates visual analytics and reports from notification data
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
from sqlalchemy import create_engine

# Suppress warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
# Use a font that supports emojis better
plt.rcParams['font.family'] = 'DejaVu Sans'

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'varun5526',
    'database': 'instagram'
}

def create_connection():
    """Create MySQL database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def create_sqlalchemy_engine():
    """Create SQLAlchemy engine for pandas compatibility"""
    try:
        connection_string = f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        print(f"❌ Error creating SQLAlchemy engine: {e}")
        return None

def execute_query(query):
    """Execute a query and return results as DataFrame using SQLAlchemy"""
    engine = create_sqlalchemy_engine()
    if engine is None:
        return None
    
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None
    finally:
        engine.dispose()

def create_output_directory():
    """Create directory for analytics outputs"""
    output_dir = 'analytics_output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def generate_summary_stats():
    """Generate and display summary statistics"""
    print("\n" + "="*60)
    print("📊 INSTAGRAM NOTIFICATION ANALYTICS SUMMARY")
    print("="*60)
    
    query = """
    SELECT 
        (SELECT COUNT(*) FROM notifications) AS total_notifications,
        (SELECT COUNT(*) FROM notifications WHERE type = 'foreground') AS foreground_count,
        (SELECT COUNT(*) FROM notifications WHERE type = 'background') AS background_count,
        (SELECT COUNT(*) FROM notifications WHERE DATE(received_at) = CURDATE()) AS today_count,
        (SELECT COUNT(*) FROM notifications WHERE received_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)) AS last_7_days,
        (SELECT COUNT(DISTINCT DATE(received_at)) FROM notifications) AS active_days,
        (SELECT MAX(received_at) FROM notifications) AS last_notification,
        (SELECT MIN(received_at) FROM notifications) AS first_notification
    """
    
    df = execute_query(query)
    if df is not None and not df.empty:
        stats = df.iloc[0]
        print(f"\n📈 Total Notifications: {stats['total_notifications']}")
        print(f"🔔 Foreground: {stats['foreground_count']}")
        print(f"🔕 Background: {stats['background_count']}")
        print(f"📅 Today: {stats['today_count']}")
        print(f"📆 Last 7 Days: {stats['last_7_days']}")
        print(f"🗓️  Active Days: {stats['active_days']}")
        print(f"⏰ Last Notification: {stats['last_notification']}")
        print(f"🕐 First Notification: {stats['first_notification']}")
        
        # Calculate averages
        if stats['active_days'] > 0:
            avg_per_day = stats['total_notifications'] / stats['active_days']
            print(f"📊 Average per Day: {avg_per_day:.2f}")
        
        print("="*60)
        return stats
    return None

def plot_notification_types(output_dir):
    """Create pie chart for notification types"""
    query = "SELECT type, COUNT(*) as count FROM notifications GROUP BY type"
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(10, 6))
        colors = ['#667eea', '#764ba2']
        explode = (0.05, 0) if len(df) == 2 else None
        
        plt.pie(df['count'], labels=df['type'].str.capitalize(), autopct='%1.1f%%', 
                colors=colors, explode=explode, shadow=True, startangle=90)
        plt.title('Notification Distribution by Type', fontsize=16, fontweight='bold', pad=20)
        
        filename = os.path.join(output_dir, 'notification_types.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_hourly_distribution(output_dir):
    """Create bar chart for hourly distribution"""
    query = """
    SELECT 
        HOUR(received_at) AS hour,
        COUNT(*) AS count,
        type
    FROM notifications
    GROUP BY HOUR(received_at), type
    ORDER BY hour
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(14, 6))
        
        # Pivot for grouped bar chart
        pivot_df = df.pivot(index='hour', columns='type', values='count').fillna(0)
        
        pivot_df.plot(kind='bar', color=['#667eea', '#764ba2'], width=0.8)
        plt.title('Notifications by Hour of Day', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Hour of Day', fontsize=12)
        plt.ylabel('Number of Notifications', fontsize=12)
        plt.legend(title='Type', title_fontsize=11, labels=[t.capitalize() for t in pivot_df.columns])
        plt.xticks(rotation=0)
        plt.grid(axis='y', alpha=0.3)
        
        filename = os.path.join(output_dir, 'hourly_distribution.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_top_actions(output_dir):
    """Create horizontal bar chart for top notification actions"""
    query = """
    SELECT 
        SUBSTRING(body, 1, 50) AS action,
        COUNT(*) AS count
    FROM notifications
    GROUP BY body
    ORDER BY count DESC
    LIMIT 10
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(12, 8))
        
        # Remove emojis for better rendering
        df['action_clean'] = df['action'].str.encode('ascii', 'ignore').str.decode('ascii')
        
        colors = plt.cm.viridis(range(len(df)))
        plt.barh(df['action_clean'], df['count'], color=colors)
        plt.title('Top 10 Notification Actions', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Count', fontsize=12)
        plt.ylabel('Action', fontsize=12)
        plt.gca().invert_yaxis()
        
        # Add value labels
        for i, v in enumerate(df['count']):
            plt.text(v + 0.1, i, str(v), va='center', fontweight='bold')
        
        filename = os.path.join(output_dir, 'top_actions.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_daily_trend(output_dir):
    """Create line chart for daily trend"""
    query = """
    SELECT 
        DATE(received_at) AS date,
        COUNT(*) AS count,
        type
    FROM notifications
    WHERE received_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    GROUP BY DATE(received_at), type
    ORDER BY date
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(14, 6))
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Plot for each type
        for notification_type in df['type'].unique():
            type_df = df[df['type'] == notification_type]
            plt.plot(type_df['date'], type_df['count'], 
                    marker='o', linewidth=2, markersize=8, 
                    label=notification_type.capitalize())
        
        plt.title('Daily Notification Trend (Last 30 Days)', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Notifications', fontsize=12)
        plt.legend(title='Type', title_fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        filename = os.path.join(output_dir, 'daily_trend.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_day_of_week(output_dir):
    """Create bar chart for day of week distribution"""
    query = """
    SELECT 
        DAYNAME(received_at) AS day_name,
        DAYOFWEEK(received_at) AS day_num,
        COUNT(*) AS count
    FROM notifications
    GROUP BY DAYNAME(received_at), DAYOFWEEK(received_at)
    ORDER BY day_num
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(12, 6))
        
        colors = ['#667eea' if i % 2 == 0 else '#764ba2' for i in range(len(df))]
        plt.bar(df['day_name'], df['count'], color=colors, edgecolor='black', linewidth=1.5)
        plt.title('Notifications by Day of Week', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Day of Week', fontsize=12)
        plt.ylabel('Number of Notifications', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for i, v in enumerate(df['count']):
            plt.text(i, v + 0.1, str(int(v)), ha='center', fontweight='bold')
        
        filename = os.path.join(output_dir, 'day_of_week.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_time_period_heatmap(output_dir):
    """Create heatmap for time periods"""
    query = """
    SELECT 
        DAYNAME(received_at) AS day_name,
        DAYOFWEEK(received_at) AS day_num,
        CASE 
            WHEN HOUR(received_at) BETWEEN 6 AND 11 THEN 'Morning'
            WHEN HOUR(received_at) BETWEEN 12 AND 17 THEN 'Afternoon'
            WHEN HOUR(received_at) BETWEEN 18 AND 23 THEN 'Evening'
            ELSE 'Night'
        END AS time_period,
        COUNT(*) AS count
    FROM notifications
    GROUP BY day_name, day_num, time_period
    ORDER BY day_num
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        # Pivot for heatmap
        pivot_df = df.pivot(index='day_name', columns='time_period', values='count').fillna(0)
        
        # Reorder columns
        period_order = ['Morning', 'Afternoon', 'Evening', 'Night']
        pivot_df = pivot_df.reindex(columns=period_order, fill_value=0)
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(pivot_df, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Notification Count'}, linewidths=1)
        plt.title('Notification Heatmap: Day vs Time Period', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time Period', fontsize=12)
        plt.ylabel('Day of Week', fontsize=12)
        
        filename = os.path.join(output_dir, 'time_period_heatmap.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def plot_notification_timeline(output_dir):
    """Create timeline visualization of all notifications"""
    query = """
    SELECT 
        received_at,
        type,
        SUBSTRING(body, 1, 30) AS short_body
    FROM notifications
    ORDER BY received_at DESC
    LIMIT 50
    """
    df = execute_query(query)
    
    if df is not None and not df.empty:
        plt.figure(figsize=(14, 8))
        
        df['received_at'] = pd.to_datetime(df['received_at'])
        
        # Create scatter plot
        colors = {'foreground': '#667eea', 'background': '#764ba2'}
        for ntype in df['type'].unique():
            type_df = df[df['type'] == ntype]
            plt.scatter(type_df['received_at'], range(len(type_df)), 
                       c=colors[ntype], label=ntype.capitalize(), 
                       s=100, alpha=0.6, edgecolors='black')
        
        plt.title('Notification Timeline (Last 50)', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Notification Index', fontsize=12)
        plt.legend(title='Type', title_fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        filename = os.path.join(output_dir, 'notification_timeline.png')
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✅ Saved: {filename}")

def generate_csv_reports(output_dir):
    """Generate CSV reports for further analysis"""
    print("\n📄 Generating CSV Reports...")
    
    reports = {
        'all_notifications.csv': "SELECT * FROM notifications ORDER BY received_at DESC",
        'hourly_summary.csv': """
            SELECT 
                HOUR(received_at) AS hour,
                type,
                COUNT(*) AS count
            FROM notifications
            GROUP BY HOUR(received_at), type
            ORDER BY hour, type
        """,
        'daily_summary.csv': """
            SELECT 
                DATE(received_at) AS date,
                type,
                COUNT(*) AS count
            FROM notifications
            GROUP BY DATE(received_at), type
            ORDER BY date DESC, type
        """,
        'weekly_summary.csv': """
            SELECT 
                YEARWEEK(received_at) AS year_week,
                type,
                COUNT(*) AS count
            FROM notifications
            GROUP BY YEARWEEK(received_at), type
            ORDER BY year_week DESC, type
        """
    }
    
    for filename, query in reports.items():
        df = execute_query(query)
        if df is not None:
            filepath = os.path.join(output_dir, filename)
            df.to_csv(filepath, index=False)
            print(f"✅ Saved: {filepath}")

def main():
    """Main function to run all analytics"""
    print("\n🚀 Starting Instagram Notification Analytics...")
    print("="*60)
    
    # Create output directory
    output_dir = create_output_directory()
    print(f"\n📁 Output Directory: {output_dir}")
    
    # Generate summary statistics
    stats = generate_summary_stats()
    
    if stats is None or stats['total_notifications'] == 0:
        print("\n⚠️  No notifications found in database!")
        print("💡 Tip: Send some notifications first using send_notification.py")
        return
    
    print("\n📊 Generating Visualizations...")
    print("-" * 60)
    
    # Generate all plots
    try:
        plot_notification_types(output_dir)
        plot_hourly_distribution(output_dir)
        plot_top_actions(output_dir)
        plot_daily_trend(output_dir)
        plot_day_of_week(output_dir)
        plot_time_period_heatmap(output_dir)
        plot_notification_timeline(output_dir)
    except Exception as e:
        print(f"⚠️  Warning: Some visualizations may have failed: {e}")
    
    # Generate CSV reports
    generate_csv_reports(output_dir)
    
    print("\n" + "="*60)
    print("✨ Analytics Complete!")
    print(f"📂 All files saved in: {output_dir}/")
    print("="*60)
    print("\n💡 Next Steps:")
    print("   • Open the PNG files to view visualizations")
    print("   • Import CSV files into Excel/Google Sheets for further analysis")
    print("   • Share insights with your team!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime

def count_talk_times(df):
    # print(df['talker'])
    user_talk_time_dict={}
    for user in set(df['talker']):
        user_talk_time_dict[user] = len(df[df['talker']== user])
    
    return user_talk_time_dict

def print_least_talkative_hour(df):
    """
    分析最少说话的hour，并返回该小时的所有具体日期（年月日）
    """
    # 确保CreateTime为datetime类型
    df['CreateTime'] = pd.to_datetime(df['CreateTime'])
    df['hour'] = df['CreateTime'].dt.hour
    df['year'] = df['CreateTime'].dt.year
    df['month'] = df['CreateTime'].dt.month
    df['day'] = df['CreateTime'].dt.day
    # 统计每小时消息数
    hour_count = df['hour'].value_counts().sort_index()
    # 找到最少说话的小时（可能有多个）
    min_count = hour_count.min()
    least_hours = hour_count[hour_count == min_count].index.tolist()
    print(f"最少说话的小时有: {least_hours}，每小时消息数为: {min_count}")
    # 针对每个小时，返回所有具体日期及该日期下的聊天开始和结束时间段
    for hour in least_hours:
        hour_df = df[df['hour'] == hour]
        dates = hour_df[['year', 'month', 'day']].drop_duplicates().sort_values(['year', 'month', 'day'])
        print(f"\n==== hour: {hour} ====")
        for _, row in dates.iterrows():
            y, m, d = row['year'], row['month'], row['day']
            date_df = hour_df[(hour_df['year'] == y) & (hour_df['month'] == m) & (hour_df['day'] == d)]
            if not date_df.empty:
                start_time = date_df['CreateTime'].min().strftime('%H:%M:%S')
                end_time = date_df['CreateTime'].max().strftime('%H:%M:%S')
                print(f"{int(y)}-{int(m):02d}-{int(d):02d} 时间段: {start_time} - {end_time}")

def print_late_night_messages(df):
    """
    统计每年凌晨3-6点的消息数
    """
    # 确保CreateTime为datetime类型
    df['CreateTime'] = pd.to_datetime(df['CreateTime'])
    df['year'] = df['CreateTime'].dt.year
    df['hour'] = df['CreateTime'].dt.hour
    
    # 筛选3-6点的消息
    late_night_df = df[(df['hour'] >= 3) & (df['hour'] <= 7)]
    
    # 按年份统计
    yearly_count = late_night_df.groupby('year').size().sort_index()
    
    print("\n=== 每年凌晨3-6点的消息数 ===")
    for year, count in yearly_count.items():
        print(f"{year}年: {count}条消息")
        
    # 统计具体时间分布
    hour_dist = late_night_df.groupby(['year', 'hour']).size().unstack(fill_value=0)
    print("\n 详细时间分布 ")
    print(hour_dist)
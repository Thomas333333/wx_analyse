import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
from collections import Counter
import os
import pandas as pd 
from data_utils import load_stopwords
plt.rcParams['font.sans-serif'] = ['SimHei']

stopwords = load_stopwords()


def generate_wordcloud(df,output_path, text_column='msg'):
    """
    生成词云图
    
    Args:
        df (pandas.DataFrame): 包含文本数据的DataFrame
        text_column (str): 要生成词云的文本列名
        output_path (str): 词云图片保存路径
    """
    # 加载停用词
    # 合并所有文本
    text_df = df[df['type_name'] == '文本']
    text_df = text_df[~text_df['msg'].str.contains('https', na=False)]


    # print(text_df['msg'])
    # https_msgs = text_df[text_df['msg'].str.contains('https', na=False)]
    # print(https_msgs)
    # print(len(https_msgs))

    text = ' '.join(text_df[text_column].astype(str))
    # 使用jieba进行中文分词
    words = jieba.cut(text)
    # 过滤停用词和长度小于等于1的词
    # words = [word for word in words if len(word) > 1 ]
    words = [word for word in words if len(word) > 1 and word not in stopwords]
    # 统计词频
    word_freq = Counter(words)
    # 创建词云对象
    wordcloud = WordCloud(
        font_path='simhei.ttf',  # 使用黑体字体，确保支持中文
        width=800,
        height=400,
        background_color='white',
        max_words=100,
        max_font_size=100,
        random_state=42
    )
    
    # 生成词云
    wordcloud.generate_from_frequencies(word_freq)
    
    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # 保存词云图
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"词云图已保存到: {output_path}")
    
    # 显示词云图
    # plt.show()



def hours_talk_barchart_each_year(df, mapping_dict, save_path):
    # 根据时间解析画条形图
    save_path = os.path.join(save_path, 'talk_barchart')
    os.makedirs(save_path, exist_ok=True)

    df['CreateTime'] = pd.to_datetime(df['CreateTime'])
    df['year'] = df['CreateTime'].dt.year
    df['month'] = df['CreateTime'].dt.month
    df['day'] = df['CreateTime'].dt.day
    df['hour'] = df['CreateTime'].dt.hour

    print(df.head())

    # 0.每年消息数
    year_count = df['year'].value_counts().sort_index()
    fig_width = max(6, len(year_count) * 1.5)
    plt.figure(figsize=(fig_width, 4))
    year_count.plot(kind='bar')
    plt.title('每年消息数 (Bar Chart)')
    plt.xlabel('Year')
    plt.ylabel('Message Count')
    plt.tight_layout()
    plt.savefig(save_path + f'/output_year.png', dpi=300)
    plt.close()

    # 1. 每月消息数
    month_count = df['month'].value_counts().sort_index()
    plt.figure(figsize=(10, 4))
    month_count.plot(kind='bar')
    plt.title(f' 每月消息数 (Bar Chart)')
    plt.xlabel('Month')
    plt.ylabel('Message Count')
    plt.xticks(range(0, 12), [str(i + 1) for i in range(12)])
    plt.tight_layout()
    plt.savefig(save_path + f'/output_month.png', dpi=300)
    plt.close()

    # 2. 每天消息数
    day_count = df['day'].value_counts().sort_index()
    plt.figure(figsize=(12, 4))
    day_count.plot(kind='bar')
    plt.title(f'每天消息数 (Bar Chart)')
    plt.xlabel('Day')
    plt.ylabel('Message Count')
    plt.xticks(range(0, 31), [str(i + 1) for i in range(31)])
    plt.tight_layout()
    plt.savefig(save_path + f'/output_day.png', dpi=300)
    plt.close()

    # 3. 每小时消息数
    hour_count = df['hour'].value_counts().sort_index()
    plt.figure(figsize=(10, 4))
    hour_count.plot(kind='bar')
    plt.title(f' 每小时消息数 (Bar Chart)')
    plt.xlabel('Hour')
    plt.ylabel('Message Count')
    plt.xticks(range(0, 24), [str(i) for i in range(24)])
    plt.tight_layout()
    plt.savefig(save_path + f'/output_hour.png', dpi=300)
    plt.close()

    # ========== 平均消息数统计 ==========
    # 平均每月消息数（分母为实际出现的年份数）
    month_count = df.groupby(['month']).size()
    month_years = df.groupby(['month'])['year'].nunique()
    month_avg = month_count / month_years
    plt.figure(figsize=(10, 4))
    month_avg.plot(kind='bar')
    plt.title('每月平均消息数 (Bar Chart)')
    plt.xlabel('Month')
    plt.ylabel('Average Message Count')
    plt.xticks(range(0, 12), [str(i + 1) for i in range(12)])
    plt.tight_layout()
    plt.savefig(save_path + f'/avg_month.png', dpi=300)
    plt.close()
    print(f'每月平均统计图已保存为 {save_path}/avg_month.png')

    # 平均每天消息数（分母为统计区间内该天在所有年份和月份中真实存在的次数）
    from datetime import datetime
    years = sorted(df['year'].unique())
    all_days = []
    for day in range(1, 32):
        for month in range(1, 13):
            for year in years:
                try:
                    datetime(year, month, day)
                    all_days.append((day, month, year))
                except ValueError:
                    continue  # 跳过不存在的日期（如2月30日）
    all_days_df = pd.DataFrame(all_days, columns=['day', 'month', 'year'])
    day_possible = all_days_df.groupby(['day']).size()
    day_count = df.groupby(['day']).size()
    day_avg = day_count / day_possible
    day_avg = day_avg.fillna(0)
    day_labels = [str(d) for d in day_avg.index]
    plt.figure(figsize=(12, 4))
    plt.bar(day_labels, day_avg.values)
    plt.title('每一天平均消息数 (Bar Chart)')
    plt.xlabel('Day')
    plt.ylabel('Average Message Count')
    plt.xticks(range(0, 31), [str(i + 1) for i in range(31)])
    plt.tight_layout()
    plt.savefig(save_path + f'/avg_day.png', dpi=300)
    plt.close()
    print(f'每天平均统计图已保存为 {save_path}/avg_day.png')

    # 平均每小时消息数（分母为统计区间内所有天数，每天24小时都计入）
    # 统计区间内的所有天数
    unique_days = df.drop_duplicates(['year', 'month', 'day'])
    total_days = unique_days.shape[0]
    # 统计每小时消息数
    hour_count = df.groupby(['hour']).size()
    # 分母为所有天数（每小时都应出现total_days次）
    hour_avg = hour_count / total_days
    # 保证每个小时都在结果中
    hour_avg = hour_avg.reindex(range(24), fill_value=0)
    plt.figure(figsize=(10, 4))
    hour_avg.plot(kind='bar')
    plt.title('每小时平均消息数 (Bar Chart)')
    plt.xlabel('Hour')
    plt.ylabel('Average Message Count')
    plt.xticks(range(0, 24), [str(i) for i in range(24)])
    plt.tight_layout()
    plt.savefig(save_path + f'/avg_hour.png', dpi=300)
    plt.close()
    print(f'每小时平均统计图已保存为 {save_path}/avg_hour.png')


    # 按照时间顺序画出每年每月的消息总数的条形图
    month_count = df.groupby(['year', 'month']).size().sort_index()
    # 构造横坐标标签 'YYYY-MM'
    month_labels = [f'{y}-{m:02d}' for y, m in month_count.index]
    plt.figure(figsize=(max(12, len(month_labels) * 0.5), 4))
    plt.bar(month_labels, month_count.values)
    plt.title('每年每月消息总数 (Bar Chart)')
    plt.xlabel('Year-Month')
    plt.ylabel('Message Count')
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.savefig(save_path + f'/output_year_month.png', dpi=300)
    plt.close()
    print(f'每年每月消息总数统计图已保存为 {save_path}/output_year_month.png')
    return 0
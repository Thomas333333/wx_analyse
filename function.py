import os
from data_utils import merge_csv_files,read_user_json,read_csv_file,load_stopwords
from analysis import count_talk_times,print_least_talkative_hour,print_late_night_messages
from plot_utils import generate_wordcloud,hours_talk_barchart_each_year


def function(df,talker_name,user_info):
    os.makedirs(talker_name, exist_ok=True)

    # 每个人说了多少话
    user_talk_time_dict = count_talk_times(df)
    mapping_dict = {k: (user_info[k]['nickname']+'('+user_info[k]['remark']+')') for k, v in user_talk_time_dict.items()}
    # print(mapping_dict)

    final_dict = {mapping_dict[k]: v for k, v in user_talk_time_dict.items()}
    print('====每个人说了多少话==')
    print(final_dict)
    print('\n')

    #各自说的最多的词云
    save_path = talker_name +'/each_user_wordcloud/'
    os.makedirs(save_path, exist_ok=True)
    for user,id in mapping_dict.items():
        generate_wordcloud(df[df['talker']==user], save_path+id,text_column='msg')

   
    # 统计每年、每月、每天、每小时的总消息数和平均消息数，此外还有按照时间顺序画出每年每月的消息总数的条形图
    hours_talk_barchart_each_year(df,mapping_dict,save_path=talker_name)

     # 异常值分析
    print_least_talkative_hour(df)

    # 统计每年凌晨3-6点的消息数
    print_late_night_messages(df)
  
    #总聊天记录的词云分析
    generate_wordcloud(df, talker_name+'/wordcloud.png',text_column='msg')


if __name__ == "__main__":
    #ready
    stopwords = load_stopwords()
    directory_path = r"    "
    merge_csv_file_path = directory_path+ '\merged_output.csv'
    user_info  = read_user_json(directory_path)

    #merge csv files
    merge_csv_files(directory_path, merge_csv_file_path)

    # Example usage
    df = read_csv_file(merge_csv_file_path)

    talker_name = merge_csv_file_path.split("\\")[-2]
    function(df,talker_name,user_info)
    

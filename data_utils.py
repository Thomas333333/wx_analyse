import os
import pandas as pd
import glob
import json

def merge_csv_files(directory_path, output_file):
    """
    Merge multiple CSV files from a directory into a single CSV file.
    
    Args:
        directory_path (str): Path to the directory containing CSV files
        output_file (str): Path to the output merged CSV file
    """
    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory_path, "*.csv"))
    
    # Sort files to ensure correct order
    csv_files.sort()
    
    # Create an empty list to store dataframes
    dfs = []
    
    # Read each CSV file and append to the list
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"Successfully read: {file}")
        except Exception as e:
            print(f"Error reading {file}: {str(e)}")
    
    if not dfs:
        print("No CSV files were successfully read.")
        return
    
    # Concatenate all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
     
    # Save the merged dataframe to a new CSV file
    try:
        merged_df.to_csv(output_file, index=False)
        print(f"Successfully merged {len(dfs)} files into: {output_file}")
    except Exception as e:
        print(f"Error saving merged file: {str(e)}")

def read_user_json(directory_path):
    file_path = os.path.join(directory_path, 'users.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def read_csv_file(file_path):
    '''
    去除MsgSvrID、talker列
    '''
    df = pd.read_csv(file_path)

    if 'MsgSvrID' in df.columns:
        df = df.drop('MsgSvrID', axis=1)
        df = df.drop('room_name', axis=1)
        df = df.drop('src', axis=1)


        # print("\n已删除MsgSvrID列")

    print("\n=== CSV文件基本信息 ===")
    print(f"总行数: {len(df)}")
    print(f"总列数: {len(df.columns)}")
    
    # Display column names
    print("\n=== 列名列表 ===")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
    
    # Display data types
    print("\n=== 数据类型信息 ===")
    print(df.dtypes)
    
    # Display first few rows
    print("\n=== 前5行数据 ===")
    print(df.head())
    
    return df 


def load_stopwords():
    """
    加载所有停用词文件并合并为一个集合
    
    Returns:
        set: 包含所有停用词的集合
    """
    stopwords_dir = os.path.join(os.path.dirname(__file__), 'stopwords')
    stopwords = set()
    
    # 遍历stopwords目录下的所有txt文件
    for filename in os.listdir(stopwords_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(stopwords_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    words = f.read().splitlines()
                    stopwords.update(words)
                # print(f"已加载停用词文件: {filename}")
            except Exception as e:
                print(f"加载停用词文件 {filename} 时出错: {str(e)}")
    
    return stopwords
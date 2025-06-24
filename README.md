# wx_analyse
## 介绍
根据消息记录完成一些基本的数据分析，具体如下
## 效果
1.每个人的说话总次数
2.统计每年、每月、每天、每小时的总消息数和平均消息数，此外还有按照时间顺序画出每年每月的消息总数的条形图
3.“异常小时”：说话次数最少的小时，输出聊天时间段（一般会是深夜，可以看看那几次在聊什么）
4.统计每年凌晨3-6点的消息数
5.总聊天记录的词云分析（两个人的高频词）
## 使用方式
1.使用项目`PyWxDump`导以csv格式导出自己微信的聊天记录，并记住导出文件夹路径，比如`D:\...\wxdump_work\export\wxid...\csv\wxid...`

2.克隆本项目
```
git clone git@github.com:Thomas333333/wx_analyse.git
```

3.准备工作，下载[停用词](https://github.com/goto456/stopwords)，用于后续生成词云出去无意义的词组。
```
cd wx_analyse
git clone git@github.com:goto456/stopwords.git

#使用PyWxDump的环境的基础上
pip install wordcloud jieba pandas
```
4.修改`funciton.py`的42行代码，写入本地的导出文件夹路径，之后运行
```
python function.py
```

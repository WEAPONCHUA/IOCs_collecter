# 依赖

```python
# Python 3.11  windows x64
# 请通过pip命令下载以下模块
jsonlines
pymongo
iocextract
scrapy
tweepy
django
mongoengine
```

## 运行

1. CMD输入`scrapy runspider article_spider.py -o recent_article_url.jsonl` 获得最近社区文章的url, 输出为jsonl格式
2. CMD输入`scrapy runspider article_analysis.py -o article_IOCs.jsonl`爬虫获取所有文章的IOCs,输出为jsonl格式
3. 将自己的twitter-api-key(需提前向Twitter官方申请)写入secrets.py文件, CMD输入 `py tweetfeed.py`获取最近的推文中的IOCs
4. 配置Mongodb数据库, 注意设定集合规则, 运行ex_to_mongodb.py文件
5. 查看数据库, 获得数据
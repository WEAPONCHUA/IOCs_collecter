import pymongo
import jsonlines

# 读取jsonlines里面的IOCs数据 文章IOCs
article_IOCs = []  # 存放社区文章IOCs
Twitter_IOCs = []  # 存放推特IOCs

with open("./article_IOCs.jsonl", "r+", encoding="utf-8") as ori:
    for item in jsonlines.Reader(ori):
        article_IOCs.append(item)
# 读取推特IOCs
with open("./Twitter_IOCs.jsonl", "r+", encoding="utf-8") as ori:
    for item in jsonlines.Reader(ori):
        Twitter_IOCs.append(item)

# 将IOCs数据存放入Mongodb
client = pymongo.MongoClient("localhost", 27017)
db = client.data

# updata_one 去重插入数据
for ele in article_IOCs:
    temp = db.Community_IOCs.update_one({'value': ele['value']}, {'$set': ele}, True)

for ele in Twitter_IOCs:
    temp = db.Twitter_IOCs.update_one({'value': ele['value']}, {'$set': ele}, True)

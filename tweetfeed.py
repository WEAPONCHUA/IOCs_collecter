import tweepy
import iocextract  # 获取ioc的包, 来源于: https://github.com/InQuest/python-iocextract
from tags import *  # 需要搜索的标签
from whitelist import *  # 白名单
from secrets import *  # 通过 https://developer.twitter.com/apps 获取私人密钥
from datetime import datetime, timedelta
import os
import glob
import csv
import requests
import json
import jsonlines

# 设定颜色集
RED = '\033[91m'
ENDC = '\033[0m'
GREEN = '\033[1;32m'
WHITE = '\033[1m'
BOLD = '\033[01m'
BLUE = '\033[94m'
ORANGE = '\033[38;5;202m'

# 最大爬取推文数量  最好不要超过一百, 容易429回码
max_tweets = 100

# Twitter API认证信息
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
whoami = api.verify_credentials().screen_name

# 搜索的参数1 , 要搜索的标签
query1 = " OR ".join(tags)
query1 = query1 + " -filter:retweets -filter:replies"  # query1 = tags + " -filter:retweets -filter:replies"

# 通过特定主页搜索, 如果后面有新增的, 比如一些特定的作者, 直接以字符串拼接的方式加上去就可以了   注意加OR
query2 = "list:1423693426437001224"
query3 = "https:" + "//api.tweet" + "feed.live/v1/week"

# 搜索的推文
searched_tweets1 = [status for status in
                    tweepy.Cursor(api.search_tweets, q=query1, result_type="recent", tweet_mode='extended').items(
                        max_tweets)]
searched_tweets2 = [status for status in
                    tweepy.Cursor(api.search_tweets, q=query2, result_type="recent", tweet_mode='extended').items(
                        max_tweets)]

searched_tweets = searched_tweets1 + searched_tweets2
search_tweets_info = requests.request("GET", query3, params=None).text

# 爬取速率, 一定要写, 推特对开发者有速率限制 ( https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits)
data = api.rate_limit_status()  # Rate limit
remaining = data["resources"]["search"]["/search/tweets"]["remaining"]  # Remaining rate limit

# 已经获得IOCs放这几个数组里面
seen_urls = []
seen_ips = []
seen_sha256 = []
seen_md5 = []

outputs = glob.glob("output/*.csv")  # 输出成csv便于查看, 后续输出成jsonl便于py读取

# 新获取的IOCs放这里
new_urls = []
new_ips = []
new_sha256 = []
new_md5 = []

# 获取IOCs
for tweet in reversed(searched_tweets):

    # 检查发布推文的用户是否在白名单里面
    tweet_user = tweet.user.screen_name

    if tweet_user in whitelist_users:
        continue

    # 拿到推文, 如果是转推, 也保存
    if hasattr(tweet, 'retweeted_status'):
        text = tweet.retweeted_status.full_text
    else:
        text = tweet.full_text

    # iocectract的包拿到IOCs,  只有url和ip需要修复, sha256和md5s一般不需要
    urls = iocextract.extract_urls(text, refang=True)
    ips = iocextract.extract_ips(text, refang=True)
    sha256s = iocextract.extract_sha256_hashes(text)
    md5s = iocextract.extract_md5_hashes(text)

    # 获取URL
    for url in urls:
        # 白名单处理
        if url not in seen_urls and not url.startswith("https://t.co") and url not in whitelist_urls:

            # 推文信息
            if hasattr(tweet, 'retweeted_status'):
                tweet_date = tweet.retweeted_status.created_at
                tweet_user = tweet.retweeted_status.user.screen_name
                tweet_id = tweet.retweeted_status.id
            else:
                tweet_date = tweet.created_at
                tweet_user = tweet.user.screen_name
                tweet_id = tweet.id

            f_out = "output/" + tweet_date.strftime('%Y%m%d.csv')
            tweet_date = tweet_date.strftime('%Y-%m-%d %H:%M:%S')

            ioc_type = "url"
            ioc_value = url

            tweet_tags = ""
            n_tags = 0
            for tag in tags:
                if tag.lower() in tweet.full_text.lower():
                    if n_tags == 0:
                        tweet_tags = tag
                    else:
                        tweet_tags = tweet_tags + " " + tag
                    n_tags += 1

            tweet_url = "https://twitter.com/{}/status/{}".format(tweet_user, tweet_id)

            row = [tweet_date, tweet_user, ioc_type, ioc_value, tweet_tags, tweet_url]

            with open(f_out, mode='a', encoding="utf-8") as iocs_file:
                iocs_writer = csv.writer(iocs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                iocs_writer.writerow(row)

            seen_urls.append(url)
            new_urls.append(url)

    # 得IP
    for ip in ips:
        # 白名单
        if ip not in seen_ips and ip not in whitelist_ips:

            # 推文信息
            if hasattr(tweet, 'retweeted_status'):
                tweet_date = tweet.retweeted_status.created_at
                tweet_user = tweet.retweeted_status.user.screen_name
                tweet_id = tweet.retweeted_status.id
            else:
                tweet_date = tweet.created_at
                tweet_user = tweet.user.screen_name
                tweet_id = tweet.id

            f_out = "output/" + tweet_date.strftime('%Y%m%d.csv')
            tweet_date = tweet_date.strftime('%Y-%m-%d %H:%M:%S')

            ioc_type = "ip"
            ioc_value = ip

            tweet_tags = ""
            n_tags = 0
            for tag in tags:
                if tag.lower() in tweet.full_text.lower():
                    if n_tags == 0:
                        tweet_tags = tag
                    else:
                        tweet_tags = tweet_tags + " " + tag
                    n_tags += 1

            tweet_url = "https://twitter.com/{}/status/{}".format(tweet_user, tweet_id)

            row = [tweet_date, tweet_user, ioc_type, ioc_value, tweet_tags, tweet_url]

            with open(f_out, mode='a',encoding="utf-8") as iocs_file:
                iocs_writer = csv.writer(iocs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                iocs_writer.writerow(row)

            seen_ips.append(ip)
            new_ips.append(ip)

    # SHA256s
    for sha256 in sha256s:
        if sha256 not in seen_sha256:

            # 推文信息
            if hasattr(tweet, 'retweeted_status'):
                tweet_date = tweet.retweeted_status.created_at
                tweet_user = tweet.retweeted_status.user.screen_name
                tweet_id = tweet.retweeted_status.id
            else:
                tweet_date = tweet.created_at
                tweet_user = tweet.user.screen_name
                tweet_id = tweet.id

            f_out = "output/" + tweet_date.strftime('%Y%m%d.csv')
            tweet_date = tweet_date.strftime('%Y-%m-%d %H:%M:%S')

            ioc_type = "sha256"
            ioc_value = sha256

            tweet_tags = ""
            n_tags = 0
            for tag in tags:
                if tag.lower() in tweet.full_text.lower():
                    if n_tags == 0:
                        tweet_tags = tag
                    else:
                        tweet_tags = tweet_tags + " " + tag
                    n_tags += 1

            tweet_url = "https://twitter.com/{}/status/{}".format(tweet_user, tweet_id)

            row = [tweet_date, tweet_user, ioc_type, ioc_value, tweet_tags, tweet_url]

            with open(f_out, mode='a',encoding="utf-8") as iocs_file:
                iocs_writer = csv.writer(iocs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                iocs_writer.writerow(row)

            seen_sha256.append(sha256)
            new_sha256.append(sha256)

    # MD5s
    for md5 in md5s:
        if md5 not in seen_md5:

            # 推文信息
            if hasattr(tweet, 'retweeted_status'):
                tweet_date = tweet.retweeted_status.created_at
                tweet_user = tweet.retweeted_status.user.screen_name
                tweet_id = tweet.retweeted_status.id
            else:
                tweet_date = tweet.created_at
                tweet_user = tweet.user.screen_name
                tweet_id = tweet.id

            f_out = "output/" + tweet_date.strftime('%Y%m%d.csv')
            tweet_date = tweet_date.strftime('%Y-%m-%d %H:%M:%S')

            ioc_type = "md5"
            ioc_value = md5

            tweet_tags = ""
            n_tags = 0
            for tag in tags:
                if tag.lower() in tweet.full_text.lower():
                    if n_tags == 0:
                        tweet_tags = tag
                    else:
                        tweet_tags = tweet_tags + " " + tag
                    n_tags += 1

            tweet_url = "https://twitter.com/{}/status/{}".format(tweet_user, tweet_id)

            row = [tweet_date, tweet_user, ioc_type, ioc_value, tweet_tags, tweet_url]

            with open(f_out, mode='a',encoding="utf-8") as iocs_file:
                iocs_writer = csv.writer(iocs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                iocs_writer.writerow(row)

            seen_md5.append(md5)
            new_md5.append(md5)

# 同时输出jsonl格式文件, 便于读取
IOCs_list = json.loads(search_tweets_info)
with jsonlines.open("./Twitter_IOCs.jsonl", "w") as w:
    for i in IOCs_list:
        w.write(i)

# 打印部分信息
print(40 * "=")
print(ORANGE + "限制速率: " + ENDC + str(remaining) + " (@" + whoami + ")")
print(40 * "=")
print(BLUE + "[+] 参数1: " + ENDC + query1)
print(40 * "=")
print(BLUE + "[+] 参数2: " + ENDC + query2)
print(40 * "=")
print(
    BLUE + "[+] 共计获取推文数量:" + ENDC + " {} tweets ({} tweets per query)".format(len(searched_tweets), max_tweets))
print(40 * "=")
print(GREEN + "[+] 新增加的威胁指标:" + ENDC)
print("\t- URLs: " + str(len(new_urls)))
print("\t- IPs: " + str(len(new_ips)))
print("\t- SHA256: " + str(len(new_sha256)))
print("\t- MD5: " + str(len(new_md5)))
print(40 * "=")

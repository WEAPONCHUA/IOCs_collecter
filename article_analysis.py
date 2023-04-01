import scrapy
import iocextract
import jsonlines

# 存放要爬取文章的url
url_lists = []
with open("./recent_article_url.jsonl", "r+", encoding="utf-8") as ori:
    for item in jsonlines.Reader(ori):
        url_lists.append(item)
# 变成字符串数组
my_start_urls = []
for item in url_lists:
    my_start_urls.append(item['url'])


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    # start_urls = [
    #     # 以url列表的第一个url作为爬虫起始点  测试
    #     url_lists[0]['url']
    # ]
    start_urls = my_start_urls

    # a = url_index,
    def parse(self, response):
        article_time = response.css("span.elementor-post-info__item--type-date::text").get().strip()
        article_body = response.css("div.elementor-widget-container")  # 文章本体 p:last-child
        # 先判断文章是否有iocs列表
        flag = str(article_body.css("figure.wp-block-table")[-1].css("table tbody tr:first-child td:first-child").get())
        # flag = str(article_body.css("figure.wp-block-table table tbody tr:first-child td:first-child"))
        a = "Indicators" in flag
        # a是true说明这个文章包含IOCs
        if (a == True):
            # 现在大体上是得到表格数据了
            IOCs_table = article_body.css("figure.wp-block-table")[-1].css("table tbody tr")  # 用于保存table
            # 删除第一行表格标题 , 这样就没有标题了 现在是所有tr
            IOCs_table.pop(0)
            # 下面的数组存放IOCs,  每一个元素都是一个对象
            IOCs_list = []  # {'value'=? 'type'=? 'date'=? 'description'=? }
            # 判断字符串的行数
            for item in IOCs_table:  # 该循环的item是每一个tr
                data = str(item.css('td').get())  # get参数得到第一个td  data就是td里面的字符串
                description = item.css('td')[-1].get()  # 获取描述 tr的最后一个td
                # 出去一些杂标签
                data = data.replace('<br>', ' ')
                data = data.replace('</td>', ' ')
                data = data.replace('<td colspan="2">', ' ')
                data = data.replace('<strong>', ' ')
                data = data.replace('</strong>', ' ')
                description = description.strip();
                description = description.replace('<br>', ' ')
                description = description.replace('</td>', ' ')
                description = description.replace('<td colspan="2">', ' ')
                description = description.replace('<td>', ' ')
                description = description.replace('<strong>', ' ')
                description = description.replace('</strong>', ' ')
                description = description.replace('\xa0', ' ')
                # 获取所有的iocs  左边这些参数应该都是列表
                ips = iocextract.extract_ips(data, refang=True)
                urls = iocextract.extract_urls(data, refang=True)
                md5s = iocextract.extract_md5_hashes(data)
                sha1s = iocextract.extract_sha1_hashes(data)
                sha256s = iocextract.extract_sha256_hashes(data)
                for ip in ips:
                    IOCs_list.append({'value': ip, 'type': "ip", 'date': article_time, 'description': description})
                    yield {'value': ip, 'type': "ip", 'date': article_time, 'description': description}
                for url in urls:
                    IOCs_list.append({'value': url, 'type': "url", 'date': article_time, 'description': description})
                    yield {'value': url, 'type': "url", 'date': article_time, 'description': description}
                for md5 in md5s:
                    IOCs_list.append({'value': md5, 'type': "md5", 'date': article_time, 'description': description})
                    yield {'value': md5, 'type': "md5", 'date': article_time, 'description': description}
                for sha1 in sha1s:
                    IOCs_list.append({'value': sha1, 'type': "sha1", 'date': article_time, 'description': description})
                    yield {'value': sha1, 'type': "sha1", 'date': article_time, 'description': description}
                for sha256 in sha256s:
                    IOCs_list.append(
                        {'value': sha256, 'type': "sha256", 'date': article_time, 'description': description})
                    yield {'value': sha256, 'type': "sha256", 'date': article_time, 'description': description}

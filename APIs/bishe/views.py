# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import json

# 连接数据库
import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.data


def testioc(request):
    if request.method == "GET":
        # 得到用户所要查询的url参数
        data = request.GET
        url = data.get("url")  # url 是参数名字
        if url:
            # 如果用户传递了url参数
            result = db.Twitter_IOCs.find_one({"value": url})
            # 这里要再加一个判断, 判断是否数据库拿到了数据
            if result:
                del result['_id']  # 删除_id,因为类型无法识别
                result["flag"] = 1  # 添加一个flag标识位  1代表这个url在地址库里面
                result[
                    "str"] = f'注意,你访问的网站于{result["date"]}被推特用户@{result["user"]}标记为可疑的恶意网站, \n推文地址为:{result["tweet"]}'
                response=JsonResponse(data=result, json_dumps_params={"ensure_ascii": False})
                response["Access-Control-Allow-Origin"] = '*'
                return response
            else:
                response=JsonResponse(data={'flag': 0}, json_dumps_params={"ensure_ascii": False})
                response["Access-Control-Allow-Origin"] = '*'
                return response
        else:
            return JsonResponse(data={"message": "请传递url参数", 'flag': 0}, json_dumps_params={"ensure_ascii": False})
    elif request.method == "POST":
        return JsonResponse(data={"message": "这不是一个POST请求", 'flag': 0},
                            json_dumps_params={"ensure_ascii": False})
    else:
        return JsonResponse(data={"message": "仅接收GET请求", 'flag': 0}, json_dumps_params={"ensure_ascii": False})

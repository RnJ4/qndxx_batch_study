import json
import requests as r
import urllib.parse

apiHeaders = {
  'Host': 'tuanapi.12355.net',
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Origin': 'https://tuan.12355.net',
  'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/201101 Mobile Safari/537.36 MMWEBID/8628 MicroMessenger/7.0.21.1783(0x27001543) Process/tools WeChat/arm64 Weixin GPVersion/1 NetType/WIFI Language/zh_CN ABI/arm64',
  'X-Requested-With': 'com.tencent.mm',
  'Sec-Fetch-Site': 'same-site',
  'Sec-Fetch-Mode': 'cors',
  'Referer': 'https://tuan.12355.net/wechat/view/YouthLearning/page.html',
  'Accept-Encoding': 'gzip, deflate',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

youthstudyHeaders = {
        'Host': 'youthstudy.12355.net',
        'Connection': 'keep-alive',
        'Content-Length': '134',
        'Origin': 'https://youthstudy.12355.net',
        'X-Litemall-Token': '',
        'X-Litemall-IdentiFication': 'young',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/201101 Mobile Safari/537.36 MMWEBID/8628 MicroMessenger/7.0.21.1783(0x27001543) Process/tools WeChat/arm64 Weixin GPVersion/1 NetType/WIFI Language/zh_CN ABI/arm64',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://youthstudy.12355.net/h5/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }

def getSign(mid):
    url="https://tuanapi.12355.net/questionnaire/getYouthLearningUrl?mid="+str(mid)
    response = r.request("GET", url,headers=apiHeaders)
    j=json.loads(response.text)
    signUrl=j['youthLearningUrl']
    sign=signUrl.split('?')
    # print(sign[1][5:])
    return sign[1][5:]

def getToken(sign):

    payload="sign="+urllib.parse.quote(sign)
    url = "https://youthstudy.12355.net/apih5/api/user/get"
    response = r.request("POST", url, headers=youthstudyHeaders, data=payload)
    j=json.loads(response.text)
    # print(j["data"]["entity"]["token"])
    return j["data"]["entity"]["token"]

def getChapterId():
    url = "https://youthstudy.12355.net/apih5/api/young/chapter/new"
    headers = {
        'X-Litemall-IdentiFication': 'young'
    }
    response = r.request("GET", url, headers=headers)
    j=json.loads(response.text)
    return j["data"]["entity"]["id"]

def saveHistory(token,cid):
    headers=youthstudyHeaders
    headers["X-Litemall-Token"]=token
    url = "https://youthstudy.12355.net/apih5/api/young/course/chapter/saveHistory"
    payload = 'chapterId='+str(cid)
    response = r.request("POST", url, headers=headers, data=payload)
    j=json.loads(response.text)
    return j

if __name__ == "__main__":
    for mid in open("mid.txt"):
        print("开始："+mid)
        try:
            cid = getChapterId()
            sign = getSign(mid)
            token = getToken(sign)
            res = saveHistory(token, cid)
        except:
            print(mid+"异常")
            continue

        if res["errno"] == 0:
            print("保存观看记录成功")
        else:
            print("出错啦")
            print(res["errmsg"])
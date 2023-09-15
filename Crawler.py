import re
import requests
import bs4
import urllib.parse



baseUrl = "https://www.luogu.com.cn/problem"
#设置用来保存爬取题目的文件路径
DownloadPath = "洛谷题库\\"
#根据难度将题目分类，存储在不同的文件路径中
secondPath = ["入门/","普及/","普及&提高-/","普及+&提高/","提高+&省选/","省选&NOI-/","NOI&NOI+&CTSC/"]
#洛谷的题目编号是从1000开始的，因此设置最小值为1000，最大值可以设置为1100，根据实际情况进行修改即可

def main(pid,flag):
    
    crawler(pid,flag)

#定义爬虫函数主题，pid为题目id，flag用于作为secondPath数组的标记，决定将爬到的文档存储在二级目录何处
def crawler(pid,flag):
    
    #显示正在爬取的题目进度
    print("正在爬取题目"+str(pid))
    #洛谷题库的网址结构为https://www.luogu.com.cn/problem/P1000类型，因此通过字符串拼接确定get的url
    response = getQuestion(baseUrl +"/P" +str(pid))
    #检查response状态码，如果不为200，显示出现的错误
    if (type(response) == str or response is None):
        print("爬取失败,HTTP:" + str(response))
    else:
            #此处进行题目内容的保存
            #通过对网页文本筛选，找出题目标题title
        
        title = getTitle(response.text)
        problem = problemToMarkdown(response.text)
        print("题目爬取成功！正在保存...",end="")
        saveData(problem,str(secondPath[flag-1]) + "P"+str(pid)+"-"+str(title) +".md")
        print("题目保存成功!")

            #洛谷题库的网址结构为https://www.luogu.com.cn/problem/solution/P1000类型，因此通过字符串拼接确定get的url
        response2 = getAnswer(baseUrl +"/solution/P"+ str(pid))
        if (type(response2) == str or response2 is None):
            print("爬取失败,HTTP:" + str(response))
        else:
            answer = answerToMarkdown(response2.text)
            print("解答爬取成功！正在保存...",end="")
            #print("保存路径"+str(title)+"\\"+"P"+str(i)+"-"+str(title)+ "-题解" +".md")
            saveData(answer,str(secondPath[flag-1])+"P"+str(pid)+"-"+str(title)+ "-题解" +".md")
            print("解答保存成功!")
        print("爬取完毕")
    return 0

def getQuestion(url):
    #将浏览器访问题库时的headers写在此处
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    #通过get获取题目页面内容
    response = requests.get(url = url,headers = headers)
    if(response is None):
        return "未知错误"
    #检查返回response对象的status状态码，如果为200则表示连接成功
    else:
        if response.status_code == 200:#正确返回的话状态码为200
            return response
        elif response.status_code == 302:
            return "错误302"
        elif response.status_code == 403:
            return "错误403"
    
    
#获取题目之后，可以获取题目相应的解答
def getAnswer(url):
    #通过get请求获取题目解答页面的资源
    #因为查看题目解答需要登录，所以用户登录后，将个人信息相关的headers写在此处
    headers = {
        "authority":"www.luogu.com.cn",
        "method":"GET",
        "scheme":"https",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie":"__client_id=1cc74affa2c678a9ca31a870cd53bd0c2662aa7b; _uid=1097207",
        "Referer":"https://www.luogu.com.cn/",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get(url = url,headers = headers)
    if(response is None):
        return "未知错误"
    #检查返回response对象的status状态码，如果为200则表示连接成功
    else:
        if response.status_code == 200:#正确返回的话状态码为200
            return response
        elif response.status_code == 302:
            return "错误302"
        elif response.status_code == 403:
            return "错误403"
    
def getTitle(text):
    bs = bs4.BeautifulSoup(text,"html.parser")
    #通过<h1>标签确定标题位置
    try:
        text = bs.select("h1")[0]
    except:
        print(str(text))
        text = bs.select("h3")[0]
    print(str(text))
    #剪切字符串
    title = str(text).removeprefix("<h1>")
    title = title.removesuffix("</h1>")
    return title

def problemToMarkdown(text):
    bs = bs4.BeautifulSoup(text,"html.parser")
    core = bs.select("article")[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md

def answerToMarkdown(text):
    #解码
    text = str(urllib.parse.unquote(text,encoding ='unicode_escape'))
    core = re.findall('decodeURIComponent\("\{"code":200,"currentTemplate":"ProblemSolution","currentData":\{"solutions":\{"result":\[\{"content":"(.*?)\)\)', text,re.S)[0]
    md = str(core)
    md = re.sub("<h1>","# ",md)
    md = re.sub("<h2>","## ",md)
    md = re.sub("<h3>","#### ",md)
    md = re.sub("</?[a-zA-Z]+[^<>]*>","",md)
    return md

def saveData(data,filename):
    cfilename = DownloadPath + filename
    file = open(cfilename,"a",encoding="utf-8")
    for d in data:
        file.writelines(d)
    file.close()

if __name__ == '__main__':
    main(1000,1)



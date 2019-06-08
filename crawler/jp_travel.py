from lxml import etree
import requests
import time
import json
# def api(thisapi):
#     resp = requests.get(thisapi)
#     myip = resp.text
#     print('get new ip')
#     return myip
# headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1',
#                                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#                                                    'Accept-Encoding': 'gzip, deflate, br',
#                                                    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
#                                                    'Connection': 'keep-alive','DNT': '1',}
def my_get(url):
    resp = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'})
    time.sleep(3)
    print('Sataus Code: ',resp.status_code)
    return resp.text
addr = 'https://www.ptt.cc'
count = 0
for page in range(1,2):
    url = 'https://www.ptt.cc/bbs/Japan_Travel/index'+str(page)+'.html'
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'})
    resp.encoding='utf-8'
    print('get web page')
    time.sleep(3)
    html = etree.HTML(resp.text)
    element_title = html.xpath("//div[@class='title']/a/text()")
    element_url = html.xpath("//div[@class='title']/a/@href")
    full_url = [addr+u for u in element_url]
    element_author = html.xpath("//div[@class='author']/text()")

    # 每夜都是20個內容，四個項目個數一致
    # print('url',len(element_url))
    # print('author',len(element_author))
    # print(element_title)
    # print('title',len(element_title))

    #獲取內容
    resp_cnt = [my_get(u) for u in full_url]
    element_content = [etree.HTML(u).xpath("//div[starts-with(@class,'bbs-screen')]")[0].xpath('string(.)') for u in resp_cnt]
    # 每頁的20文章內容寫入，完成後才會進行下一頁
    with open('./jp_ptt.txt', 'a', encoding='utf-8')as file:
        for i in range(0,len(element_content)):
            my_dict = {}
            my_dict['article_author'] = element_author[i]
            my_dict['article_content'] = element_content[i]
            my_dict['article_title'] = element_title[i]
            my_dict['article_date'] = ''
            print('page {},item {}'.format(str(page),str(i+1)))
            file.write(json.dumps(my_dict,ensure_ascii=False))
            file.write('\n')
    print('finish page')

















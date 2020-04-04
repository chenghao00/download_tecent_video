from pyquery import PyQuery as pq
import re
import json
import requests

# url_list=[]
# for i in range(1, 2):
#     url = 'https://v.qq.com/x/search/?q={0}&needCorrect={1}&stag=3&' \
#           'cur={2}&cxt=tabid%3D0%26sort%3D0%26pubfilter%3D0%26duration%3D0'.format(key, key, i)
#     url_list.append(url)
# 收集要下载的地址，每页的url由6个参数组成，其中ses可以去掉，q和needCorrect都是要搜索的关键词“病毒 教育”，stage是固定值，cur是当前页码，cxt是固定值，
key = '病毒教育'
url_list = ['https://v.qq.com/x/search/?q={0}&needCorrect={1}&stag=3&' \
            'cur={2}&cxt=tabid%3D0%26sort%3D0%26pubfilter%3D0%26duration%3D0'.format(key, key, i) for i in range(1, 2)]

# 遍历url获取每页中的视频连接href_location
for url in url_list:
    doc = pq(url)
    # 获取a标签的父级所在的div,多个元素用items()
    div_tags = doc('.result_title').items()
    for div_tag in div_tags:
        # 获取div的子元素a中的href属性值
        href = div_tag.find('a').attr('href')
        #print(href)
        # 正则提取出vid用于视频下载
        if 'qq' in href and 'page' in href:
            pattern = re.compile('page/(.*?).html', re.S)
            vid = re.findall(pattern, href)[0]
            #print(vid)

            # 使用视频解析接口，只需传入vid
            url = 'http://vv.video.qq.com/getinfo?vids={}&platform=101001&charge=0&otype=json'.format(vid)
            doc2 = pq(url)
            # print(type(doc2.html()))
            # print(doc2.html())
            # 处理数据
            result = doc2.html().replace('QZOutputJson=', '').replace(';', '')
            # print(result,type(result))
            result = json.loads(result)
            print(result)
            try:
                for i in result['vl']['vi']:
                    vkey = i['fvkey']
                    title = i['ti']
                    fn = i['fn']
                    url2 = i['ul']['ui'][2]['url']
                    print(title)

            except:
                pass

            finally:
                url3 = url2 + fn + '?vkey=' + vkey
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
                res=requests.get(url3,stream=True,headers=headers)
                #print(res.content)
                with open('{0}/{1}.mp4'.format('file', 'title'), 'ab') as f:
                    f.write(res.content)
                    f.flush()
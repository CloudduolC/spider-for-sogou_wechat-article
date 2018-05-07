import random
import re;

import pymysql
import requests;
from urllib.parse import urlencode;
import time
from requests import RequestException;
from pyquery import PyQuery as pq;

class Tool:
    # 去除img标签，7位长空格
    removeEm_1 = re.compile('<em>');
    # 删除超链接标签
    removeEm_2 = re.compile('</em>');
    # 把换行标签替换为\n
    replaceRed_1 = re.compile('<!--red_beg-->');
    # 把表格制表<td>替换为\t
    replaceRed_2 = re.compile('<!--red_end-->');
    replace_1=re.compile('&ldquo');
    replace_2=re.compile('&rdquo')
    replace_3 = re.compile('&middot')
    replace_4=re.compile('&mdash');


    def replace(self, x):
        x = re.sub(self.removeEm_1, "", x);
        x = re.sub(self.removeEm_2, "", x);
        x = re.sub(self.replaceRed_1, "", x);
        x = re.sub(self.replaceRed_2, "", x);
        x = re.sub(self.replace_1, "", x);
        x = re.sub(self.replace_2, "", x);
        x = re.sub(self.replace_3, "", x);
        x = re.sub(self.replace_4, "", x);
        # strip()将前后多余内容删除
        return x.strip();

class weixin:
    def __init__(self):
        self.proxy_pool_url='http://127.0.0.1:5555/random';
        self.response_list=[];
        self.proxy=[];
        self.res_1 = [];
        self.res_2=[];
        self.key=True;
        self.tool = Tool();
        self.pattern=re.compile('<div class="txt-box.*?=">(.*?)</a.*?class="txt-info.*?>(.*?)</p.*?class="s-p.*?class="account.*?uigs=".*?">(.*?)</a><span class="s2">',re.S);

    def get_proxy(self):
        try:
            response=requests.get(self.proxy_pool_url);
            #time.sleep(1)
            if response.status_code ==200:
                print('get proxy',response.text);
                return response.text;
        except requests.ConnectionError:
            return None

    def get_response(self,keyword,num):
        base_url='http://weixin.sogou.com/weixin';
        url=base_url+'?'+urlencode({'query':keyword,'type':2, 'page':num});
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'ABTEST=7|1525261186|v1; IPLOC=CN3100; SUID=8407731B4A42910A000000005AE9A382; SUID=8407731B5218910A000000005AE9A382; weixinIndexVisited=1; SUV=00C325401B73078A5AE9A384B7E5A794; ppinf=5|1525261204|1526470804|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxODolRTYlOTYlODclRTklOUIlODB8Y3J0OjEwOjE1MjUyNjEyMDR8cmVmbmljazoxODolRTYlOTYlODclRTklOUIlODB8dXNlcmlkOjQ0Om85dDJsdURVX1JMOFdlU3E3MG1vZ3B3eUI4c2dAd2VpeGluLnNvaHUuY29tfA; pprdig=HIa0NTOLdu6nu7D30KtuzXQYz7LvrATgj58I8C9YTu-0oksxhQHK215w1jIH6sV0R9yfiELfc6NY-Yk1PCjjfpHm_qyCTSjz2Tu4A_SPD465jA0ztomizCG6HRP52rwMC8zeU94oNfuRh8zPPubJSjOQvaJrKBzGhRUPvsadhSg; sgid=19-34829859-AVrpo5TLjaEibpziaBKpusbdU; ppmdig=1525261204000000e284a15bb230ea54a18cb47ffa5b2ca2; sct=1; SNUID=3CB0CBA3B7BDDC8F3B66BD9AB842B543; JSESSIONID=aaaEn7FuJhs-fbPHcjlmw',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        if self.key:
            self.proxy = self.get_proxy();
        if self.proxy:
            proxies = {
                'http': 'http://' + self.proxy,
                'https': 'https://' + self.proxy
            }
        try:
            response = requests.get(url ,allow_redirects=False, proxies=proxies,headers=headers,timeout=25);
            time.sleep(round(random.uniform(1, 4), 2));
            requests.adapters.DEFAULT_RETRIES = 5
            print(response.status_code)
            if response.status_code == 200 and 'ip-time-p' not in response.text:
                self.response_list.append(response.text);
                self.key = False;
                print('代理可用，继续使用原代理。')
            else:
                self.key = True;
                print('代理被封，回调。');
                self.get_response('陈一发', self.i);
        except AttributeError:
            self.key = True;
            print('代理出错+1，回调。');
            self.get_response('陈一发',self.i);
        except RequestException:
            self.key = True;
            print('代理出错+2，回调。');
            self.get_response('陈一发',self.i);

    def parseing_response_1(self):
        for response_i in self.response_list:
            item =re.findall(self.pattern,response_i);
            res_2=[];
            for item_1 in item:
                item_3 = list(item_1);
                item_3[0] = self.tool.replace(item_1[0])
                item_3[1] = self.tool.replace(item_1[1])
                res_2.append(item_3);
            self.res_2.append(res_2);

    def parseing_response_2(self):
        for response_i in self.response_list:
            doc = pq(response_i);
            items = doc('.txt-box').items()
            item_1 = []
            for lis in items:
                item = []
                lis_1 = lis.find('h3 a')
                item.append(lis_1.text())
                lis_2 = lis.find('.txt-info');
                item.append(lis_2.text())
                lis_3 = lis.find('.s-p a');
                item.append(lis_3.text())
                lis_4 = lis.find('.s2 script')
                item.append(lis_4.text())
                item_1.append(item)
            self.res_1.append(item_1);

    def create_sql(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='popslun128245', db='spider_sougouweixin', charset="utf8");
        self.cur = self.conn.cursor();
        self.cur.execute("DROP TABLE IF EXISTS spider_res_1");
        self.cur.execute("DROP TABLE IF EXISTS spider_res_2");
        sqlc_1 = """create table spider_res_1(id int(11) not null auto_increment primary key,
                                title varchar(2000) null,
                                content varchar(5000) null,
                                author varchar(500) null)
                                DEFAULT CHARSET=utf8;"""
        sqlc_2 = """create table spider_res_2(id int(11) not null auto_increment primary key,
                                title varchar(2000) null,
                                content varchar(5000) null,
                                author varchar(500) null)
                                DEFAULT CHARSET=utf8;"""
        self.cur.execute(sqlc_1)
        self.cur.execute(sqlc_2)
        self.conn.commit();

    def writing_sql_1(self):
        sqla_1 = """
                insert into spider_res_1(title,content,author)
                values(%s,%s,%s);
                """
        for item in self.res_1:
            for lis in item:
                self.cur.execute(sqla_1,(lis[0],lis[1],lis[2]));
        self.conn.commit();

    def writing_sql_2(self):
        sqla_2 = """
                insert into spider_res_2(title,content,author)
                values(%s,%s,%s);
                """
        for item in self.res_2:
            for lis in item:
                self.cur.execute(sqla_2,(lis[0],lis[1],lis[2]));
        self.conn.commit();

    def start(self):
        for self.i in range(1,5):
            self.get_response('陈一发',self.i)
        self.parseing_response_1();
        self.parseing_response_2();
        self.create_sql() ;
        self.writing_sql_1();
        self.writing_sql_2();

        print('js')

spider=weixin();
spider.start();


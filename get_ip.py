import requests
import os
import webbrowser
from bs4 import BeautifulSoup
import json
import pickle

temp_set = set()

def get_xici():
    print("getting ip from xicidaili.com...")
    headers_xici = {
        "Host": "www.xicidaili.com",
        "Referer": "https://www.xicidaili.com/nn/1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }

    for i in range(3):
        ses = requests.session()
        ses.get("https://www.xicidaili.com/nn/1")
        xici_url = "https://www.xicidaili.com/nn/{}".format(str(i+1))
        xici_req = requests.get(xici_url,headers=headers_xici)
        print(xici_req.status_code)
        if xici_req.status_code == 200:
            soup = BeautifulSoup(xici_req.text,'html.parser')
            ip_table = soup.find('table',attrs={'id':'ip_list'})
            trs = ip_table.find_all('tr')
            for i,tr in enumerate(trs):
                if i>0:
                    td = tr.find_all('td')
                    ip_port = td[1].string + ":" + td[2].string
                    print(ip_port)
                    temp_set.add(ip_port)

def get_66ip():
    print("getting ip from 66ip.cn...")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        #"Cookie": "",
        "DNT": "1",
        "Host": "www.66ip.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    webbrowser.open("http://www.66ip.cn/areaindex_1/1.html")
    cookie = input("input a valid cookie for 66ip.cn first:")
    headers["Cookie"] = cookie
    ses = requests.session()

    for i in range(26):
        fucking_url = "http://www.66ip.cn/areaindex_{}/1.html".format(str(i+1))     #ÿ������ֻ�е�һҳ���������֤��
        addr = ses.get(fucking_url,headers=headers)
        if addr.status_code == 200:
            soup = BeautifulSoup(addr.content,'html.parser')
            table = soup.find_all('table')[2]
            trs = table.find_all('tr')
            for i,tr in enumerate(trs):
                if i > 0:
                    td = tr.find_all('td')
                    ip_port = td[0].string+ ":" + td[1].string
                    print(ip_port)
                    temp_set.add(ip_port)

def get_freeproxylist():
    print("getting ip from freeproxylist...")
    fpl_url = "http://proxylist.fatezero.org/proxy.list"
    proxy_list = requests.get(fpl_url)
    if proxy_list.status_code == 200:
        lines = proxy_list.text.split('\n')
        for i,line in enumerate(lines):
            try:
                content = json.loads(line)
            except:
                continue
            if str(content["anonymity"]) == "high_anonymous" and str(content["type"]) == "http":
                ip_port = str(content["host"]) + ":" + str(content["port"])
                # print(ip_port)
                temp_set.add(ip_port)
            if i%1000 == 0:
                print("processed {} in free proxy list".format(str(i)))

get_xici()

get_freeproxylist()
f = open("pool.pkl",'wb')
pickle.dump(temp_set,f) 
f.close()

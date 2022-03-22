import requests
import time
import hashlib
import random
from itertools import cycle

class PROXYHANDLER():
    proxy_cycle = None
    proxies_list = []
    proxy_used = 0
    IP = None
    
    def __init__(self,recall_proxy_interval = 25,flag=False):
        self.flag = flag
        self.recall_proxy_interval = recall_proxy_interval
        try:    
            self.IP = self.get_ip_API()
        except:
            self.IP = self.get_ip()
        self.add_ip_to_whitelist(self.IP)
        self._call_for_tt_proxies()


    def _check_to_call_tt_proxy(self):
        if self.proxy_used % self.recall_proxy_interval == 0:
            self._call_for_tt_proxies()


    def _call_for_tt_proxies(self):
        try_times = 10
        while try_times != 0:
            try:
                self.obtain_proxy_list_from_tt_proxy()
                self.shuffel_proxies()
                break
            except:
                time.sleep(3)
                try_times = try_times - 1


    def shuffel_proxies(self,flag=False):
        random.shuffle(self.proxies_list)
        self.proxy_cycle = cycle(self.proxies_list)


    def make_proxy(self):
        PROXY = next(self.proxy_cycle)
        self.proxy_used = self.proxy_used + 1
        self._check_to_call_tt_proxy()
        return PROXY

    def get_proxy_list_from_tt_proxy(self):
        proxies = []
        secret = '50piVRZ9ZedEy2EfqXX9u3'
        params = {
            "license": "PBA5EE66C8FE5DE84",
            "time": int(time.time()),
            "cnt": 1000,
        }
        params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + secret).encode('utf-8')).hexdigest()
        response = requests.get(
                    url="https://api.ttproxy.com/v1/obtain",
                    params=params,
                    headers={
                        "Content-Type": "text/plain; charset=utf-8",
                    },
                    data="1"
                ).json()
        proxies = response["data"]["proxies"]
        return proxies


    def obtain_proxy_list_from_tt_proxy(self,start=0,end=-1):
        proxies_list = self.get_proxy_list_from_tt_proxy()
        final_proxies = []
        for PROXY in proxies_list:
            if self.flag:
                pr = {"http"  : "http://" + PROXY}
            else:
                pr = {"http"  : "http://" + PROXY,"https" : "http://" + PROXY}
            final_proxies.append(pr)
        self.proxies_list = final_proxies


    def add_ip_to_whitelist(self,ip=''):
        secret = '50piVRZ9ZedEy2EfqXX9u3'
        params = {
        "license": "PBA5EE66C8FE5DE84",
        "time": int(time.time()),
        "cnt": 1000,
        }
        params["sign"] = hashlib.md5((params["license"] + str(params["time"]) + secret).encode('utf-8')).hexdigest()
        params['ip']=ip
        response = requests.get(
                url='https://api.ttproxy.com/v1/whitelist/add',
                params=params,
                headers={
                    "Content-Type": "text/plain; charset=utf-8",
                },
                data="1"
            ).json()
        return response

    def find_my_ip_address(self):
        ## importing socket module
        import socket
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        # print(f"Hostname: {hostname}")
        # print(f"IP Address: {ip_address}")
        return ip_address

    def get_ip(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def get_ip_API(self):
        api_url = 'https://api.ipify.org?format=json'
        return requests.get(api_url).json()['ip']

    def get_ip_address_by_google(self):
        from requests_html import HTMLSession
        from bs4 import BeautifulSoup
        sess = HTMLSession()
        rrr = "https://www.google.com/search?ei=uihSYKirGpPB3LUP_Li3gAk&q=what+is+my+ip"
        res = sess.get(rrr).content
        res = BeautifulSoup(res,"lxml")
        res = res.find("span",style="font-size:20px").text
        return res
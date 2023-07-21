import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime

class Stock:
    def __init__(self,stock_num):
        self.stock_num = stock_num
        
    def stock_price(self):
        num = self.stock_num
        stock_id = str(num)

        url = f"https://tw.quote.finance.yahoo.net/quote/q?type=ta&perd=d&mkt=10&sym={stock_id}&v=1&callback=jQuery111302872649618000682_1649814120914&_=1649814120915"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/111.25 (KHTML, like Gecko) Chrome/99.0.2345.81 Safari/123.36'}
        res = requests.get(url,headers=headers)
        # 最新價格
        current = [l for l in res.text.split('{') if len(l)>=60][-1]
        current = current.replace('"','').split(',')
        # print(current)
        # 昨日價格
        yday_all = [l for l in res.text.split('{') if len(l)>=60][-2].split(',')
        yday = float(re.search(':.*',yday_all[4]).group()[1:])
        stock_dict = {'股票代碼':stock_id,
            '開盤':float(re.search(':.*',current[1]).group()[1:]),
            '最高':float(re.search(':.*',current[2]).group()[1:]),
            '最低':float(re.search(':.*',current[3]).group()[1:]),
            '收盤':float(re.search(':.*',current[4]).group()[1:]),
            '數量':float(re.search(':.*',current[5].replace('}]','')).group()[1:]),
            '漲跌幅':round((float(re.search(':.*',current[4]).group()[1:])/yday-1)*100,2)
        }
        return stock_dict
    
    def check_stock_price_change(self,stock_dict):
        thresholds = [5,6,7,8,9,10]
        for threshold in range(len(thresholds)-1,0,-1):
            # print(thresholds[threshold])
            if 5<=stock_dict['漲跌幅']<=thresholds[threshold]:
                return rf"{stock_dict['股票代碼']}目前股價漲幅為{stock_dict['漲跌幅']}%"
    
    def send_notify(self,message):
        url = 'https://notify-api.line.me/api/notify'
        token = 'cYGf4HZecMzcV6GwuugeHF3TUQ5xyOj5bYOzTUuUjRB'
        headers = {
            'Authorization': 'Bearer ' + token    # 設定權杖
        }
        # stock_send = requests.post(url, headers=headers)   # 
        # print(stock_num.json())
        data = {
            'message':message     # 設定要發送的訊息
        }
        data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法
    
    def main (self):
        
        stock_dict = self.stock_price()
        message = self.check_stock_price_change(stock_dict)
        self.send_notify(message)
        
        

if __name__ == '__main__':
    
    
    stop_time = datetime.now().replace(hour=13, minute=30, second=0, microsecond=0) 
    stock_num = input('請輸入股票代碼：').split()
    while datetime.now() < stop_time:
        for i in stock_num:
            print(i)
            test = Stock(i)
            test.main() 
        time.sleep(300)  # 300 秒等於五分鐘
  

        
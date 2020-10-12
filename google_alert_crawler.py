from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import pandas as pd
from datetime import datetime


class GoogleAlertCrawler:
    '''Google Alert 爬蟲'''
    def __init__(self, keywords:list, driver_path:str, output_path:str='./google_alert.csv', sleep_time=1):
        """初始化的資訊

        Args:
            keywords (list): 關鍵字清單
            driver_path (str): Chrome driver的路徑
            output_path (str, optional): Output csv的位置. Defaults to './google_alert.csv'.
            sleep_time (int, optional): 網頁讀取資料的等候時間. Defaults to 1.
        """
        self.keywords = keywords
        self.driver_path = driver_path
        self.output_path = output_path
        self.url = 'https://www.google.com/alerts?hl=zh-tw#1:1'
        self.data = None
        self.sleep_time = sleep_time

    def get_data(self):
        """取得爬蟲資料

        Returns:
            json: Google Alert爬蟲資訊
        """
        data_collection = defaultdict(list)

        # 開啟web driver & get google alert url
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=chrome_options)
        driver.get(self.url)

        # time
        start_time = time.time()

        for k in self.keywords:
            try:
                # 取得關鍵字輸入框位置 & 輸入關鍵字
                search_bar = driver.find_element_by_xpath('//*[@id="query_div"]/input')
                search_bar.clear()
                search_bar.send_keys(k)
                # 等待讀取網頁資訊使用
                time.sleep(self.sleep_time)

                # 取得網路資料（preview set)
                preview_set = driver.find_elements_by_xpath('//*[@id="preview_results"]/ul/li')
                for preview in preview_set:
                    news, news_count = self.parse_html(preview.get_attribute('innerHTML'))
                    data_collection['關鍵字'].extend([k for i in range(news_count)])
                    data_collection['網頁標題'].extend(news['網頁標題'])
                    data_collection['網頁連結'].extend(news['網頁連結'])
                    data_collection['抓取日期'].extend([datetime.now().strftime("%Y-%m-%d") for i in range(news_count)])
                    crawling_time = round(time.time() - start_time, 3)
                    print(f'關鍵字：{k} 抓取完成，總共抓取 {news_count} 筆資料，抓取時間：{crawling_time}')
            except:
                print(f'關鍵字：{k} 抓取失敗 :((')
                pass
        self.data = data_collection
        return self.data
    
    def parse_html(self, html_source:str):
        """解析HTML內的資訊

        Args:
            html_source (str): google alert html資料

        Returns:
            dict: 解析出來的標題與URL
        """
        data = defaultdict(list)
        soup = BeautifulSoup(html_source, 'html.parser')
        counter = 0
    
        # 解析每筆資料的標題與連結
        for l in soup.find_all('li', class_='result'):
            counter += 1
            data['資料來源'].append(soup.h3.text)
            if len(l.a.text.replace(' ', '')) > 0:
                data['網頁標題'].append(l.a.text)
                data['網頁連結'].append(l.a.attrs['href'])
            else:
                data['網頁標題'].append(l.h4.a.text)
                data['網頁連結'].append(l.h4.a.attrs['href'])
        return data, counter

    def output_csv(self):
        """輸出CSV檔案
        """
        df = pd.DataFrame.from_dict(self.data)
        df.to_csv(self.output_path ,index=False)
        print(f'{self.output_path} 存取完成!')
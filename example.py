from google_alert_crawler import GoogleAlertCrawler

##############################
#        定義爬取參數          #
##############################

# chrome driver的位置
driver = './chromedriver'
# 關鍵字清單
keywords = ['蔡英文', '馬英九', '柯文哲']
# 網頁撈取資料的時間
sleep = 2
# 輸出CSV的路徑
csv_file = './google_alert.csv'


##############################
#        執行爬取程式          #
##############################

# 建立google alert instance
google_alert = GoogleAlertCrawler(keywords, driver, output_path=csv_file, sleep_time=sleep)

# 抓取資料
data = google_alert.get_data()

# 輸出CSV檔案
google_alert.output_csv()

print(f'關鍵字 {keywords} 爬取完畢！')
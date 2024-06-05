from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 设置 ChromeDriver 路径
service = Service('/usr/local/bin/chromedriver')  # 替换为实际路径

# 创建浏览器对象
driver = webdriver.Chrome(service=service)

# 打开 Google News
driver.get("https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant")

# 打印页面标题
print("Page title:", driver.title)

# 等待几秒以确保页面加载
driver.implicitly_wait(10)

# 获取一些具体的新闻标题内容
headlines = driver.find_elements(By.CSS_SELECTOR, 'h3')
print("Headlines:")
for headline in headlines[:10]:  # 打印前10个标题
    print(headline.text)

# 关闭浏览器
driver.quit()

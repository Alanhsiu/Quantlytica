from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import time
import sys
sys.path.append('../')
import config

from pybit.unified_trading import HTTP


def setup_driver():
    service = Service('/usr/local/bin/chromedriver')

    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_coin_names(text):
    pattern = r'Binance Will Delist ([A-Z, ]+) on'
    match = re.search(pattern, text)
    if match:
        coins = match.group(1)
        coin_list = [coin.strip() for coin in coins.split(',')]
        return coin_list
    return []

def main():
    driver = setup_driver()
    place_order = False
    
    session = HTTP(
        testnet=False,
        api_key=config.API_KEY_BYBIT,
        api_secret=config.API_SECRET_BYBIT
    )

    with open('log.txt', 'w') as f:
        try:
            while place_order == False:
                cur_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                print('current time:', cur_time)   
                
                start_time = time.time()
                driver.get("https://www.binance.com/en/support/announcement/delisting?c=161&navId=161&hl=en")
                print("Page loaded successfully", file=f, flush=True)

                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.css-1tl1y3y'))
                )
                print("Announcement elements found", file=f, flush=True)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                announcements = soup.select('.css-1w8j6ia')[:2]
                times = soup.select('h6.css-eoufru')[:2]  

                if announcements and times:
                    for announcement, time_element in zip(announcements, times):
                        text = announcement.get_text()
                        time_text = time_element.get_text()
                        # print(f"Announcement Date: {time_text}", file=f, flush=True)
                        # print(f"Announcement: {text}", file=f, flush=True)
                        # print current time
                        if "Binance Will Delist" in text:
                            coin_list = extract_coin_names(text)
                            print(f"Coins to be delisted: {coin_list}", file=f, flush=True)
                            place_order = True
                            # use bybit api to place order
                            symbol = coin_list[0] + "USDT"
                            print(session.get_instruments_info(
                                category="linear",
                                symbol=symbol,
                            ))
                            
                else:
                    print("No announcements found.", file=f, flush=True)

                end_time = time.time()      
                print(f"Runtime: {end_time - start_time} seconds", file=f, flush=True)
                
                time.sleep(3)

        except Exception as e:
            print(f"Error: {e}", file=f, flush=True)

        finally:
            driver.quit()
            print("Driver quit", file=f, flush=True)

if __name__ == "__main__":
    main()

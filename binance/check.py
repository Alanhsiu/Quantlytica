import requests

def check_robots_txt(url):
    if not url.endswith('/'):
        url += '/'
    robots_url = url + 'robots.txt'
    response = requests.get(robots_url)
    if response.status_code == 200:
        print(response.text)
    else:
        print("No robots.txt found")

# Example usage
check_robots_txt("https://www.binance.com/en/support/announcement/latest-binance-news?c=49&navId=49&hl=en")

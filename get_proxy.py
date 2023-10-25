import time
import json
import requests
from bs4 import BeautifulSoup


def check_ip():
    with open("http.txt", "r") as file:
        for proxy in file.read().split("\n"):
            url = "https://www.minimaks.ru/"
            proxies = {
                "http": "http://" + proxy,
            }

            try:
                response = requests.get(url=url, proxies=proxies)

                if response.status_code == 200:
                    print(proxy)
                    return proxies
                else:
                    print("No")

            except requests.exceptions.RequestException as e:
                print("Не удалось выполнить запрос через прокси:", e)

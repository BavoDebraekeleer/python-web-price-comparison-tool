from abc import ABC, abstractmethod
import datetime

# Web scrapping imports
import requests
from bs4 import BeautifulSoup
import smtplib


class Shop(ABC):

    shop_count: int = 0
    SHOP_TYPES: list[str] = ["Amazon"]
    HEADERS = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

    def __init__(self, url: str):
        Shop.shop_count += 1
        self.id: int = Shop.shop_count
        self.name: str = str(self.__class__)
        self.url: str = url
        self.price: float = 0.0
        self.last_updated: datetime.date
        self.price_history: dict[float, datetime.date]  # price + date

    @abstractmethod
    def scrape_data(self, product_name: str):
        # data scrapping to fill in empty product data
        self.update_price()
        pass

    @abstractmethod
    def update_price(self):
        pass


class Amazon(Shop):

    def __init__(self, url: str):
        super().__init__(url)

        self.name: str = "Amazon"

    def scrape_data(self, product_name: str) -> bool:
        page = requests.get(url=self.url, headers=Shop.HEADERS)
        soup = BeautifulSoup(page.content, "html.parser")
        soup.prettify()

        title = soup.find(id="productTitle")
        product_title = title.get_text().strip()    # Gets text from html tags & Strips special chars
        if not product_title.lower().find(product_name.lower()) == -1:
            try:
                self.price = float(soup.find(id="priceblock_ourprice").get_text().replace('.', '').replace('€', '').replace(',', '.').strip())
            except:
                print(f"Price for {product_name} at {self.name} not found.")
                return False

            self.update_price()
            return True
        else:
            print(f"No product name match for {product_name} at {self.name}.")
            return False

    def update_price(self):
        pass

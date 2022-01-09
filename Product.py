from Shop import *


class Product:

    user_count: int = 0
    ID_BASE_STRUCTURE: str = "PROD0000"

    def __init__(self, brand: str, name: str):
        Product.user_count += 1
        self.id: str = Product.ID_BASE_STRUCTURE[len(str(Product.user_count)):] + str(Product.user_count)
        self.name: str = name
        self.ean: str = "0000000000000"  # 13 digits
        self.brand: str = brand
        self.description: str = ""
        self.image_url: str = ""
        self.shops: list[Shop] = []
        self.bestPrice: float = 99999999.99
        self.bestPrice_shopIndex: int = 0

    def add_shop(self, shop: Shop):
        self.shops.append(shop)

    def scrape_data(self):
        for shop in self.shops:
            if not shop.scrape_data(self.name):
                print(f"Scrape for {self.name} at {shop.name} failed.")
            else:
                print(f"Scrape for {self.name} at {shop.name} succeeded.")

    def get_shop_names(self) -> list[str]:
        names: list[str] = []
        for product in self.shops:
            names.append(f"{product.name}")
        return names

    def calculate_best_price(self):
        self.scrape_data()  # Update data

        index = 0
        for shop in self.shops:
            if shop.price < self.bestPrice:
                self.bestPrice = shop.price
                self.bestPrice_shopIndex = index
                print("New best price set.")
            index += 1
        print("Best price unchanged.")

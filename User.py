from Product import *


class User:

    user_count: int = 0
    ID_BASE_STRUCTURE: str = "USER0000"

    def __init__(self, username: str, password: str):
        User.user_count += 1
        self.id: str = User.ID_BASE_STRUCTURE[len(str(User.user_count)):] + str(User.user_count)
        self.username: str = username
        self.password: str = password
        self.products: list[Product] = []

    def get_product_names(self) -> list[str]:
        names: list[str] = []
        for product in self.products:
            names.append(f"{product.brand} {product.name}")
        return names

# UI imports
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QStackedWidget, QDialog, QTextBrowser, QComboBox, QGraphicsPixmapItem, QGraphicsView
from PyQt6.QtGui import QIcon
from PyQt6.uic import loadUi

# Classes imports
from User import *


class PopUp(QWidget):

    def __init__(self, ui_path: str, icon_path: str):
        super().__init__()

        loadUi(ui_path, self)
        self.setWindowIcon(QIcon(icon_path))


class Main(QMainWindow):

    def __init__(self, ui_path: str, icon_path: str):
        super().__init__()

        loadUi(ui_path, self)
        self.setWindowIcon(QIcon(icon_path))


class Interface:

    PASSWORD_LENGTH: int = 3
    STATES = ["Main", "Login", "Create User"]

    def __init__(self, name: str, icon_path: str):
        self.name: str = name
        self.users: list[User] = []
        self.active_user_index: int = 0
        self.current_state = "Main"

        # Windows setup
        self.win_stack = QStackedWidget()
        self.win_main = Main('./interfaces/main.ui', icon_path)
        self.win_login = PopUp('./interfaces/login.ui', icon_path)
        self.win_create = PopUp('./interfaces/create_user.ui', icon_path)
        self.win_stack.addWidget(self.win_main)
        self.win_stack.addWidget(self.win_login)
        self.win_stack.addWidget(self.win_create)
        self.win_stack.show()

        self.dropdown_products: list[QComboBox] = [
            self.win_main.in_add_productSelect,
            self.win_main.in_display_productSelect,
            self.win_main.in_removeProduct
        ]

        # self.state_to_login()     # Normal app flow
        self.test_data()
        self.state_to_main()        # Test

    # State Machine
    def change_state(self):
        if self.current_state == "Main":
            self.open_main()

        elif self.current_state == "Login":
            self.open_login()

        elif self.current_state == "Create User":
            self.open_create_user()

    def state_to_main(self):
        self.current_state = "Main"
        self.change_state()

    def state_to_login(self):
        self.current_state = "Login"
        self.change_state()

    def state_to_create(self):
        self.current_state = "Create User"
        self.change_state()

    def open_main(self):
        self.win_stack.setCurrentIndex(0)
        self.win_stack.setFixedWidth(1000)
        self.win_stack.setFixedHeight(900)

        if self.users:
            self.win_stack.setWindowTitle(f"{self.name} - {self.users[self.active_user_index].username}")
            self.fill_product_dropdowns()
            self.fill_shop_dropdowns()
        else:
            self.win_stack.setWindowTitle(f"{self.name} - No user logged in!")

        # See UI files for QtPy object names
        # Menubar
        self.win_main.actionLogin.triggered.connect(lambda: self.state_to_login())
        self.win_main.actionCreate.triggered.connect(lambda: self.state_to_create())

        # Buttons
        self.win_main.btn_addProduct.clicked.connect(lambda: self.add_product())
        self.win_main.btn_addProductShop.clicked.connect(lambda: self.add_product_shop())

        self.win_main.btn_removeProduct.clicked.connect(lambda: self.remove_product())
        self.win_main.btn_removeProductShop.clicked.connect(lambda: self.remove_product_shop())

        # Dropdown ComboBox https://doc.qt.io/qt-6/qcombobox.html
        self.win_main.in_display_productSelect.activated.connect(lambda: self.show_info())
        self.win_main.in_removeProduct.activated.connect(lambda: self.fill_shop_dropdowns())

        if self.users[self.active_user_index].products:
            self.show_info()

    def open_login(self):
        if self.users:
            self.win_stack.setCurrentIndex(1)
            self.win_stack.setWindowTitle(self.current_state)
            self.win_stack.setFixedWidth(400)
            self.win_stack.setFixedHeight(500)

            self.win_login.btn_login.clicked.connect(lambda: self.login())
            self.win_login.btn_close.clicked.connect(lambda: self.state_to_main())
        else:
            self.state_to_create()

    def login(self):
        username: str = self.win_login.in_username.text()
        password: str = self.win_login.in_password.text()

        print(f"in_username: {username}, in_password: {password}")

        if len(username) > 0 and len(password > 0):
            index = 0
            print("Looping through users.")
            for user in self.users:
                if user.username == username:
                    print("Username found.")
                    if user.password == password:
                        print("Password match.")
                        self.active_user_index = index  # self.users.index(user)
                        print(f"active_user_index set to {index}")
                        self.state_to_main()
                    else:
                        print("Password incorrect.")
                else:
                    print("Username not found.")
                    self.win_login.lb_info.setText(f"Username or password incorrect.")
                print(f"User index: {index}")
                index += 1
        else:
            self.win_login.lb_info.setText(f"Fill in username and password.")

    def open_create_user(self):
        self.win_stack.setCurrentIndex(2)
        self.win_stack.setWindowTitle(self.current_state)
        self.win_stack.setFixedWidth(400)
        self.win_stack.setFixedHeight(400)

        if not self.users:
            self.win_create.btn_close.setEnabled(False)
        self.win_create.lb_info.setText(f"Password at least {Interface.PASSWORD_LENGTH} characters.")
        self.win_create.btn_create.clicked.connect(lambda: self.create_user())
        self.win_create.btn_close.clicked.connect(lambda: self.state_to_main())

    def create_user(self):
        username: str = self.win_create.in_username.text()
        password: str = self.win_create.in_password.text()
        retype: str = self.win_create.in_retype.text()

        print(f"in_username: {username}, in_password: {password}, in_retype: {retype}")

        if len(username) > 0:
            if len(password) >= Interface.PASSWORD_LENGTH:
                if password == retype:
                    user = User(username, password)
                    self.users.append(user)
                    self.win_create.in_username.setText("")
                    self.win_create.in_password.setText("")
                    self.win_create.in_retype.setText("")
                    self.state_to_main()
                else:
                    print("Password and retype inputs don't match.")
                    self.win_create.lb_info.setText(f"Password and retype don't match.")
            else:
                print(f"Password input length below {Interface.PASSWORD_LENGTH} chars.")
                self.win_create.lb_info.setText(f"Password at least {Interface.PASSWORD_LENGTH} characters.")
        else:
            print("Empty username input.")
            self.win_create.lb_info.setText(f"Fill in a username.")

    def fill_product_dropdowns(self):
        products = self.users[self.active_user_index].get_product_names()
        for dropdown in self.dropdown_products:
            dropdown.clear()  # clear first for refills
            if products:
                dropdown.insertItems(0, products)

        if products:
            print("Drop downs for Product select filled.")
            # print(f"Index {self.win_main.in_productSelect_add.currentIndex()} = {self.win_main.in_productSelect_add.currentText()}")

    def fill_shop_dropdowns(self):
        shops_remove = self.users[self.active_user_index].products[self.win_main.in_removeProduct.currentIndex()].get_shop_names()
        self.win_main.in_removeShop.clear()
        if shops_remove:
            self.win_main.in_removeShop.insertItems(0, shops_remove)
            print("Drop down for Shop select in Remove area filled.")

        shops_display = self.users[self.active_user_index].products[self.win_main.in_display_productSelect.currentIndex()].get_shop_names()
        self.win_main.in_display_shop.clear()
        if shops_display:
            self.win_main.in_display_shop.insertItems(0, shops_display)
            print("Drop down for Shop select in Display area filled.")

    def add_product(self):
        brand = self.win_main.in_productBrand.text()
        name = self.win_main.in_productName.text()
        message = ""

        if len(brand) > 0 and len(name) > 0:
            self.users[self.active_user_index].products.append(Product(brand, name))
            self.fill_product_dropdowns()
            message = "Product added."
        else:
            message = "Product brand or name is empty."

        print(message)
        self.win_main.lb_addProduct_message.setText(message)

    def add_product_shop(self):
        url: str = self.win_main.in_productShopUrl.text()
        index = self.win_main.in_productSelect_add.currentIndex()
        message = ""

        if len(url) > 0:
            for shop_type in Shop.SHOP_TYPES:
                if url.find(shop_type.lower()):
                    if shop_type == "Amazon":
                        self.users[self.active_user_index].products[index].add_shop(Amazon(url))
                        message = f"{shop_type} URL added for product {self.users[self.active_user_index].products[index].name}."
                else:
                    message = "Shop type not supported."
        else:
            message = "Shop URL field is empty."

        print(message)
        self.win_main.lb_addShop_message.setText(message)

    def remove_product(self):
        index = self.win_main.in_removeProduct.currentIndex()
        print(f"Product index = {index}")
        message = ""

        if index >= 0:
            message = f"Product {self.users[self.active_user_index].products[index].name} removed."
            del self.users[self.active_user_index].products[index]
        else:
            message = "No product selected."

        print(message)
        self.win_main.lb_remove_message.setText(message)

        try:
            self.fill_product_dropdowns()
            self.fill_shop_dropdowns()
        except:
            print("Dropdowns refill failed!")

    def remove_product_shop(self):
        try:
            product_index = self.win_main.in_removeProduct.currentIndex()
            shop_index = self.win_main.in_removeProductShop.currentIndex()
            print(f"product_index = {product_index}, shop_index = {shop_index}")
        except:
            print("Index input retrival failed!")
        message = ""

        if product_index >= 0 and shop_index >= 0:
            message = f"{self.users[self.active_user_index].products[product_index].shops[shop_index].name} shop removed."
            del self.users[self.active_user_index].products[product_index].shops[shop_index]
        else:
            message = "No product or shop selected."

        print(message)
        self.win_main.lb_remove_message.setText(message)

        try:
            self.fill_product_dropdowns()
            self.fill_shop_dropdowns()
        except:
            print("Dropdowns refill failed!")

    def show_info(self):
        print("Show_info called")
        self.fill_shop_dropdowns()

        self.users[self.active_user_index].products[self.win_main.in_removeProduct.currentIndex()].calculate_best_price()
        product = self.users[self.active_user_index].products[self.win_main.in_removeProduct.currentIndex()]

        # Product general info
        self.win_main.lb_display_brand.setText(product.brand)
        self.win_main.lb_display_name.setText(product.name)
        self.win_main.lb_display_ean.setText(product.ean)
        self.win_main.txt_display_description.setHtml(product.description)
        self.win_main.image.setHtml(
            f"""<img src="./images/{product.brand}_{product.name}" alt="Product image" width="200" height="200">"""
        )

        # Best price info
        self.win_main.lb_display_priceBest.setText(str(product.bestPrice))
        self.win_main.lb_display_priceBest_shop.setText(product.shops[product.bestPrice_shopIndex].name)
        self.win_main.txt_display_priceBest_url.setHtml(
            f"""<a href="{product.shops[product.bestPrice_shopIndex].url}">{product.shops[product.bestPrice_shopIndex].url}</a>""")

        # Shops
        index = self.win_main.in_display_shop.currentIndex()
        self.win_main.lb_display_shop_price.setText(str(product.shops[index].price))
        self.win_main.txt_display_shop_url.setHtml(
            f"""<a href="{product.shops[index].url}">{product.shops[index].url}</a>""")

    def test_data(self):
        self.users.append(User("Bavo", "123"))
        self.users.append(User("Fien", "123"))
        self.users[0].products.append(Product("Logi", "StreamCam"))
        self.users[0].products[0].ean = "5099206087187"
        self.users[0].products[0].description = "Webcam"
        self.users[0].products[0].image_url = "https://m.media-amazon.com/images/I/71JkixZlp-L._AC_SL1500_.jpg"
        self.users[0].products[0].shops.append(Amazon("https://www.amazon.de/-/en/Logitech-Streamcam-streaming-creation-Vertical/dp/B07W4DHNBF/ref=sr_1_3?crid=IH7NUNW228J9&keywords=streamcam&qid=1641734547&sprefix=streamcam%2Caps%2C77&sr=8-3"))
        self.users[0].products[0].shops[0].price = 159.00
        self.users[0].products.append(Product("Google", "Pixel 6"))
        self.users[0].products.append(Product("Bose", "QuietComfort 3"))


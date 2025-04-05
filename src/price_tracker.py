import os
import json
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tracked_products_file = os.path.join(root_dir, "data", "tracked_products.json")


class PriceTracker:

    def __init__(self, tracked_products=tracked_products_file):
        self.tracked_products = tracked_products

    common_price_selectors = [
        ".price",
        ".product-price",
        ".offer-price",
        ".current-price",
        '[itemprop="price"]',
        ".price_value",
        ".price-current",
        ".a-price",
        ".a-price",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        ".andes-money-amout_fraction",
    ]

    def format_thousand_separator(self, price_text, thousand_separator):
        if thousand_separator == ".":
            price_text = price_text.replace(".", "")
            price_text = price_text.replace(",", ".")
        else:
            price_text = price_text.replace(",", "")

        return price_text

    def clean_price(self, price_text):
        clean_price = re.sub(r"[^\d.]", "", price_text)
        match = re.search(r"\d+\.\d+|\d+", clean_price)

        return float(match.group()) if match else None

    def get_price(self, url, selector=None, thousand_separator=","):
        """Get the price of a product from a given URL"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                "Accept-Language": "en-US, en;q=0.9",
                "accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "origin": "https://www.amazon.ca",
                "referer": "https://www.amazon.ca/",
            }

            response = requests.get(url, headers=headers)
            print("Response status: ", response.status_code)

            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.text, "lxml")
            print("Soup: ", soup)

            price_el = None
            if selector:
                price_el = soup.select_one(selector)
            else:
                for default_selector in self.common_price_selectors:
                    price_el = soup.select_one(default_selector)
                    if price_el:
                        break

            print("Price element: ", price_el)
            if not price_el:
                return None

            price_text = price_el.get_text().strip()
            price_text = self.format_thousand_separator(price_text, thousand_separator)

            return self.clean_price(price_text)

        except Exception as e:
            print(f"Error getting price: {e}")
            return None

    def load_tracked_products(self):
        """Load the tracked products from the JSON file"""
        if not os.path.exists(self.tracked_products):
            return []

        with open(self.tracked_products, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_tracked_products(self, products):
        """Save the tracked products to the JSON file"""
        try:
            with open(self.tracked_products, "w", encoding="utf-8") as file:
                json.dump(products, file, indent=4)

            print("=> Tracked products saved successfully.")
            return True
        except Exception as e:
            print(f"Error saving tracked products: {e}")
            return False

    def add_product(
        self, name, url, desired_price, selector=None, thousand_separator=","
    ):
        """Add a product to the tracked products"""
        print("Adding product...")
        try:
            products = self.load_tracked_products()

            # Check if the product is already being tracked
            for product in products:
                if product["url"] == url:
                    return False

            current_price = self.get_price(url, selector, thousand_separator)

            # Check if the price could be obtained
            if current_price is None:
                return False

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            products.append(
                {
                    "name": name,
                    "url": url,
                    "desired_price": desired_price,
                    "current_price": current_price,
                    "selector": selector,
                    "thousand_separator": thousand_separator,
                    "created_at": date,
                    "price_history": [{"date": date, "price": current_price}],
                }
            )

            self.save_tracked_products(products)

            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    def update_prices(self):
        """Update tracked products"""
        products = self.load_tracked_products()
        print(f"load_tracked_products: {len(products)}")
        updated_products = []

        for product in products:
            thousand_separator = product.get("thousand_separator", ",")
            current_price = self.get_price(
                product["url"], product.get("selector"), thousand_separator
            )
            # print(f"current_price=> {current_price}")

            product["price_history"].append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "price": current_price,
                }
            )

            if current_price is not None:
                product["current_price"] = current_price
                # verify if price is equal or low than desired price
                if current_price <= product["desired_price"]:
                    updated_products.append(product)

        self.save_tracked_products(products)

        return updated_products

    def delete_products(self, index):
        """Delete products from traked_products"""
        products = self.load_tracked_products()

        if not products or index < 1 or index > len(products):
            return False

        products.pop(index - 1)
        self.save_tracked_products(products)

        return True

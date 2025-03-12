import os
import json
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup


class PriceTracker:
    def __init__(self, tracked_products="tracked_products.json"):
        self.tracked_products = tracked_products

    common_prices_selectors = [
        ".price",
        ".product-price",
        ".offer-price",
        ".current-price",
        '[itemprop="price"]',
        ".price_value",
        ".price-current",
        ".a-price .a-offscreen",
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
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "acept-language": "en-US,en;q=0.5",
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response != 200:
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            price_el = None
            if selector:
                price_el = soup.select_one(selector)
            else:
                for selector in self.common_prices_selectors:
                    price_el = soup.select_one(selector)
                    if price_el:
                        break

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

            return True
        except Exception as e:
            print(f"Error saving tracked products: {e}")
            return False

    def add_product(
        self, name, url, desired_price, selector=None, thousand_separator=","
    ):
        """Add a product to the tracked products"""
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

    def update_prices(self):
        """Update tracked products"""
        products = self.load_tracked_products()
        updated_products = []

        for product in products:
            thousand_separator = product.get("thousand_separator", ",")
            current_price = self.get_price(
                product["url"], product.get("selector"), thousand_separator
            )

            if current_price is not None:
                product["current_price"] = current_price

                # add to history
                product["price_history"].append(
                    {
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "precio": current_price,
                    }
                )

                # verify if price is equal or low than desired price
                if current_price <= product["desired_price"]:
                    updated_products.append(product)

        self.save_tracked_products(updated_products)
        return updated_products

    # TODO: delete product

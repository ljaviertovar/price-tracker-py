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
      '.price', '.product-price', '.offer-price', '.current-price', '[itemprop="price"]', '.price_value', '.price-current', '.a-price .a-offscreen', '#priceblock_ourprice', '#priceblock_dealprice', '.andes-money-amout_fraction'
    ]

    def format_thousand_separator(self, price_text, thousand_separator):
      if thousand_separator == '.':
        price_text = price_text.replace('.', '')
        price_text = price_text.replace(',', '.')
      else:
        price_text = price_text.replace(',', '')

      return price_text

    def clean_price(self, price_text):
      clean_price = re.sub(r'[^\d.]', '', price_text)
      match = re.search(r'\d+\.\d+|\d+', clean_price)

      return float(match.group()) if match else None


    def get_price(self, url, selector=None, thousand_separator=","):
        """Get the price of a product from a given URL"""

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                "acept-language": "en-US,en;q=0.5"
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response != 200:
                return None

            soup = BeautifulSoup(response.text, "html.parser")

            # If a selector is provided, use it to get the price
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
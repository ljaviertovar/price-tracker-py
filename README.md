# 📊 Price Tracker - Online Price Tracking

This is a **Price Tracker in Python** that allows you to track the prices of online products. You can add products, set a desired price, and receive alerts when the price drops.

---

## 🚀 Features

✅ Add and store products with a desired price  
✅ Check and update prices automatically  
✅ Display a price change history  
✅ Support for URL and number validation  
✅ Console interface with colorful messages (using `termcolor`)  
✅ Web scraping support to fetch real-time prices

---

## 🛠 Installation and Usage

### 1️⃣ Clone the repository

```sh
 git clone https://github.com/YOUR_USERNAME/price-tracker.git
 cd price-tracker
```

### 2️⃣ Install dependencies

```sh
pip install -r requirements.txt
```

### 3️⃣ Run the program

```sh
python main.py
```

---

## 🛠 How It Works

The core of the project is the `PriceTracker` class, which is responsible for tracking and updating product prices. It uses **BeautifulSoup** for web scraping and follows a structured process:

1. Fetches the webpage content of the given product URL.
2. Extracts the price using common selectors.
3. Cleans and formats the price to ensure accuracy.
4. Saves and updates the price history in a JSON file.
5. Checks if the price has dropped below the desired value.

---

## 📌 Screenshots

📸 **Main menu**

```
=== PRICE TRACKER ===
1. Track a new product
2. Show tracked products
3. Update prices
4. Delete a product
5. Exit
```

📊 **Example of an added product**

```
1. NAME: Laptop XYZ
   URL: https://example.com/laptop
   CURRENT PRICE: $999.99
   DESIRED PRICE: $850.00
   PRICE HISTORY:
    2024-03-01: $1050.00
    2024-03-10: $999.99
```

---

## 🖥 Technologies Used

- **Python 3.x**
- `BeautifulSoup` (for web scraping)
- `requests` (for HTTP requests)
- `json` (for storing product data)
- `re` (URL and number validation)
- `termcolor` (for colored messages)

---

## 🌟 Future Improvements

🔹 Email notifications when the price drops  
🔹 Graphical interface with **Tkinter** or **Flask**  
🔹 Support for multiple e-commerce platforms

---

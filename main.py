from price_tracker import PriceTracker


def show_products(tracker):
    products = tracker.load_tracked_products()

    if not products:
        print("\nThere is not products yet. Save one!")
        return

    print(f"\n=== TRACKED PRODUCTS ({len(products)}) ===")

    for i, product in enumerate(products, 1):
        print(f"\n{i}. {product['name']}")
        print(f"  URL: {product['url']}")
        print(f"  Current Price: {product.get('current_price', 'Not avilable')}")
        print(f"  Desired Price: {product['desired_price']}")

        # show history
        if product.get("price_history"):
            print("  Price History:")
            for register in product["price_history"][-3:]:
                print(f"  {register['date']}: {register['price']}")


def main():
    """Main menu"""
    print("=== PRICE TRACKER ===")

    tracker = PriceTracker()

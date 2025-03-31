from price_tracker import PriceTracker

tracker = PriceTracker()

print("\nUpdating prices...")

updated_prices = tracker.update_prices()
if updated_prices:
    print(
        f"\n{len(updated_prices)} product(s) have reached the desired price! :D\n",
    )

    for product in updated_prices:
        print(
            f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
        )
else:
    print("\nNo products have reached the disired price.")

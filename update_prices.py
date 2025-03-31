from price_tracker import PriceTracker

tracker = PriceTracker()

print("\n=> Updating prices...")

updated_prices = tracker.update_prices()
if updated_prices:
    print(
        f"\n\033[00m{len(updated_prices)} product(s) have reached the desired price! :D\033[00m\n",
    )

    for product in updated_prices:
        print(
            f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
        )
else:
    print("\n\033[93mNo products have reached the disired price.\033[00m\n")

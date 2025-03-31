from price_tracker import PriceTracker
from utils import log_message

tracker = PriceTracker()

print("\n=> Updating prices...")

updated_prices = tracker.update_prices()
if updated_prices:
    log_message(
        f"\n{len(updated_prices)} product(s) have reached the desired price! :D\n",
        " success",
    )

    for product in updated_prices:
        print(
            f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
        )
else:
    log_message("\nNo products have reached the disired price.", "warning")

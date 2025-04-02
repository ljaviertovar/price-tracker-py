from price_tracker import PriceTracker
from price_tracker_bot import send_message
from rich.console import Console

console = Console()

tracker = PriceTracker()

with console.status("\nUpdating prices...") as staus:

    updated_prices = tracker.update_prices()
    if updated_prices:
        message = (
            f"\n{len(updated_prices)} product(s) have reached the desired price! :D\n"
        )
        console.log(f"\n[green]{message}[/green]\n")
        send_message(message)

        for product in updated_prices:
            product_message = f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
            print(product_message)
            send_message(product_message)
    else:
        message = "\nNo products have reached the desired price.\n"
        console.log(f"\n[yellow]{message}[/yellow]")
        print("\nSending message...\n")
        send_message(message)

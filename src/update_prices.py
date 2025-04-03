from price_tracker import PriceTracker
from price_tracker_bot import send_message
from rich.console import Console

console = Console(force_terminal=True)

tracker = PriceTracker()

with console.status("Updating prices...", spinner="aesthetic"):

    updated_prices = tracker.update_prices()
    if updated_prices:
        message = f"{len(updated_prices)} product(s) have reached the desired price! 😁"
        console.log(f"\n[green]{message}[/green]\n")

        product_message = message + "\nUPDATED PRODUCTS:\n"
        for product in updated_prices:
            product_message += f"{product['name']} - {product['current_price']}\n"
        print(product_message)
        send_message(product_message)
    else:
        message = "No products have reached the desired price. 😕"
        console.log(f"\n[yellow]{message}\n[/yellow]")
        send_message(message)

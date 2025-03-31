from price_tracker import PriceTracker
from rich.console import Console

console = Console()

tracker = PriceTracker()

with console.status("\nUpdating prices...") as staus:

    updated_prices = tracker.update_prices()
    if updated_prices:
        console.log(
            f"\n[green]{len(updated_prices)} product(s) have reached the desired price! :D[/green]\n"
        )

        for product in updated_prices:
            print(
                f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
            )
    else:
        console.log("\n[yellow]No products have reached the disired price.[/yellow]\n")

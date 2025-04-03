from src.price_tracker import PriceTracker
from src.utils import log_message, input_message, is_valid_url, is_valid_number
from src.menu_helpers import show_products, get_valid_input


def main():
    """Main menu"""
    log_message("\n\n=== PRICE TRACKER ===", "info")

    tracker = PriceTracker()

    while True:

        log_message("\nMenu:", "info")
        log_message("1. Track a new product", "info")
        log_message("2. Show tracked products", "info")
        log_message("3. Update prices", "info")
        log_message("4. Delete a product", "info")
        log_message("5. Exit", "info")

        option = input_message("\nChoose an option: ")

        if option == "1":
            name = input_message("Product name: ")
            url = get_valid_input(
                "Product URL: ", is_valid_url, "Please enter a valid URL."
            )
            desired_price = float(
                get_valid_input(
                    "Desired price: ", is_valid_number, "Please enter a valid number."
                )
            )

            use_selector = (
                input_message("Do you want to use a selector? (y/n): ").lower().strip()
            )

            selector = None
            if use_selector == "y":
                selector = input_message("Enter the selector: ")

            thousand_separator = input_message(
                "Enter the thousand separator (default is ','): "
            ).strip()

            if thousand_separator not in [".", ","]:
                thousand_separator = ","
                log_message("Using default ','", "info")

            added_product = tracker.add_product(
                name, url, desired_price, selector, thousand_separator
            )

            if added_product:
                log_message(f"\nProduct {name} added successfully!", "success")
            else:
                log_message(
                    "\nProduct could not be added. Check if alredy exists.", "error"
                )

        elif option == "2":
            show_products(tracker)

        elif option == "3":
            print("\nUpdating prices...")

            updated_prices = tracker.update_prices()
            if updated_prices:
                log_message(
                    f"\n{len(updated_prices)} product(s) have reached the desired price! :D\n",
                    "success",
                )
                for product in updated_prices:
                    print(
                        f"PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
                    )
            else:
                log_message("\nNo products have reached the disired price.", "warning")

        elif option == "4":
            show_products(tracker)
            products = tracker.load_tracked_products()

            if products:
                product_to_delete = input_message(
                    "\nChoose the number of the product to delete: "
                )
                try:
                    index = int(product_to_delete)
                    print(index)
                    deleted = tracker.delete_products(index)
                    if deleted:
                        log_message("\nProduct deleted successfully!", "success")
                    else:
                        log_message("\nProduct not found.", "warning")
                except ValueError:
                    log_message(
                        f"\nProduct {product_to_delete} could not be deleted.", "error"
                    )

        elif option == "5":
            print("\nGoodbye!\n")
            exit()

        else:
            log_message("\n Oops! Please choose a valid option.", "warning")


if __name__ == "__main__":
    main()

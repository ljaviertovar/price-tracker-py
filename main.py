from termcolor import colored
import re
from price_tracker import PriceTracker


def log_message(message, level):
    if level == "info":
        # Print informational message in blue
        print(colored(message, "light_blue"))
    elif level == "warning":
        # Print warning message in yellow
        print(colored(message, "yellow"))
    elif level == "error":
        # Print error message in red
        print(colored(message, "red"))
    elif level == "success":
        # Print success message in green
        print(colored(message, "green"))


def input_message(message):
    return input(colored(message, "light_blue"))


def show_products(tracker):
    products = tracker.load_tracked_products()

    if not products:
        log_message("\nThere is not products yet. Save one!", "warning")
        return

    print(f"\n=== TRACKED PRODUCTS ({len(products)}) ===")

    for i, product in enumerate(products, 1):
        print(f"\n{i}. NAME: {product['name']}")
        print(f"   URL: {product['url']}")
        print(f"   CURRENT PRICE: {product.get('current_price', 'Not avilable')}")
        print(f"   DESIRED PRICE: {product['desired_price']}")

        # show history
        if product.get("price_history"):
            print("   PRICE HISTORY:")
            for register in product["price_history"][-3:]:
                print(f"    {register['date']}: {register['price']}")


def is_valid_url(url):
    # Regular expression for validating a URL
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ...or ipv4
        r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ...or ipv6
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return re.match(regex, url) is not None


def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


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
            url = input_message("Product URL: ")
            while not is_valid_url(url):
                log_message("Please enter a valid URL.", "error")
                url = input_message("Product URL: ")

            desired_price = input_message("Desired price: ")
            while not is_valid_number(desired_price):
                log_message("Please enter a valid price", "error")
                desired_price = input_message("Desired price: ")
            desired_price = float(desired_price)

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
                    f"\n{len(updated_prices)} product(s) have reached the desired price! :D",
                    "success",
                )
                for product in updated_prices:
                    print(
                        f"- PRODUCT: {product['name']} - NEW CURRENT PRICE: {product['current_price']}"
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
            break

        else:
            log_message("\n Oops! Please choose a valid option.", "warning")


main()

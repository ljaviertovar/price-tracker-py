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

    while True:

        print("1. Track a new product")
        print("2. Show tracked products")
        print("3. Update prices")
        print("4. Delete a product")
        print("5. Exit")

        option = input("\nChoose an option:")

        if option == "1":
            name= input("Product name: ")
            url= input("Product URL: ")
            desired_price= float(input("Desired price: ")).lower()

            use_selector = input("Do you want to use a selector to get the price? (y/n): ")
            selector= None

            if(use_selector == "y"):
                selector= input("Enter the selector: ")

            thousand_separator = input("Enter the thousand separator (default is ','): ").strip()
            if(thousand_separator not in ['.', ',']):
                thousand_separator = ','
                print("Invalid separator. Using default ','")

            added_product = tracker.add_product(name, url, desired_price, selector, thousand_separator)
            if added_product:
                print(f"\nProduct {name} added successfully!")
            else:
                print("\n Product could not be added. Check if alredy exists.")

        elif option == "2":
            show_products(tracker)

        elif option == "3":
            print("\nUpdating prices...")

            updated_prices = tracker.update_prices()
            if updated_prices:
                print(f"\n{len(updated_prices)} products have reached the desired price!")
                for product in updated_prices:
                    print(f"- {product['name']} - Current price: {product['current_price']}")
            else:
                print("\nNo products have reached the disired price.")

        elif option == "4":
            show_products(tracker)
            products = tracker.load_tracked_products()
            if products:
                try:
                    index = int(input("\nChoose the number of the product to delete: "))
                    deleted = tracker.delete_product(index)
                    if deleted:
                        print("\nProduct deleted successfully!")
                    else:
                        print(f"\nProduct {index} could not be deleted.")
                except ValueError:
                    print("\nInvalid product number. Please enter a valid number.")
            else:
                print("\n There are no products to delete.")

        elif option == "5":
            print("\nGoodbye!")
            break

        else:
            print("\n Invalid option. Please choose a valid option.")

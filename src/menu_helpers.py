from src.utils import log_message, input_message


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
        history = product.get("price_history", [])
        if history:
            print("   PRICE HISTORY:")
            for register in product["price_history"][-3:]:
                print(f"    {register['date']}: {register['price']}")


def get_valid_input(prompt, validation_func, error_msg):
    value = input_message(prompt)
    while not validation_func(value):
        log_message(error_msg, "error")
        value = input_message(prompt)
    return value

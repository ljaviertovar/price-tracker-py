import re
from termcolor import colored


def log_message(message, level):
    colors = {
        "info": "light_blue",
        "warning": "yellow",
        "error": "red",
        "success": "green",
    }
    print(colored(message, colors.get(level, "white")))  # Default white


def input_message(message):
    return input(colored(message, "light_blue"))


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

    return re.fullmatch(regex, url) is not None


def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

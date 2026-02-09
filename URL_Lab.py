import json
import os
import secrets
import string
from urllib.parse import urlparse

DATA_FILE = "urls.json"
MAX_CODE_LEN = 11  # must be < 12
ALLOWED_CODE_CHARS = string.ascii_letters + string.digits  # ASCII, URL-friendly


def is_valid_url(url: str) -> bool:
    """
    Basic validation:
    - must parse
    - must be http or https
    - must have a network location (domain)
    """
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


def is_valid_code(code: str) -> bool:
    """
    Code rules:
    - 1..MAX_CODE_LEN
    - ASCII letters/digits only (simple + safe)
    """
    if not (1 <= len(code) <= MAX_CODE_LEN):
        return False
    return all(c in ALLOWED_CODE_CHARS for c in code)


def load_data(filename: str):
    if not os.path.exists(filename):
        return {"code_to_url": {}, "url_to_code": {}}

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure keys exist
        data.setdefault("code_to_url", {})
        data.setdefault("url_to_code", {})
        # Ensure they are dicts
        if not isinstance(data["code_to_url"], dict) or not isinstance(data["url_to_code"], dict):
            raise ValueError("Invalid JSON structure")
        return data
    except (json.JSONDecodeError, OSError, ValueError):
        # If file is corrupted/unreadable, start fresh (or you could raise an error)
        return {"code_to_url": {}, "url_to_code": {}}


def save_data(filename: str, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def generate_unique_code(existing_codes: set) -> str:
    """
    Generate a random code (1..MAX_CODE_LEN) until it's unique.
    Use cryptographically strong randomness (secrets).
    """
    # Choose a fixed length for consistency; 7-11 is common. We'll use 8.
    length = 8
    length = min(length, MAX_CODE_LEN)

    while True:
        code = "".join(secrets.choice(ALLOWED_CODE_CHARS) for _ in range(length))
        if code not in existing_codes:
            return code


def shorten_url(data, long_url: str, custom_code: str | None = None) -> str:
    long_url = long_url.strip()

    if not is_valid_url(long_url):
        raise ValueError("Invalid URL. Must start with http:// or https:// and include a domain.")

    # If already shortened, return existing code (prevents duplicates)
    if long_url in data["url_to_code"]:
        return data["url_to_code"][long_url]

    existing_codes = set(data["code_to_url"].keys())

    if custom_code is not None and custom_code.strip() != "":
        code = custom_code.strip()
        if not is_valid_code(code):
            raise ValueError(f"Invalid code. Must be 1-{MAX_CODE_LEN} chars, ASCII letters/digits only.")
        if code in existing_codes:
            raise ValueError("That code is already taken. Choose another.")
    else:
        code = generate_unique_code(existing_codes)

    # Store both directions
    data["code_to_url"][code] = long_url
    data["url_to_code"][long_url] = code
    return code


def expand_code(data, code: str) -> str | None:
    code = code.strip()
    return data["code_to_url"].get(code)


def main():
    data = load_data(DATA_FILE)

    MENU = """
URL Shortener (JSON-backed)
1) Add/Shorten a URL
2) Search/Expand a code
3) Count shortened URLs
4) List all (debug)
5) Quit
"""

    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            long_url = input("Enter the long URL: ").strip()
            custom = input(f"Enter a custom code (1-{MAX_CODE_LEN} chars) or press Enter for random: ").strip()

            try:
                code = shorten_url(data, long_url, custom_code=custom if custom else None)
                save_data(DATA_FILE, data)
                print(f"\nSaved!\nShort code: {code}")
                print(f"Example short URL: https://myApp.com/{code}\n")
            except ValueError as e:
                print(f"\nError: {e}\n")

        elif choice == "2":
            code = input("Enter the short code: ").strip()
            url = expand_code(data, code)
            if url:
                print(f"\nFull URL: {url}\n")
            else:
                print("\nNot found: no URL stored for that code.\n")

        elif choice == "3":
            print(f"\nTotal shortened URLs: {len(data['code_to_url'])}\n")

        elif choice == "4":
            # Helpful for testing/demo
            if not data["code_to_url"]:
                print("\nNo URLs stored yet.\n")
            else:
                print("\nStored URLs:")
                for c, u in data["code_to_url"].items():
                    print(f"  {c} -> {u}")
                print()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Pick 1-5.\n")


if __name__ == "__main__":
    main()

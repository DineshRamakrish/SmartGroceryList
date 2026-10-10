import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("groceries.json")


def load_items():
    if DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as file:
            return json.load(file)
    return []


def save_items(items):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(items, file, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Create a reusable grocery list.")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Add something to the shopping list.")
    add.add_argument("name")
    add.add_argument("--quantity", default="1")
    commands.add_parser("list", help="Show items still needed.")
    bought = commands.add_parser("bought", help="Mark an item as bought.")
    bought.add_argument("id", type=int)
    commands.add_parser("clear-bought", help="Remove all bought items.")
    args = parser.parse_args()
    items = load_items()

    if args.command == "add":
        duplicate = next((item for item in items if item["name"].casefold() == args.name.casefold() and not item["bought"]), None)
        if duplicate:
            duplicate["quantity"] = args.quantity
            save_items(items)
            print(f'Updated {duplicate["name"]}: {args.quantity}')
        else:
            item_id = max((item["id"] for item in items), default=0) + 1
            items.append({"id": item_id, "name": args.name, "quantity": args.quantity, "bought": False})
            save_items(items)
            print(f"Added {args.name} (ID {item_id}).")
    elif args.command == "list":
        needed = [item for item in items if not item["bought"]]
        if not needed:
            print("Your shopping list is empty.")
        for item in needed:
            print(f'[{item["id"]}] {item["name"]} - {item["quantity"]}')
    elif args.command == "bought":
        item = next((item for item in items if item["id"] == args.id), None)
        if item is None:
            parser.error(f"No grocery item has ID {args.id}.")
        item["bought"] = True
        save_items(items)
        print(f'Marked as bought: {item["name"]}')
    else:
        remaining = [item for item in items if not item["bought"]]
        removed = len(items) - len(remaining)
        save_items(remaining)
        print(f"Cleared {removed} bought item(s).")


if __name__ == "__main__":
    main()

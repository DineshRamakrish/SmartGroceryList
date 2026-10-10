# Smart Grocery List

Keep a shopping list between trips. Add items, see what's still needed, mark
items bought, and clear completed items when you are ready for the next trip.

```text
python main.py add "Oats" --quantity "1 bag"
python main.py add "Apples" --quantity "6"
python main.py list
python main.py bought 1
python main.py clear-bought
```

Shopping data is saved in `groceries.json` and excluded from Git.

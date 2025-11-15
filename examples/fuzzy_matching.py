"""Fuzzy matching examples for blart TreeMap.

This script demonstrates the fuzzy search capabilities using
Levenshtein distance for approximate string matching.
"""

from blart import TreeMap


def main():
    print("=" * 60)
    print("Fuzzy Matching Examples")
    print("=" * 60)
    print()

    # ===== Basic Fuzzy Search =====
    print("1. Basic Fuzzy Search")
    print("-" * 40)

    tree = TreeMap(
        {"hello": 1, "hallo": 2, "hullo": 3, "help": 4, "world": 5, "word": 6}
    )

    print("All entries in tree:")
    for key, value in tree.items():
        print(f"  {key}: {value}")
    print()

    # Exact match (distance 0)
    print("Search for 'hello' with max_distance=0:")
    for key, value, distance in tree.fuzzy_search("hello", 0):
        print(f"  {key}: {value} (distance={distance})")
    print()

    # Close matches (distance 1)
    print("Search for 'hello' with max_distance=1:")
    for key, value, distance in tree.fuzzy_search("hello", 1):
        print(f"  {key}: {value} (distance={distance})")
    print()

    # Wider search (distance 2)
    print("Search for 'hello' with max_distance=2:")
    for key, value, distance in tree.fuzzy_search("hello", 2):
        print(f"  {key}: {value} (distance={distance})")
    print()

    # ===== Understanding Levenshtein Distance =====
    print("2. Understanding Levenshtein Distance")
    print("-" * 40)

    print("Levenshtein distance counts:")
    print("  - Insertions: 'cat' -> 'cats' (distance=1)")
    print("  - Deletions:  'cats' -> 'cat' (distance=1)")
    print("  - Substitutions: 'cat' -> 'bat' (distance=1)")
    print()

    examples = TreeMap(
        {
            "cat": "feline",
            "cats": "felines",
            "bat": "flying mammal",
            "rat": "rodent",
            "hat": "headwear",
            "car": "vehicle",
        }
    )

    search_term = "cat"
    print(f"Fuzzy search for '{search_term}' (max_distance=1):")
    results = sorted(examples.fuzzy_search(search_term, 1), key=lambda x: x[2])
    for key, value, distance in results:
        print(f"  {key}: distance={distance}")
    print()

    # ===== Real-World Use Case: Spell Checking =====
    print("3. Real-World Use Case: Spell Checking")
    print("-" * 40)

    dictionary = TreeMap(
        {
            "python": "A programming language",
            "program": "A set of instructions",
            "programming": "The act of writing programs",
            "programmer": "One who writes programs",
            "function": "A reusable block of code",
            "variable": "A named storage location",
            "algorithm": "A step-by-step procedure",
        }
    )

    def spell_check(word, max_distance=2):
        """Check spelling and suggest corrections."""
        suggestions = list(dictionary.fuzzy_search(word, max_distance))
        if not suggestions:
            return None
        # Sort by distance
        suggestions.sort(key=lambda x: x[2])
        return suggestions

    # Typo: "phyton" instead of "python"
    typo = "phyton"
    print(f"User typed: '{typo}'")
    suggestions = spell_check(typo)
    if suggestions:
        print("Did you mean:")
        for word, desc, distance in suggestions[:3]:
            print(f"  {word} (distance={distance})")
    print()

    # Typo: "progam" instead of "program"
    typo = "progam"
    print(f"User typed: '{typo}'")
    suggestions = spell_check(typo)
    if suggestions:
        print("Did you mean:")
        for word, desc, distance in suggestions[:3]:
            print(f"  {word} (distance={distance})")
    print()

    # ===== Real-World Use Case: Name Matching =====
    print("4. Real-World Use Case: Name Matching")
    print("-" * 40)

    users = TreeMap(
        {
            "john_smith": {"email": "john@example.com", "id": 1},
            "jane_smith": {"email": "jane@example.com", "id": 2},
            "jon_smyth": {"email": "jon@example.com", "id": 3},
            "alice_jones": {"email": "alice@example.com", "id": 4},
            "bob_johnson": {"email": "bob@example.com", "id": 5},
        }
    )

    def find_user(name, tolerance=2):
        """Find users with similar names."""
        matches = list(users.fuzzy_search(name, tolerance))
        matches.sort(key=lambda x: x[2])
        return matches

    # Search with potential typo
    search = "john_smyth"
    print(f"Searching for user: '{search}'")
    matches = find_user(search)
    if matches:
        print("Possible matches:")
        for username, user_data, distance in matches:
            print(f"  {username:15} (distance={distance}) - {user_data['email']}")
    print()

    # ===== Real-World Use Case: Command Correction =====
    print("5. Real-World Use Case: Command Correction")
    print("-" * 40)

    commands = TreeMap(
        {
            "list": "List items",
            "load": "Load file",
            "save": "Save file",
            "search": "Search items",
            "delete": "Delete item",
            "create": "Create item",
            "update": "Update item",
            "export": "Export data",
            "import": "Import data",
        }
    )

    def suggest_command(user_input, max_distance=2):
        """Suggest corrections for mistyped commands."""
        suggestions = list(commands.fuzzy_search(user_input, max_distance))
        suggestions.sort(key=lambda x: x[2])
        return suggestions

    # User makes typos
    typos = ["lst", "delte", "serch", "crete"]

    for typo in typos:
        print(f"User typed: '{typo}'")
        suggestions = suggest_command(typo)
        if suggestions:
            if suggestions[0][2] == 0:
                print(f"  Executing: {suggestions[0][0]}")
            else:
                print("  Command not found. Did you mean:")
                for cmd, desc, distance in suggestions[:3]:
                    print(f"    {cmd} (distance={distance})")
        print()

    # ===== Real-World Use Case: Product Search =====
    print("6. Real-World Use Case: Product Search")
    print("-" * 40)

    products = TreeMap(
        {
            "iphone_13": {"price": 799, "stock": 50},
            "iphone_14": {"price": 899, "stock": 30},
            "iphone_15": {"price": 999, "stock": 20},
            "samsung_galaxy": {"price": 849, "stock": 40},
            "samsung_note": {"price": 949, "stock": 15},
            "macbook_pro": {"price": 1999, "stock": 10},
            "macbook_air": {"price": 1299, "stock": 25},
        }
    )

    def search_products(query, max_distance=3):
        """Search products with fuzzy matching."""
        results = list(products.fuzzy_search(query, max_distance))
        results.sort(key=lambda x: x[2])
        return results

    # User searches with typos
    queries = ["iphone", "mackbook", "samsng"]

    for query in queries:
        print(f"User searches for: '{query}'")
        results = search_products(query)
        if results:
            print("  Found products:")
            for name, info, distance in results[:3]:
                print(
                    f"    {name:20} ${info['price']:4} (match quality: {3-distance}/3)"
                )
        print()

    # ===== Combining Prefix and Fuzzy Search =====
    print("7. Combining Prefix and Fuzzy Search")
    print("-" * 40)

    cities = TreeMap(
        {
            "new_york": "USA",
            "new_delhi": "India",
            "new_orleans": "USA",
            "newcastle": "UK",
            "san_francisco": "USA",
            "san_diego": "USA",
            "santa_monica": "USA",
            "los_angeles": "USA",
        }
    )

    # First filter by prefix, then apply fuzzy matching on user input
    def smart_search(query, prefix=None, max_distance=2):
        """Smart search combining prefix and fuzzy matching."""
        if prefix:
            # First get all with prefix
            candidates = TreeMap({k: v for k, v in cities.prefix_iter(prefix)})
            # Then fuzzy search within candidates
            results = list(candidates.fuzzy_search(query, max_distance))
        else:
            results = list(cities.fuzzy_search(query, max_distance))

        results.sort(key=lambda x: x[2])
        return results

    # Search within "new_*" cities
    print("Search for 'new_yurk' within 'new_' prefix:")
    results = smart_search("new_yurk", prefix="new_")
    for city, country, distance in results:
        print(f"  {city:20} {country:10} (distance={distance})")
    print()

    # General search
    print("Search for 'los_angles' (general):")
    results = smart_search("los_angles")
    for city, country, distance in results[:3]:
        print(f"  {city:20} {country:10} (distance={distance})")
    print()

    # ===== Performance with Larger Dataset =====
    print("8. Performance with Larger Dataset")
    print("-" * 40)

    # Create a larger tree
    large_tree = TreeMap()
    words = [
        "algorithm",
        "data",
        "structure",
        "function",
        "variable",
        "class",
        "object",
        "method",
        "property",
        "interface",
        "implementation",
        "abstract",
        "concrete",
        "inherit",
        "polymorphism",
    ]

    for i in range(1000):
        for word in words:
            key = f"{word}_{i:04d}"
            large_tree[key] = i

    print(f"Created tree with {len(large_tree)} entries")

    # Fuzzy search
    search_term = "algorthm_0050"  # Typo in "algorithm"
    matches = list(large_tree.fuzzy_search(search_term, 2))
    print(f"Fuzzy search for '{search_term}' found {len(matches)} matches")
    if matches:
        print("Best matches:")
        for key, value, distance in sorted(matches, key=lambda x: x[2])[:5]:
            print(f"  {key}: {value} (distance={distance})")
    print()

    print("=" * 60)
    print("Fuzzy matching examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

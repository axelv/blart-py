"""Basic usage examples for blart TreeMap.

This script demonstrates the fundamental operations of TreeMap,
including creation, insertion, retrieval, deletion, and iteration.
"""

from blart import TreeMap


def main():
    print("=" * 60)
    print("Basic TreeMap Usage Examples")
    print("=" * 60)
    print()

    # ===== Creating TreeMaps =====
    print("1. Creating TreeMaps")
    print("-" * 40)

    # Empty TreeMap
    tree = TreeMap()
    print(f"Empty tree: {tree}")
    print(f"Is empty: {tree.is_empty()}")
    print()

    # From dictionary
    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    print(f"From dict: {tree}")
    print(f"Length: {len(tree)}")
    print()

    # From list of tuples
    tree = TreeMap([("dog", "woof"), ("cat", "meow"), ("bird", "tweet")])
    print(f"From tuples: {tree}")
    print()

    # ===== Inserting and Updating =====
    print("2. Inserting and Updating Values")
    print("-" * 40)

    tree = TreeMap()

    # Using insert method
    tree.insert("hello", "world")
    print(f"After insert('hello', 'world'): {tree}")

    # Using subscript notation
    tree["python"] = "programming"
    tree["rust"] = "systems"
    print(f"After tree['python'] = 'programming': {tree}")
    print()

    # Updating existing values
    tree["hello"] = "universe"
    print(f"After updating 'hello': tree['hello'] = {tree['hello']}")
    print()

    # ===== Retrieving Values =====
    print("3. Retrieving Values")
    print("-" * 40)

    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})

    # Using subscript notation
    print(f"tree['apple'] = {tree['apple']}")

    # Using get method
    print(f"tree.get('banana') = {tree.get('banana')}")
    print(f"tree.get('orange') = {tree.get('orange')}")
    print(f"tree.get('orange', 'not found') = {tree.get('orange', 'not found')}")
    print()

    # Checking membership
    print(f"'apple' in tree: {'apple' in tree}")
    print(f"'orange' in tree: {'orange' in tree}")
    print()

    # ===== Deleting Values =====
    print("4. Deleting Values")
    print("-" * 40)

    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3})
    print(f"Initial: {list(tree.items())}")

    # Using del statement
    del tree["banana"]
    print(f"After del tree['banana']: {list(tree.items())}")

    # Using remove method
    value = tree.remove("apple")
    print(f"Removed 'apple' with value: {value}")
    print(f"After remove: {list(tree.items())}")
    print()

    # Clear all entries
    tree.clear()
    print(f"After clear(): {tree}")
    print()

    # ===== Iteration =====
    print("5. Iteration (Ordered by Key)")
    print("-" * 40)

    tree = TreeMap({"zebra": 26, "apple": 1, "mango": 13, "banana": 2, "cherry": 3})

    print("Iterating over keys (sorted):")
    for key in tree:
        print(f"  {key}")
    print()

    print("Using keys() method:")
    for key in tree.keys():
        print(f"  {key}")
    print()

    print("Using values() method:")
    for value in tree.values():
        print(f"  {value}")
    print()

    print("Using items() method:")
    for key, value in tree.items():
        print(f"  {key}: {value}")
    print()

    # ===== Boundary Operations =====
    print("6. Boundary Operations")
    print("-" * 40)

    tree = TreeMap({"apple": 1, "banana": 2, "cherry": 3, "date": 4})

    print(f"First entry: {tree.first()}")
    print(f"Last entry: {tree.last()}")
    print()

    print(f"Pop first: {tree.pop_first()}")
    print(f"Pop last: {tree.pop_last()}")
    print(f"Remaining: {list(tree.items())}")
    print()

    # ===== Working with Different Value Types =====
    print("7. Different Value Types")
    print("-" * 40)

    tree = TreeMap()
    tree["number"] = 42
    tree["string"] = "hello"
    tree["list"] = [1, 2, 3]
    tree["dict"] = {"nested": "value"}
    tree["none"] = None

    print("TreeMap can store any Python object:")
    for key, value in tree.items():
        print(f"  {key}: {value} (type: {type(value).__name__})")
    print()

    # ===== Unicode Support =====
    print("8. Unicode Support")
    print("-" * 40)

    tree = TreeMap(
        {
            "hello": "English",
            "你好": "Chinese",
            "こんにちは": "Japanese",
            "مرحبا": "Arabic",
            "🚀": "Rocket emoji",
            "🐍": "Snake emoji",
        }
    )

    print("Unicode keys and values work seamlessly:")
    for key, value in tree.items():
        print(f"  {key}: {value}")
    print()

    # ===== Error Handling =====
    print("9. Error Handling")
    print("-" * 40)

    tree = TreeMap({"apple": 1})

    # KeyError on missing key
    try:
        value = tree["missing"]
    except KeyError as e:
        print(f"KeyError when accessing missing key: {e}")

    # Safe access with get
    value = tree.get("missing", "default")
    print(f"Safe access with get(): {value}")
    print()

    # TypeError on non-string key
    try:
        tree[123] = "value"
    except TypeError as e:
        print(f"TypeError when using non-string key: {e}")
    print()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

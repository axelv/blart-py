"""Prefix query examples for blart TreeMap.

This script demonstrates the powerful prefix query capabilities
of TreeMap, which is one of the key advantages of adaptive radix trees.
"""

from blart import TreeMap


def main():
    print("=" * 60)
    print("Prefix Query Examples")
    print("=" * 60)
    print()

    # ===== Basic Prefix Queries =====
    print("1. Basic Prefix Queries")
    print("-" * 40)

    tree = TreeMap(
        {
            "apple": 1,
            "application": 2,
            "apply": 3,
            "apricot": 4,
            "banana": 5,
            "band": 6,
            "bandana": 7,
            "cherry": 8,
        }
    )

    print("All entries in tree:")
    for key, value in tree.items():
        print(f"  {key}: {value}")
    print()

    # Get first match
    print("Get first entry with prefix 'app':")
    result = tree.get_prefix("app")
    if result:
        key, value = result
        print(f"  Found: {key} = {value}")
    print()

    # Get all matches
    print("Get all entries with prefix 'app':")
    for key, value in tree.prefix_iter("app"):
        print(f"  {key}: {value}")
    print()

    print("Get all entries with prefix 'ban':")
    for key, value in tree.prefix_iter("ban"):
        print(f"  {key}: {value}")
    print()

    # ===== Empty Prefix =====
    print("2. Empty Prefix (Matches All)")
    print("-" * 40)

    print("Empty prefix matches all entries:")
    count = 0
    for key, value in tree.prefix_iter(""):
        count += 1
    print(f"  Total entries: {count}")
    print()

    # ===== No Matches =====
    print("3. Handling No Matches")
    print("-" * 40)

    result = tree.get_prefix("xyz")
    print(f"get_prefix('xyz'): {result}")

    matches = list(tree.prefix_iter("xyz"))
    print(f"prefix_iter('xyz'): {matches}")
    print()

    # ===== Real-World Use Cases =====
    print("4. Real-World Use Case: Command Completion")
    print("-" * 40)

    # Build a command tree
    commands = TreeMap(
        {
            "list": "List all items",
            "list-users": "List all users",
            "list-files": "List all files",
            "load": "Load configuration",
            "load-config": "Load config file",
            "save": "Save current state",
            "save-config": "Save config file",
            "search": "Search for items",
            "search-by-name": "Search by name",
            "search-by-date": "Search by date",
        }
    )

    # Simulate command completion
    user_input = "li"
    print(f"User types: '{user_input}'")
    print("Available completions:")
    for cmd, desc in commands.prefix_iter(user_input):
        print(f"  {cmd:20} - {desc}")
    print()

    user_input = "list-"
    print(f"User types: '{user_input}'")
    print("Available completions:")
    for cmd, desc in commands.prefix_iter(user_input):
        print(f"  {cmd:20} - {desc}")
    print()

    # ===== Real-World Use Case: Autocomplete =====
    print("5. Real-World Use Case: Autocomplete")
    print("-" * 40)

    # Dictionary of programming languages
    languages = TreeMap(
        {
            "python": "High-level programming language",
            "javascript": "Web programming language",
            "java": "Enterprise programming language",
            "julia": "Scientific computing language",
            "rust": "Systems programming language",
            "ruby": "Dynamic programming language",
            "go": "Concurrent programming language",
            "c": "Low-level programming language",
            "c++": "Object-oriented systems language",
            "c#": "Microsoft's programming language",
        }
    )

    def autocomplete(prefix, max_results=5):
        """Show autocomplete suggestions."""
        results = []
        for key, value in languages.prefix_iter(prefix):
            results.append((key, value))
            if len(results) >= max_results:
                break
        return results

    print("Autocomplete for 'py':")
    for lang, desc in autocomplete("py"):
        print(f"  {lang:15} - {desc}")
    print()

    print("Autocomplete for 'ja':")
    for lang, desc in autocomplete("ja"):
        print(f"  {lang:15} - {desc}")
    print()

    print("Autocomplete for 'c':")
    for lang, desc in autocomplete("c", max_results=3):
        print(f"  {lang:15} - {desc}")
    print()

    # ===== Real-World Use Case: File System Paths =====
    print("6. Real-World Use Case: File System Paths")
    print("-" * 40)

    filesystem = TreeMap(
        {
            "/home/user/documents/report.pdf": 1024,
            "/home/user/documents/notes.txt": 256,
            "/home/user/downloads/file.zip": 2048,
            "/home/user/downloads/image.png": 512,
            "/home/admin/config.yml": 128,
            "/var/log/system.log": 4096,
            "/var/log/error.log": 1024,
            "/usr/bin/python": 8192,
        }
    )

    def list_directory(path_prefix):
        """List all files under a path prefix."""
        files = []
        for path, size in filesystem.prefix_iter(path_prefix):
            files.append((path, size))
        return files

    print("Files in /home/user/documents/:")
    for path, size in list_directory("/home/user/documents/"):
        print(f"  {path:45} {size:5} bytes")
    print()

    print("Files in /var/log/:")
    for path, size in list_directory("/var/log/"):
        print(f"  {path:45} {size:5} bytes")
    print()

    # ===== Real-World Use Case: URL Routing =====
    print("7. Real-World Use Case: URL Routing")
    print("-" * 40)

    routes = TreeMap(
        {
            "/api/users": "List users",
            "/api/users/create": "Create user",
            "/api/users/delete": "Delete user",
            "/api/products": "List products",
            "/api/products/search": "Search products",
            "/admin": "Admin dashboard",
            "/admin/users": "Manage users",
            "/admin/settings": "System settings",
        }
    )

    def find_routes(path_prefix):
        """Find all routes matching a prefix."""
        return list(routes.prefix_iter(path_prefix))

    print("All /api/ routes:")
    for route, handler in find_routes("/api/"):
        print(f"  {route:30} -> {handler}")
    print()

    print("All /admin routes:")
    for route, handler in find_routes("/admin"):
        print(f"  {route:30} -> {handler}")
    print()

    # ===== Performance Demonstration =====
    print("8. Performance with Large Dataset")
    print("-" * 40)

    # Create a large tree
    large_tree = TreeMap()
    for i in range(10000):
        large_tree[f"item_{i:05d}"] = i

    print(f"Created tree with {len(large_tree)} entries")

    # Prefix query is very fast
    prefix = "item_99"
    matches = list(large_tree.prefix_iter(prefix))
    print(f"Found {len(matches)} entries starting with '{prefix}'")
    print("First 5 matches:")
    for key, value in matches[:5]:
        print(f"  {key}: {value}")
    print()

    print("=" * 60)
    print("Prefix query examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()

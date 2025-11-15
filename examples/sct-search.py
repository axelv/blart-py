#!/usr/bin/env python3
"""
SNOMED CT Term Search CLI with Tab Completion and Multi-Language Support.

Interactive search tool for SNOMED CT medical terms using TreeMap
with readline-based tab completion, fuzzy matching, and language switching.

Loads SNOMED CT RF2 release directories and supports all available languages.
"""

import glob
import re
import readline
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from blart import TreeMap


def find_description_files(rf2_path: Path) -> Dict[str, Path]:
    """
    Find all SNOMED CT description files in an RF2 release directory.

    Args:
        rf2_path: Path to RF2 release root directory

    Returns:
        Dict mapping language codes to file paths
        Example: {"en": Path(...), "nl": Path(...)}
    """
    snapshot_dir = rf2_path / "Snapshot" / "Terminology"

    if not snapshot_dir.exists():
        return {}

    description_files = {}
    pattern = snapshot_dir / "sct2_Description_Snapshot-*.txt"

    for file_path in glob.glob(str(pattern)):
        path = Path(file_path)
        # Extract language code from filename
        # Format: sct2_Description_Snapshot-{lang}_{rest}.txt
        match = re.search(r"sct2_Description_Snapshot-([a-z]{2})_", path.name)
        if match:
            lang_code = match.group(1)
            description_files[lang_code] = path

    return description_files


def load_description_file(file_path: Path) -> TreeMap:
    """
    Load a single SNOMED CT description file into a TreeMap.

    Args:
        file_path: Path to tab-separated description file

    Returns:
        TreeMap with terms as keys and concept IDs as values
    """
    tree = TreeMap()
    count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        # Skip header line
        next(f)

        for line in f:
            fields = line.strip().split("\t")
            if len(fields) >= 9:
                # Column 5 (index 4) = conceptId
                # Column 8 (index 7) = term
                concept_id = fields[4].strip()
                term = fields[7].strip()

                if term and concept_id:
                    tree[term] = concept_id
                    count += 1

    return tree


class SnomedCompleter:
    """Readline completer for SNOMED CT terms using TreeMap."""

    def __init__(self, tree: TreeMap):
        self.tree = tree
        self.matches: List[Tuple[str, str]] = []

    def complete(self, text: str, state: int) -> Optional[str]:
        """
        Completer function called by readline.

        Args:
            text: The text to complete
            state: The completion state (0 = first call, 1+ = subsequent)

        Returns:
            The completion string, or None when exhausted
        """
        if state == 0:
            # First call: generate all matches
            if text:
                # Use TreeMap's efficient prefix search
                self.matches = list(self.tree.prefix_iter(text))
            else:
                self.matches = []

        # Return the state'th match
        try:
            term, _concept_id = self.matches[state]
            return term
        except IndexError:
            return None


class SnomedCLI:
    """Interactive CLI for searching SNOMED CT terms with multi-language support."""

    def __init__(self, trees: Dict[str, TreeMap]):
        self.trees = trees
        # Default to Dutch if available, otherwise first available language
        self.current_lang = "nl" if "nl" in trees else sorted(trees.keys())[0]
        self.completer = SnomedCompleter(trees[self.current_lang])
        self.history_file = Path.home() / ".snomed_search_history"
        self.setup_readline()

    def setup_readline(self) -> None:
        """Configure readline for tab completion and history."""
        # Set completer
        readline.set_completer(self.completer.complete)

        # Enable tab completion
        readline.parse_and_bind("tab: complete")

        # Load history if exists
        if self.history_file.exists():
            try:
                readline.read_history_file(str(self.history_file))
            except Exception:
                pass  # Ignore history errors

        # Set history length
        readline.set_history_length(1000)

        # Save history on exit
        import atexit

        atexit.register(self.save_history)

    def save_history(self) -> None:
        """Save command history to file."""
        try:
            readline.write_history_file(str(self.history_file))
        except Exception:
            pass  # Ignore save errors

    def run(self) -> None:
        """Run the interactive REPL."""
        self.print_banner()

        while True:
            try:
                # Read user input with language indicator in prompt
                prompt = f"search[{self.current_lang}]> "
                user_input = input(prompt).strip()

                # Handle exit commands
                if user_input.lower() in ("quit", "exit", "q"):
                    print("Goodbye!")
                    break

                # Handle help command
                if user_input.lower() in ("help", "?"):
                    self.print_help()
                    continue

                # Handle stats command
                if user_input.lower() == "stats":
                    self.print_stats()
                    continue

                # Handle language switching command
                if user_input.lower() == "lang":
                    self.switch_language()
                    continue

                # Skip empty input
                if not user_input:
                    continue

                # Execute search
                self.execute_search(user_input)

            except KeyboardInterrupt:
                print("\n(Use 'quit' to exit)")
                continue
            except EOFError:
                print("\nGoodbye!")
                break

    def print_banner(self) -> None:
        """Print welcome banner."""
        print("=" * 60)
        print("SNOMED CT Term Search CLI")
        print("=" * 60)

        # Show available languages
        lang_info = []
        for lang in sorted(self.trees.keys()):
            count = len(self.trees[lang])
            marker = " [CURRENT]" if lang == self.current_lang else ""
            lang_info.append(f"  {lang}: {count:,} terms{marker}")

        print("Available languages:")
        for info in lang_info:
            print(info)

        print("\nCommands:")
        print("  - Type a term prefix and press TAB for completions")
        print("  - Press ENTER to search and show top 10 results")
        print("  - Type 'lang' to switch language")
        print("  - Type 'help' for more commands")
        print("  - Type 'quit' or press Ctrl+D to exit")
        print("=" * 60)
        print()

    def print_help(self) -> None:
        """Print help information."""
        print("\nAvailable commands:")
        print("  help, ?     - Show this help message")
        print("  stats       - Show database statistics for current language")
        print("  lang        - Switch language (interactive menu)")
        print("  quit, exit  - Exit the program")
        print("\nSearch tips:")
        print("  - Use TAB for auto-completion")
        print("  - Prefix matching is case-sensitive")
        print("  - Both prefix and fuzzy matching (edit distance ≤ 2)")
        print("  - Results show term → concept ID")
        print()

    def print_stats(self) -> None:
        """Print database statistics for current language."""
        tree = self.trees[self.current_lang]
        print(f"\nDatabase Statistics ({self.current_lang.upper()}):")
        print(f"  Total terms: {len(tree):,}")
        print(f"  Empty: {tree.is_empty()}")
        if not tree.is_empty():
            first = tree.first()
            last = tree.last()
            if first:
                print(f"  First term: {first[0]}")
            if last:
                print(f"  Last term: {last[0]}")
        print()

    def execute_search(self, term: str) -> None:
        """
        Execute both prefix and fuzzy searches, displaying top 10 results from each.

        Args:
            term: The search term/prefix
        """
        tree = self.trees[self.current_lang]

        # Execute prefix search
        start = time.time()
        prefix_matches = list(tree.prefix_iter(term))
        prefix_elapsed = (time.time() - start) * 1000  # Convert to ms

        # Execute fuzzy search with max edit distance of 2
        start = time.time()
        fuzzy_matches = list(tree.fuzzy_search(term, 2))
        fuzzy_elapsed = (time.time() - start) * 1000  # Convert to ms

        # Filter fuzzy matches to exclude those already in prefix results
        prefix_terms = {match_term for match_term, _ in prefix_matches}
        unique_fuzzy_matches = [
            (match_term, concept_id, distance)
            for match_term, concept_id, distance in fuzzy_matches
            if match_term not in prefix_terms
        ]

        # Check if we have any results
        if not prefix_matches and not unique_fuzzy_matches:
            print(f"No matches found for '{term}'")
            return

        print()  # Blank line before results

        # Display prefix matches
        if prefix_matches:
            print(
                f"Prefix matches: {len(prefix_matches)} found in {prefix_elapsed:.2f}ms"
            )
            print("-" * 60)
            for i, (match_term, concept_id) in enumerate(prefix_matches[:10], 1):
                print(f"  {i:2}. {match_term}")
                print(f"      → Concept ID: {concept_id}")

            if len(prefix_matches) > 10:
                print(f"\n  ... and {len(prefix_matches) - 10} more matches")
            print("-" * 60)
        else:
            print("No exact prefix matches")
            print("-" * 60)

        # Display fuzzy matches
        print()  # Blank line between sections
        if unique_fuzzy_matches:
            print(
                f"Fuzzy matches (edit distance ≤ 2): {len(unique_fuzzy_matches)} found in {fuzzy_elapsed:.2f}ms"
            )
            print("-" * 60)
            for i, (match_term, concept_id, distance) in enumerate(
                unique_fuzzy_matches[:10], 1
            ):
                print(f"  {i:2}. {match_term} (distance: {distance})")
                print(f"      → Concept ID: {concept_id}")

            if len(unique_fuzzy_matches) > 10:
                print(f"\n  ... and {len(unique_fuzzy_matches) - 10} more matches")
            print("-" * 60)
        else:
            print("No fuzzy matches found")
            print("-" * 60)

        print()  # Blank line after results

    def switch_language(self) -> None:
        """Interactive language switching menu."""
        if len(self.trees) == 1:
            print("Only one language available")
            return

        print("\nAvailable languages:")
        lang_list = sorted(self.trees.keys())

        for i, lang in enumerate(lang_list, 1):
            count = len(self.trees[lang])
            marker = " [CURRENT]" if lang == self.current_lang else ""
            print(f"  {i}. {lang} - {count:,} terms{marker}")

        try:
            choice = input(f"\nSelect language (1-{len(lang_list)}): ").strip()

            if not choice:
                print("Cancelled")
                return

            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(lang_list):
                new_lang = lang_list[choice_idx]

                if new_lang == self.current_lang:
                    print(f"Already using {new_lang.upper()}")
                    return

                # Update current language
                self.current_lang = new_lang

                # Update completer to use new language's tree
                self.completer.tree = self.trees[new_lang]

                count = len(self.trees[new_lang])
                print(f"✓ Switched to {new_lang.upper()} ({count:,} terms)")
            else:
                print("Invalid selection")

        except ValueError:
            print("Invalid input")
        except KeyboardInterrupt:
            print("\nCancelled")


def load_snomed_terms(rf2_path: Path) -> Dict[str, TreeMap]:
    """
    Load SNOMED CT terms from RF2 release directory.

    Args:
        rf2_path: Path to RF2 release directory (containing Snapshot/Terminology/)

    Returns:
        Dict mapping language codes to TreeMaps
        Example: {"en": TreeMap, "nl": TreeMap, "fr": TreeMap, "de": TreeMap}

    Raises:
        FileNotFoundError: If path doesn't exist
        ValueError: If path is not a directory or no description files found
    """
    if not rf2_path.exists():
        raise FileNotFoundError(f"Path not found: {rf2_path}")

    if not rf2_path.is_dir():
        raise ValueError(f"Path must be a directory, got: {rf2_path}")

    print(f"Loading SNOMED CT from RF2 directory: {rf2_path.name}")
    description_files = find_description_files(rf2_path)

    if not description_files:
        raise ValueError(f"No SNOMED description files found in {rf2_path}")

    trees = {}

    # Load each language
    for lang_code in sorted(description_files.keys()):
        file_path = description_files[lang_code]
        print(f"\nLoading {lang_code.upper()} from {file_path.name}...")
        start_time = time.time()

        tree = load_description_file(file_path)
        elapsed = time.time() - start_time

        trees[lang_code] = tree
        term_count = len(tree)
        print(f"✓ Loaded {term_count:,} unique terms in {elapsed:.2f} seconds")
        if elapsed > 0:
            print(f"  ({term_count/elapsed:.0f} terms/second)")

    print()  # Blank line after loading
    return trees


def main() -> int:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Error: RF2 directory path required", file=sys.stderr)
        print("\nUsage:", file=sys.stderr)
        print(f"  {sys.argv[0]} <rf2_directory>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print(f"  {sys.argv[0]} /path/to/SnomedCT_Release/", file=sys.stderr)
        return 1

    rf2_path = Path(sys.argv[1])

    try:
        # Load data from RF2 directory
        trees = load_snomed_terms(rf2_path)

        # Run CLI
        cli = SnomedCLI(trees)
        cli.run()

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

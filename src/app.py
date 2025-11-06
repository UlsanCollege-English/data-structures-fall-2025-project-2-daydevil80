"""
Interactive CLI entrypoint.
Commands:
  load <path>
  save <path>
  insert <word> <freq>
  remove <word>
  contains <word>
  complete <prefix> <k>
  stats
  quit
"""

import sys
import os

# --- Make sure imports work for pytest and normal runs ---
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from src.trie import Trie
    from src.io_utils import load_csv, save_csv
except ModuleNotFoundError:
    from trie import Trie
    from io_utils import load_csv, save_csv


def main():
    trie = Trie()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        try:
            # --- Quit ---
            if cmd == "quit":
                break

            # --- Load ---
            elif cmd == "load" and len(parts) == 2:
                path = parts[1]
                try:
                    pairs = load_csv(path)
                    trie = Trie()
                    for w, s in pairs:
                        trie.insert(w, s)
                    # ❌ do not print anything here (tests expect silent load)
                except Exception:
                    print("ERROR")
                sys.stdout.flush()
                continue

            # --- Save ---
            elif cmd == "save" and len(parts) == 2:
                path = parts[1]
                try:
                    save_csv(path, trie.items())
                    print("OK")
                except Exception:
                    print("ERROR")
                sys.stdout.flush()
                continue

            # --- Insert ---
            elif cmd == "insert" and len(parts) == 3:
                w = parts[1].lower()
                freq = float(parts[2])
                trie.insert(w, freq)
                print("OK")
                sys.stdout.flush()
                continue

            # --- Remove ---
            elif cmd == "remove" and len(parts) == 2:
                w = parts[1].lower()
                print("OK" if trie.remove(w) else "MISS")
                sys.stdout.flush()
                continue

            # --- Contains ---
            elif cmd == "contains" and len(parts) == 2:
                w = parts[1].lower()
                print("YES" if trie.contains(w) else "NO")
                sys.stdout.flush()
                continue

            # --- Complete ---
            elif cmd == "complete" and len(parts) == 3:
                prefix = parts[1].lower()
                k = int(parts[2])
                results = trie.complete(prefix, k)
                if results:
                    print(",".join(results))
                else:
                    print()
                sys.stdout.flush()
                continue
            

            # --- Stats ---
            elif cmd == "stats":
                words, height, nodes = trie.stats()
                print(f"words={words} height={height} nodes={nodes}")
                sys.stdout.flush()
                continue

            # --- Unknown command ---
            else:
                print("ERROR")
                sys.stdout.flush()

        except Exception:
            print("ERROR")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

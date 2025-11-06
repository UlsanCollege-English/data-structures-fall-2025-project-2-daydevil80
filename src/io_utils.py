"""CSV load/save helpers for (word, score) pairs."""

import csv

def load_csv(path):
    words = []
    with open(path, newline='', encoding='utf-8') as f:
        for row in csv.reader(f):
            if not row:
                continue
            w = row[0].strip().lower()
            try:
                s = float(row[1]) if len(row) > 1 else 0.0
            except ValueError:
                s = 0.0
            words.append((w, s))
    return words


def save_csv(path, items):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for w, s in items:
            writer.writerow([w, s])



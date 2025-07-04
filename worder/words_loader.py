import csv
import os


def load_words(filename="words.csv"):
    words = []
    path = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["Level"] = row["Level"].upper()
            words.append(row)
    return words

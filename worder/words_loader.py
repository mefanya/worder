import csv
import os


def load_words(filename="words.csv"):
    words = []
    path = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Для единообразия можно привести level к верхнему регистру
            row["level"] = row["level"].upper()
            words.append(row)
    return words

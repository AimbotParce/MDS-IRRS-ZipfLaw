import os
import pprint
from typing import List, Tuple

import nltk


def preprocess_file(text: str):

    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)

    # Convert to lowercase
    tokens = [token.lower() for token in tokens]

    # Remove punctuation and non-alphabetic tokens
    words = [token for token in tokens if token.isalpha()]

    return words


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python preprocess.py <file_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    files_to_process: List[Tuple[str, str]] = []
    if os.path.isfile(input_path):
        files_to_process.append((input_path, output_path))
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".txt"):
                    src_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(src_file_path, input_path)
                    out_file_path = os.path.join(output_path, relative_path)
                    files_to_process.append((src_file_path, out_file_path))

    for src_file_path, out_file_path in files_to_process:
        if not os.path.isfile(src_file_path):
            raise FileNotFoundError(f"File not found: {src_file_path}")
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)

        with open(src_file_path, "r", encoding="utf-8") as file:
            text = file.read()
        words = preprocess_file(text)

        if not words:
            print(f"No words found after preprocessing in {src_file_path}.")
            continue

        with open(out_file_path, "w", encoding="utf-8") as out_file:
            words_iter = iter(words)
            while True:
                line = next(words_iter, None)
                if line is None:
                    break
                while len(line) < 1000:
                    next_word = next(words_iter, None)
                    if next_word is None:
                        break
                    line += " " + next_word
                out_file.write(line + "\n")

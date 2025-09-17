import pprint

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

    file_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    words = preprocess_file(text)

    if not words:
        raise ValueError("No words found after preprocessing.")

    with open(output_path, "w", encoding="utf-8") as out_file:
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

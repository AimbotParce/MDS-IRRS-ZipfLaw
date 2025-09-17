import nltk


def preprocess_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Tokenize the text into words
    tokens = nltk.word_tokenize(text)

    # Convert to lowercase
    tokens = [token.lower() for token in tokens]

    # Remove punctuation and non-alphabetic tokens
    words = [token for token in tokens if token.isalpha()]

    return words


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python preprocess.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    words = preprocess_file(file_path)
    print(words)

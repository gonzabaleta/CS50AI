import nltk
from nltk.tokenize import word_tokenize
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        with open(path, 'r') as file:
            content = file.read()
            files[filename] = content

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = word_tokenize(document)
    words = list()
    for token in tokens:
        if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english"):
            words.append(token)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_df = {}
    for words in documents.values():
        unique_words = set(words)
        for word in unique_words:
            if word in words_df:
                words_df[word] += 1
            else:
                words_df[word] = 1

    words_idf = {}
    num_docs = len(documents)

    for word, df in words_df.items():
        words_idf[word] = math.log(num_docs / df)

    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    files_score = {
        filename: 0
        for filename in files.keys()
    }

    for filename, words in files.items():
        for word in query:
            if word in idfs:
                tf = words.count(word)
                tf_idf = tf * idfs[word]
                files_score[filename] += tf_idf

    top_files = sorted(files_score, key=files_score.get, reverse=True)

    return top_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_mwm = {}  # Matching word measure
    sentences_qtd = {}  # query term density

    for sentence, tokens in sentences.items():
        sentences_mwm[sentence] = 0
        matching_words = 0
        for word in query:
            if word in tokens:
                sentences_mwm[sentence] += idfs[word]
                matching_words += 1

        sentences_qtd[sentence] = matching_words / len(tokens)

    top_sentences = sorted(sentences_mwm, key=lambda s: (
        sentences_mwm[s], sentences_qtd[s]), reverse=True)

    for sentence in top_sentences[:10]:
        print(sentence, sentences_mwm[sentence], sentences_qtd[sentence]),

    return top_sentences[:n]


if __name__ == "__main__":
    main()

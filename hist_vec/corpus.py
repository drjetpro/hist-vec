

import os

from itertools import islice
from gensim.models.word2vec import Word2Vec

from .utils import scan_paths
from .bpo_article import BPOArticle
from .book import Book


class Corpus:

    def __init__(self, path):
        """Wrap BPO slices corpus.

        Args:
            path (str): Corpus root.
        """
        self.path = path

    def slice_names(self):
        """Get a list of all slice names.

        Returns: list of str
        """
        return next(os.walk(self.path))[1]

    def slice_paths(self, slice_name):
        """Generate paths in a slice.

        Args:
            slice_name (str)

        Yields: str
        """
        slice_path = os.path.join(self.path, slice_name)

        yield from scan_paths(slice_path)

    def sentences(self, slice_name):
        """Get a list of all sentences for a slice.

        Args:
            slice_name (str)

        Yields: str
        """
        raise NotImplementedError

    def word2vec_model(self, slice_name):
        """Train a word2vec model on slice.

        Args:
            slice_name (str)

        Returns: Word2Vec
        """
        sentences = list(self.sentences(slice_name))

        return Word2Vec(sentences, size=100, min_count=10, workers=8)


class BPOCorpus(Corpus):

    def sentences(self, slice_name):
        """Get a list of all sentences for a slice.

        Args:
            slice_name (str)

        Yields: str
        """
        for i, path in enumerate(self.slice_paths(slice_name)):

            article = BPOArticle.from_path(path)

            yield from article.sentences()

            if i % 100 == 0:
                print(i)


class BookCorpus(Corpus):

    def sentences(self, slice_name):
        """Get a list of all sentences for a slice.

        Args:
            slice_name (str)

        Yields: str
        """
        for i, path in enumerate(self.slice_paths(slice_name)):

            book = Book.from_path(path)

            yield from book.sentences()

            if i % 100 == 0:
                print(i)

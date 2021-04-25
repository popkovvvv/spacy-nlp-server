import os

from spacy.util import registry


@registry.callbacks("customize_language_data")
def create_callback(filepath: str):
    def customize_language_data(lang_cls):
        for word in _get_stopwords(filepath):
            lang_cls.Defaults.stop_words.add(word)
        return lang_cls

    return customize_language_data


def _get_stopwords(filepath):
    if filepath is None or not os.path.exists(filepath):
        return []
    with open(filepath) as f:
        return sorted([line.rstrip("\n") for line in f])

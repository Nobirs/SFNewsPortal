from django import template

from ..scripts.words_finder import find_bad_word, is_bad_word


register = template.Library()


@register.filter()
def censor(old_text: str):
    """Replace in 'bad' words all letters expect first to '*'."""
    bad_words = []
    text = old_text
    # Read 'bad' words from file to list.
    with open('news/source/russian_bad_words.txt', 'r') as file:
        bad_words = file.readlines()
        bad_words = [word[:-1] for word in bad_words]

    # Replace 'bad' words.
    for word in bad_words:
        text = find_bad_word(word, text)
        text = find_bad_word(word.title(), text)

    return text


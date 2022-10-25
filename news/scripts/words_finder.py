def find_bad_word(word, text):
    new_text = text
    word_pos = new_text.find(word)
    while word_pos != -1:
        if is_bad_word(word, word_pos, text):
            new_text = new_text[:word_pos] + word[0] + '*'*(len(word) - 1) + new_text[word_pos + len(word):]
        word_pos = new_text.find(word, word_pos+len(word))
    return new_text


def is_bad_word(word, word_pos, text):
    if word_pos == 0 or (word_pos > 0 and not text[word_pos - 1].isalpha()):
        return True
    return False
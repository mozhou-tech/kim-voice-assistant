import jieba


def is_all_word_segment_in_text(words, text):
    """
    关键词和文本分词后，如果关键字的每个分词都在text中出现，返回True
    :return:
    """
    for key_word in words:
        word_cut = tuple(jieba.cut(key_word))
        word_cut_length = len(word_cut)
        matching_word = [x for x in word_cut if x in text]
        if word_cut_length == len(matching_word):   # 判断匹配的关键词数量
            return True
    return False

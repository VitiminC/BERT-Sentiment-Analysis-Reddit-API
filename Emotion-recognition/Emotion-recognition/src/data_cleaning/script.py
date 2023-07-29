from src.utils.cleaning_util import *

def remove_url_subreddit(comments):
    cleaned_comment_lst = []
    for comment in comments:
        comment = re.compile(WHITESPACE_PATTERN).sub(' ', comment)

        comment_removed_embedded_url = re.compile(EXTRACT_URL_CAPTION_PATTERN).sub(r'\1', comment)

        comment_removed_embedded = re.compile(EXTRACT_SUBREDDIT_CAPTION_PATTERN).sub(r'\1',
                                                                                     comment_removed_embedded_url)

        comment_removed_all_url = re.compile(URL_PATTERN).sub('', comment_removed_embedded)
        # comment_removed_all_url_subreddit = re.compile(SUBREDDIT_PATTERN).sub('', comment_removed_all_url)

        cleaned_comment_lst.append((comment, comment_removed_all_url))

    return cleaned_comment_lst


def remove_not_english(comments):
    cleaned_comment_lst = []
    for comment in comments:
        comment_removed_all_not_english_words = copy.copy(comment)
        for word in comment.split(' '):
            discard = False
            try:
                word.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                discard = True
            if discard:
                comment_removed_all_not_english_words = comment_removed_all_not_english_words.replace(word, '')
        comment_removed_all_not_english_words = re.compile(WHITESPACE_PATTERN).sub(' ', comment_removed_all_not_english_words)
        cleaned_comment_lst.append((comment, comment_removed_all_not_english_words))

    return cleaned_comment_lst


def remove_nonsense(comments):
    cleaned_comment_lst = []
    for comment in comments:
        discard = False
        words = [item.lower() for item in comment.split(' ') if len(item) > 0]
        print(comment, words)
        single_chars = sum([len(item) == 1 for item in words])
        long_words = len(words) - single_chars

        if long_words < 4 and single_chars / len(words) > 0.6:
            # word splited for emphasis
            discard = True
        elif len(set(words)) / len(words) < 0.6:
            # repeat words
            discard = True
        elif len(words) < 10 and max(map(len, words)) > 20:
            # word length way too long
            discard = True

        if discard:
            cleaned_comment_lst.append(('DELETE! ', comment))
        else:
            cleaned_comment_lst.append(('FAIL TO DELETE: ', comment))
    return cleaned_comment_lst

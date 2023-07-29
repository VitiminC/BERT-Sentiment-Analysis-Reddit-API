from src.utils.webcrawler_util import *


def get_comments_data(comments, all_comments, submission_id):
    for comment in comments:
        comment = comment['data']
        if 'author' not in comment:
            continue

        user = comment['author']
        text = comment['body']

        cleaned_text = clean_text(text)
        if len(cleaned_text) > opt.comment_min_char_len:
            all_comments[user] = cleaned_text

        if comment['replies'] != "":
            replies = comment['replies']['data']['children']
            get_comments_data(replies, all_comments, submission_id)


def get_submission_comments(submission_id, comments_url):
    all_comments = {}

    url_params = comments_url + ".json"
    data = request_reddit_data(url_params)

    data = data[1]
    comments = data['data']['children']

    get_comments_data(comments, all_comments, submission_id)

    return all_comments

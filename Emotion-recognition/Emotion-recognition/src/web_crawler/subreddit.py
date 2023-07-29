import itertools

from src.web_crawler.comments import *


def get_submissions_subreddit(url_params, all_submissions):
    data = request_reddit_data(url_params)['data']
    submissions = data['children']

    for submission in submissions:
        submission = submission['data']
        submission_id = submission['id']
        title = submission['title']
        author = submission['author']
        comment_url = submission['permalink']
        img_url = submission['url']

        comment = get_submission_comments(submission_id, comment_url)

        # at least one user
        if len(comment) > 1:
            try:
                truncated_comment = dict(itertools.islice(comment.items(), opt.comment_min_char_len))
            except:
                truncated_comment = comment

            title = extract_emojis(title)

            if img_url.endswith(IMAGE_POSTFIX):
                submission = {'submission_id': submission_id,
                              'user': author,
                              'title': title,
                              'url': img_url,
                              # 'img_embeded_text': img_ocr(img_url),
                              'comment': truncated_comment}
                all_submissions.append(submission)

    next_page = "after=" + data['after']
    return next_page

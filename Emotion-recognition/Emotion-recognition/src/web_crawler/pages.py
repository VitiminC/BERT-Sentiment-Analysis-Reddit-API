from src.web_crawler.subreddit import *


def get_subreddit_pages(pages):
    all_submissions = []
    next_page = str()
    for page in range(pages):
        print('\n------------ Now processing page {} ------------'.format(page))

        try:
            next_page = get_submissions_subreddit("r/" + opt.subreddit + "/.json?" + next_page, all_submissions)
        except:
            print('max page: {} for subreddit {}'.format(page, opt.subreddit))
            break

    with open('json_files_example/{}.json'.format(opt.subreddit), 'w', encoding='utf8') as fp:
        json.dump(all_submissions, fp, sort_keys=True, indent=4, ensure_ascii=False)
        fp.write('\n')

from src.config.config import *
from src.utils.sql_loader import DataSqlLoader


def filter_caption(caption1, caption2):
    return caption1 if len(caption1) == np.maximum(len(caption1), len(caption2)) else caption2


def convert_timstamp_to_date(timestamp):
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def unit_test(func, samples):
    result = func(samples)
    for item in result:
        print(item)


def summarize_all_submissions(path):
    sids = []
    titles = []
    images = []
    subreddits = []
    submission_created_times = []
    submission_retrieve_times = []

    sids1 = []
    titles1 = []
    images1 = []
    subreddits1 = []
    submission_created_times1 = []
    submission_retrieve_times1 = []

    comments_created_times = []
    comments_retrieve_times = []
    commenters = []
    comments = []
    status = []
    scores = []
    controversiality_scales = []

    num_null_each_submission = defaultdict(list)

    for idx, filename in enumerate(os.listdir(path)):
        # print('\n----------------------- {} ----------------------\n'.format(filename))
        file_path = os.path.join(path, filename)
        with open(file_path, 'r') as f:
            submission = json.load(f)
            title = submission['title']
            image_link = submission['image_link']
            subreddit = submission['subreddit']

            create_time = convert_timstamp_to_date(int(submission['created_utc']))
            retrieve_time = convert_timstamp_to_date(int(submission['retrieved_utc']))

            if 'virus' in subreddit:
                sids1.append(idx + 1 + 103155)
                titles1.append(title)
                images1.append(image_link)
                subreddits1.append(subreddit)
                submission_created_times1.append(create_time)
                submission_retrieve_times1.append(retrieve_time)

            num_of_comments = len(submission['comments'].items())
            if num_of_comments > 5:

                for comment_id, comment_content in submission['comments'].items():
                    try:
                        comment_body = comment_content['comment_body']
                        commenter = comment_content['author']

                        comment_created_time = convert_timstamp_to_date(int(comment_content['created_utc']))
                        comment_retrieve_time = convert_timstamp_to_date(int(comment_content['retrieve_utc']))

                        is_child = comment_content['is_child']
                        score = comment_content['score']
                        controversiality = comment_content['controversiality']

                        if commenter != '[deleted]' and comment_body != '[deleted]' and 'virus' in subreddit:
                            sids.append(idx+1+103155)
                            titles.append(title)
                            images.append(image_link)
                            subreddits.append(subreddit)
                            submission_created_times.append(create_time)
                            submission_retrieve_times.append(retrieve_time)

                            commenters.append(commenter)
                            comments.append(comment_body)
                            comments_created_times.append(comment_created_time)
                            comments_retrieve_times.append(comment_retrieve_time)
                            status.append(is_child)
                            scores.append(score)
                            controversiality_scales.append(controversiality)
                    except Exception as e:
                        num_null_each_submission[filename.split('.txt')[0]].append(commenter)

    submission_df = pd.DataFrame(
        {
            'SubmissionID': sids1,
            'Title': titles1,
            'Images': images1,
            'SubmissionCreatTime': submission_created_times1,
            'SubmissionRetrieveTime': submission_retrieve_times1,
        }
    )
    comment_df = pd.DataFrame(
        {
            'SubmissionID': sids,
            'CommentID': range(6399745, len(subreddits)+6399745),
            'Commenter': commenters,
            'Comment': comments,
            'CommentCreatTime': comments_created_times,
            'CommentRetrieveTime': comments_retrieve_times,
            'Status': status,
            'Score': scores,
            'ControversialityScale': controversiality_scales
        }
    )

    print(submission_df)
    print(comment_df)
    # submission_df.to_csv('corona_submission.csv', index=False)
    comment_df.to_csv('corona_comments.csv', index=False)


def download_reddit_images():
    ori_path = '/data/Histology/original_reddit_images_corona'
    resize_path = '/data/Histology/resized_reddit_images_corona'

    con = DataSqlLoader()

    image_links = con.sql_query(
        query='''select SubmissionID, Images from original_submission_table where SubmissionID > 103155''')  # > 103155: coronavirus
    submission_ids = list(image_links['SubmissionID'].values)
    image_links = list(image_links['Images'].values)

    print(submission_ids, image_links)

    download_dict = defaultdict(list)
    # if os.path.exists(ori_path):
    #     shutil.rmtree(ori_path)
    # os.mkdir(ori_path)
    #
    # if os.path.exists(resize_path):
    #     shutil.rmtree(resize_path)
    # os.mkdir(resize_path)

    for idx in range(len(image_links)):
        img_url = image_links[idx]
        sid = submission_ids[idx]
        save_ori_img_name = '{}/submission_{}.png'.format(ori_path, sid)
        save_resized_img_name = '{}/submission_{}.png'.format(resize_path, sid)
        try:
            ori_img = io.imread(img_url)
            resized_img = resize(ori_img, (512, 512), anti_aliasing=True)
            io.imsave(save_ori_img_name, ori_img)
            io.imsave(save_resized_img_name, resized_img)
            download_dict['valid'].append((sid, img_url))

        except Exception as e:
            print('{}: {}'.format(sid, e))
            download_dict['invalid'].append((sid, img_url))

    pprint.pprint(download_dict)
    return download_dict


def visualize_reddit_images(images_list, nrow, ncol):
    fig = plt.figure(figsize=(20., 20.))
    grid = ImageGrid(fig, 111,
                     nrows_ncols=(nrow, ncol),
                     axes_pad=0.1,
                     )
    n_rounds = len(images_list) // (nrow * ncol)
    for i in range(n_rounds):
        for ax, im in zip(grid, images_list[nrow * ncol * i:nrow * ncol * (i + 1)]):
            ax.imshow(im)
            ax.axis('off')
            # ax.set_title(sid)
        plt.show()


def extract_emojis():
    con = DataSqlLoader()
    print('connected.')
    emos = con.sql_query(query='''select Emoji_ID, Emoji from emoji_mapping_table''')
    emo_ids = list(emos['Emoji_ID'])
    emo_list = list(emos['Emoji'])
    emo_pair = dict(zip(emo_list, emo_ids))
    # print(emo_pair)
    sample_comments = con.sql_query(query='''
                                            select SubmissionID, CommentID, Comment from valid_image_raw_comments_table
                                                ''')
    # print(sample_comments)

    emo_lst = []
    for _, row in sample_comments.iterrows():
        sid, cid, comment = row[0], row[1], row[2]
        comment = str(comment)
        cl = [c.strip() for c in comment.split(' ')]

        for e in emo_list:
            for idx, c in enumerate(cl):
                if e in c:
                    print((sid, cid, emo_pair[e], e, idx, c, comment))
                    emo_lst.append((sid, cid, emo_pair[e], e, idx, c, comment))
    pprint.pprint(emo_lst)

    sid_lst = []
    cid_lst = []
    emo_ids = []
    start_ix = []
    emoji = []
    which_word = []
    raw_txt = []
    for i in emo_lst:
        sid_lst.append(i[0])
        cid_lst.append(i[1])
        emo_ids.append(i[2])
        emoji.append(i[3])
        start_ix.append(i[4])
        which_word.append(i[5])
        raw_txt.append(i[6])

    df = pd.DataFrame(
        {
            'SubmissionID': sid_lst,
            'CommentID': cid_lst,
            'EmojiID': emo_ids,
            'Emoji/Emoticon': emoji,
            'Start_idx': start_ix,
            'Word_with_emoji': which_word,
            'Comment': raw_txt
        }
    )
    print(df)
    # df.to_csv('emo_extracted.csv', index=False)


def extract_duplicates(start, end):
    duplicates = []
    duplicate_df = pd.DataFrame()
    # num of submisisons: end
    for i in range(start, end):
        print(i)
        con = DataSqlLoader()
        comments_per_sub = con.sql_query(query='''
                                                select  A.SubmissionID as SubmissionID,
                                                        A.CommentID as CommentID_A,
                                                        B.CommentID as CommentID_B,
                                                        A.Comment as Comment_A,
                                                        B.Comment as Comment_B
                                                from
                                                    stage2_corona_table as A,
                                                    stage2_corona_table as B
                                                where A.CommentID < B.CommentID
                                                and A.SubmissionID={}
                                                and B.SubmissionID={}
                                                '''.format(i, i))

        sid_lst = []
        cid1_lst = []
        cid2_lst = []
        c1_lst = []
        c2_lst = []
        lev_lst = []
        max_diff_lst = []
        for idx, row in comments_per_sub.iterrows():
            sid = row['SubmissionID']
            cid1 = row['CommentID_A']
            cid2 = row['CommentID_B']
            comment1 = row['Comment_A']
            comment2 = row['Comment_B']
            sid_lst.append(sid)
            cid1_lst.append(cid1)
            cid2_lst.append(cid2)
            c1_lst.append(comment1)
            c2_lst.append(comment2)
            lev_lst.append(Levenshtein.ratio(comment1, comment2))  # compute similarity

            current_comment_text = ''.join(char for char in comment1 if char.isalnum() or char == ' ')
            current_set = set(current_comment_text.lower().split(' '))

            check_comment_text = ''.join(char for char in comment2 if char.isalnum() or char == ' ')
            check_set = set(check_comment_text.lower().split(' '))

            same_words = current_set.intersection(check_set)
            max_diff = max(len(current_set - same_words), len(check_set - same_words))
            max_diff_lst.append(max_diff)

        df = pd.DataFrame({
            'SubmissionID': sid_lst,
            'CommentID_A': cid1_lst,
            'CommentID_B': cid2_lst,
            'Comment_A': c1_lst,
            'Comment_B': c2_lst,
            'Levenshtein': lev_lst,
            'Max_diff': max_diff_lst
        })
        print(df)
        df = df.sort_values(by=['Levenshtein'], ascending=False)
        df = df[df['Levenshtein'] > 0.8]
        if not df.empty:
            duplicate_df = pd.concat([duplicate_df, df], axis=0)
            duplicates.append((np.unique(df['SubmissionID']).tolist(),
                               np.unique(df['CommentID_A']).tolist()))
            print(duplicate_df)
            print(duplicates)
            duplicate_df.to_csv('duplicate_comments_{}-{}.csv'.format(start, end), index=False)


def rough_sentiment():
    sid_lst = []
    cid_lst = []
    c_lst = []
    polarity_lst = []
    subjectivity_lst = []
    con = DataSqlLoader()
    comments = con.sql_query(query='''select * from stage2_comments_table''')
    for idx, row in comments.iterrows():
        sid, cid, comment = row['SubmissionID'], \
                            row['CommentID'], \
                            row['Comment']

        polarity = TextBlob(comment).sentiment.polarity
        subjectivity = TextBlob(comment).sentiment.subjectivity
        print('\n---------------------------------\n')
        print(comment)
        print('\n---------------------------------\n')
        print(polarity, subjectivity)
        sid_lst.append(sid)
        cid_lst.append(cid)
        c_lst.append(comment)
        polarity_lst.append(polarity)
        subjectivity_lst.append(subjectivity)

    df = pd.DataFrame({
        'SubmissionID': sid_lst,
        'CommentID': cid_lst,
        'Comment': c_lst,
        'Polarity': polarity_lst,
        'Subjectivity': subjectivity_lst
    })

    df.to_csv('rough_sentiment.csv', index=False)

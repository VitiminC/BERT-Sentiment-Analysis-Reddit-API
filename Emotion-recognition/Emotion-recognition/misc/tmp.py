from collections import Counter, defaultdict
from pprint import pprint
import pandas as pd
from nltk import PorterStemmer, LancasterStemmer
import numpy as np
from src.senticnetapi.senticnet.senticnet import SenticNet
porter = PorterStemmer()
lancaster = LancasterStemmer()
sn = SenticNet()
# print(len(sn.data))

# comment = pd.read_csv('/data/Histology/karenyyy/Emotion-recognition/comment.csv',
#                       header=None, error_bad_lines=False )
# primary_sentiment = []
# primary_sentiment_value = []
# sentiment_label = []
# sentiment_tags = []
#
# submission_ids = []
# comment_ids = []
# texts = []
# predicted_label = []
# predicted_label_freq = []
# predicted_tag = []
# predicted_keywords = []
#
# for idx, row in comment.iterrows():
#
#     submission_id = row[0]
#     comment_id = row[1]
#     text = row[2]
#
#     submission_ids.append(submission_id)
#     comment_ids.append(comment_id)
#     texts.append(text)
#
#     primary_sentiment_each_sentence = []
#     sentiment_label_each_sentence = []
#     sentiment_tags_each_sentence = []
#
#     for word in str(text).split(' '):
#         word = word.replace('.', '').replace('!', '').lower()
#         try:
#             polarity_label = sn.polarity_label(word)
#             polarity_value = sn.polarity_value(word)
#             moodtags = sn.moodtags(word)
#             semantics = tuple(sn.semantics(word))
#
#             if np.abs(np.float(polarity_value)) > 0.8:
#                 primary_sentiment_each_sentence.append(polarity_label)
#                 sentiment_label_each_sentence.extend(moodtags)
#                 sentiment_tags_each_sentence.append({word: semantics})
#
#         except Exception as e:
#             pass
#
#     majority_label = Counter(primary_sentiment_each_sentence).most_common(1)
#     final_label_set = np.unique(primary_sentiment_each_sentence)
#
#     pass_next_step = False
#     if len(final_label_set) == 1 and majority_label[0][-1] > 0:
#         pass_next_step = True
#     elif len(final_label_set) == 2:
#         minority_label = Counter(primary_sentiment_each_sentence).most_common(2)
#         if majority_label[0][-1] - minority_label[0][-1] > 3:
#             pass_next_step = True
#
#     if not pass_next_step:
#         predicted_label.append('neutral')
#         predicted_label_freq.append(0)
#         predicted_tag.append('')
#         predicted_keywords.append({})
#     else:
#         final_uniqueset = np.unique(sentiment_label_each_sentence)
#         final_uniquetags = set(tuple(sorted(d.items())[0]) for d in sentiment_tags_each_sentence)
#         final_uniquetags = {final_uniquetag[0]: final_uniquetag[1] for final_uniquetag in final_uniquetags}
#
#         print('\n======================= Sentence {} ==========================='.format(idx))
#         print(text)
#         print('\n----------------------------------------------------------')
#         print(majority_label)
#         print(final_uniqueset)
#         pprint(final_uniquetags)
#         print('\n==========================================================')
#
#         predicted_label.append(majority_label[0][0])
#         predicted_label_freq.append(majority_label[0][-1])
#         predicted_tag.append(','.join(final_uniqueset))
#         predicted_keywords.append(final_uniquetags)
#
#
# df = pd.DataFrame(
#     {
#         'submission_id': submission_ids,
#         'comment_id': comment_ids,
#         'comment': texts,
#         'predicted_label': predicted_label,
#         'predicted_label_freq': predicted_label_freq,
#         'predicted_tag': predicted_tag,
#         'predicted_keywords': predicted_keywords
#     }
# )
#
# print(df)
#
# df.to_csv('predicted_tag.csv', index=False)


# imports
# import requests
# import io
# from PIL import Image
#
#
# def save_to_imgur(img_path_lst):
#     for p in img_path_lst:
#         img_response = requests.get(p)
#         img = Image.open(io.BytesIO(img_response.content))
#         img_width, img_height = img.size
#         min_edge = min(img.size)
#         max_edge = max(img.size)
#
#         # square_img = img.crop(
#         #     (
#         #         (img_width - crop) // 2,
#         #         (img_height - crop) // 2,
#         #         (img_width + crop) // 2,
#         #         (img_height + crop) // 2,
#         #     )
#         # )  # Square Image is of type Pil Image
#         if max_edge > 4000 or min_edge > 3000:
#             new_size = (round(img.size[0]*0.5), round(img.size[1]*0.5))
#             square_img = img.resize(new_size)
#         else:
#             square_img = img
#         imgByteArr = io.BytesIO()
#         square_img.save(imgByteArr, format="PNG")
#         imgByteArr = imgByteArr.getvalue()
#
#         url = "https://api.imgur.com/3/image"
#
#
#         payload = {"image": imgByteArr}
#         headers = {"Authorization": "Client-ID a77915fbab1134e"}
#         response = requests.request("POST", url, headers=headers, data=payload)
#
#         print(p, response.text.encode("utf8"))
#
#
#
# d = {}
# for line in open('/Users/karenyyy/Workspace/Emotion-recognition/log', 'r'):
#     imgur_url = line.split(' ')[1].replace('"', '').replace('\n', '')
#     d[line.split(' ')[0]] = "https://i.imgur.com/xxx.jpg".replace('xxx', imgur_url)
#
#
# reddit = pd.read_csv('/Users/karenyyy/Downloads/reddit_example.csv')
#

#############################################################################################


# imgur_lst = []
# for i in list(reddit['Images']):
#     if 'imgur' not in i and i not in d.keys():
#         imgur_lst.append(i)
#
# save_to_imgur(img_path_lst=np.unique(imgur_lst))
#


#############################################################################################

df = pd.read_csv('/Users/karenyyy/Downloads/mturk_samples_100.csv')
emoji = pd.read_csv('/Users/karenyyy/Downloads/emoji_mapping_table.csv')
emoji_lst = list(emoji['Emoji'])
visited_sid = []

sid = []
img_urls = []
titles = []
comments = defaultdict(list)

for idx, row in df.iterrows():
    if row['SubmissionID'] not in visited_sid:
        visited_sid.append(row['SubmissionID'])
        sid.append(row['SubmissionID'])
        current_df = df[df['SubmissionID'] == row['SubmissionID']]
        current_df = current_df.reset_index(drop=True)
        if len(current_df.index) == 20:
            for current_idx, current_row in current_df.iterrows():
                if current_row['SubmissionTitle'] not in titles:
                    titles.append(current_row['SubmissionTitle'])
                if current_row['Images'] not in img_urls:
                    img_urls.append(current_row['Images'])
                comments[f'comment{current_idx+1}'].append(''.join(c for c in current_row['Comment'] if str(c) not in emoji_lst))


print(len(img_urls), len(sid), len(titles), [len(v) for k, v in comments.items()])

for idx, title in enumerate(titles):
    titles[idx] = ''.join(c for c in title if str(c) not in emoji_lst)

d2 = pd.DataFrame(
    {
        # 'SubmissionID': sid,
        'image_url': img_urls,
        'title': titles,
        'comment1': comments['comment1'],
        'comment2': comments['comment2'],
        'comment3': comments['comment3'],
        'comment4': comments['comment4'],
        'comment5': comments['comment5'],
        'comment6': comments['comment6'],
        'comment7': comments['comment7'],
        'comment8': comments['comment8'],
        'comment9': comments['comment9'],
        'comment10': comments['comment10'],
        'comment11': comments['comment11'],
        'comment12': comments['comment12'],
        'comment13': comments['comment13'],
        'comment14': comments['comment14'],
        'comment15': comments['comment15'],
        'comment16': comments['comment16'],
        'comment17': comments['comment17'],
        'comment18': comments['comment18'],
        'comment19': comments['comment19'],
        'comment20': comments['comment20']
    }
)

# mask = d2[['image_url']].apply(
#     lambda x: x.str.contains(
#         'i.imgur',
#         regex=True
#     )
# ).any(axis=1)
# d3 = d2[mask]
# print(len(d3.index))


for i in range(10):
    print(len(d2[10*i:10*(i+1)].index))
    d2[10*i:10*(i+1)].to_csv(f'/Users/karenyyy/Workspace/Emotion-recognition/mturk_data/{i+1}.csv', index=None)
d2.to_csv(f'/Users/karenyyy/Workspace/Emotion-recognition/mturk_data/100.csv', index=None)


# df = pd.concat([pd.read_csv(f'/Users/karenyyy/Downloads/mturk_data_tmp.csv'),
#                 pd.read_csv(f'/Users/karenyyy/Downloads/mturk_data.csv')], 0)
# df.to_csv('/Users/karenyyy/Downloads/mturk_data.csv', index=None)


# df_tmp = pd.read_csv(f'/Users/karenyyy/Downloads/mturk_data_tmp.csv')
# df_tmp = df_tmp.iloc[:, 2:]
# print(df_tmp)
# df_tmp.to_csv('/Users/karenyyy/Downloads/mturk_data_tmp2.csv', index=None)


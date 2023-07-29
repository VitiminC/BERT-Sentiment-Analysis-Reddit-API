import argparse
import urllib
import clip
import enchant
from transformers import BertTokenizer

from Transformer_Explainability.BERT_explainability.modules.BERT.ExplanationGenerator import Generator
from src.data_cleaning.script import *
from src.config.config import *
from src.emotion.go_emotion import *
from src.emotion.model import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser("data cleaning task")
    parser.add_argument("--task", default=0, type=int, help="which data cleaning task to implement")
    args = parser.parse_args()

    task = args.task

    if task == 0:
        out = remove_url_subreddit(
            ['[Bullshit](https://www.reddit.com/r/reddit.com/comments/ie1ls/i_took_a_photo_of_my_housemates_cat_leon_the/).',
             'It’s [Archie McPhee](https://mcphee.com/)',
             'Here is everything you never wanted to know about this: (scroll down for the narwhal)  [https://mcphee.com/blogs/news/avenging-unicorn-and-narwhal](https://mcphee.com/blogs/news/avenging-unicorn-and-narwhal)',
             'There is also an Avenging Unicorn set - it comes with a mime you can impale...  https://m.media-amazon.com/images/I/41Gw5sP8+hL._AC_UL320_.jpg'
            ]
        )
        for i in out:
            print(i)

    elif task == 1:

        out = remove_not_english(
            ['¯\_(ツ)_/¯  (Since I have this keyboard "layout" on my phone)',
             '°L° cout "hahaha orange man indeed bad";',
             '§çhřöəđįñğëŕ',
             '良いお年を',
             '새해 복 많이 받으세요 -o-'
             ]
        )
        for i in out:
            print(i)

    elif task == 2:

        out = remove_nonsense(
            [
                'YYYYYYYEEEEEEAAAAAAHHHH',
                'WTFFFFFF WTF WTF WTF',
                'D A M N',
            ]
        )

        for i in out:
            print(i)

    elif task == 3:
        extract_emojis()

    elif task == 4:
        extract_duplicates(start=1, end=10000)

    elif task == 5:
        device = torch.device("cuda:4" if torch.cuda.is_available() else "cpu")

        wt = WordNetTagger()
        bert_model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-original").to(device)

        bert_model.eval()
        tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
        explanations = Generator(bert_model)

        clip_model, preprocess = clip.load("ViT-B/32", device=device, jit=False)

        for i in range(40, 60):
            df = pd.read_csv(f'mturk_data/21-07-26/mturk_{i}c.csv')
            df_new = pd.DataFrame([])

            for idx, row in df.iterrows():
                urls = []
                try:
                    urllib.request.urlretrieve(row['image_url'], 'tmp.png')
                except Exception as e:
                    print(e, row['image_url'])
                    continue
                image = preprocess(Image.open("tmp.png")).unsqueeze(0).to(device)

                cap_and_comments = [row['title']]
                cap_and_comments_to_save = [row['title']]

                for comment_idx in range(1, 21):
                    urls.append(row['image_url'])

                    cap_and_comments_to_save.append(row[f'comment{comment_idx}'])

                    if isinstance(row[f'comment{comment_idx}'], np.float):
                        row[f'comment{comment_idx}'] = str(row[f'comment{comment_idx}'])
                    if len(row[f'comment{comment_idx}']) < 200:
                        cap_and_comments.append(row[f'comment{comment_idx}'])
                    else:
                        cap_and_comments.append(row[f'comment{comment_idx}'][:200])



                text = clip.tokenize(cap_and_comments).to(device)

                with torch.no_grad():
                    image_features = clip_model.encode_image(image)

                    text_features = clip_model.encode_text(text)

                    logits_per_image, logits_per_text = clip_model(image, text)
                    probs = logits_per_image.softmax(dim=-1).cpu().numpy()
                # print(probs)
                sorted_idx = [int(i[0]) for i in sorted(enumerate(probs[0]), key=lambda x:x[1], reverse=True)]

                comment_to_save = []
                emotional_tag_to_save = []
                significant_words_to_save = []

                # print('(cap_and_comments_to_save): ', len(cap_and_comments_to_save))
                for s in np.array(cap_and_comments_to_save)[sorted_idx]:
                    if s == row['title']:
                        comment_to_save.append(f'(title) {s}')
                    else:
                        comment_to_save.append(f'(comment) {s}')

                    inputs = tokenizer(s, return_tensors="pt")
                    inputs = inputs.to(device)
                    outputs = bert_model(**inputs)
                    scores = 1 / (1 + torch.exp(-outputs[0]))  # Sigmoid
                    threshold = .5

                    labels = []
                    for idx, score in enumerate(scores[0]):
                        if score > threshold:
                            labels.append(bert_model.config.id2label[idx])

                    encoding = tokenizer(s, return_tensors='pt')

                    input_ids = encoding['input_ids'].to(device)
                    attention_mask = encoding['attention_mask'].to(device)
                    expl = explanations.generate_LRP(input_ids=input_ids, attention_mask=attention_mask, start_layer=0)[0]
                    expl = (expl - expl.min()) / (expl.max() - expl.min())
                    output = torch.nn.functional.softmax(bert_model(input_ids=input_ids, attention_mask=attention_mask)[0],
                                                         dim=-1)
                    tokens = tokenizer.convert_ids_to_tokens(input_ids.flatten())
                    res = [(tokens[i], expl[i].item()) for i in range(len(tokens))]
                    sorted_res = [i for i in sorted(res, key=lambda x: x[1], reverse=True)][:5]
                    valid_word_res = []
                    for k, v in sorted_res:
                        d = enchant.Dict("en_US")
                        if d.check(k) and len(k) > 1 and v > 0.1:
                            try:
                                pos = wt.tag([k])
                            except:
                                pos = k
                            valid_word_res.append((pos, v))
                        else:
                            pass
                    # print(valid_word_res)

                    significant_words_to_save.append(valid_word_res)
                    emotional_tag_to_save.append(', '.join(labels))

                # print(len(comment_to_save))
                # print(comment_to_save)
                df_new[f"{row['image_url']} title & comment"] = comment_to_save

                df_new[f"{row['image_url']} significant words"] = [0] * len(df_new)
                df_new[f"{row['image_url']} significant words"] = df_new[f"{row['image_url']} significant words"].astype('object')
                df_new[f"{row['image_url']} significant words"] = significant_words_to_save

                df_new[f"{row['image_url']} relevance score"] = probs[0][sorted_idx]
                df_new[f"{row['image_url']} emotional tag"] = emotional_tag_to_save

                # pprint(tuple(zip(np.array(cap_and_comments)[sorted_idx], probs[0][sorted_idx])))
                # pprint(zip(urls[sorted_idx], cap_and_comments[sorted_idx]))  # prints: [[0.9927937  0.00421068 0.00299572]]
            with pd.option_context('display.max_rows', None,
                                   'display.max_columns', None,
                                   'display.precision', 3,
                                   ):
                print(df_new)
            # df_new.to_csv(f'/data/karenyyy/GroupViT/mturk_data/22-10-24/example_{i}c.csv', index=None)

    elif task == 6:
        con = DataSqlLoader()
        print('connected.')

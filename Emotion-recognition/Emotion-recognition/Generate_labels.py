from captum.attr import visualization
import torch
from transformers import BertTokenizer
from Transformer_Explainability.BERT_explainability.modules.BERT.ExplanationGenerator import Generator
from Transformer_Explainability.BERT_explainability.modules.BERT.BertForSequenceClassification import \
    BertForSequenceClassification
from transformers import AutoTokenizer

import urllib
import clip
from src.data_cleaning.script import *
from src.config.config import *
from src.emotion.go_emotion import *
from src.emotion.model import *
import warnings

warnings.filterwarnings('ignore')
import traceback

#############################
subreddit = "for_labeling"
from pathlib import Path
import pandas as pd

DATA = f'BERT-Sentiment-Analysis-Reddit-API/DataCleaning/sqldf/{subreddit}.csv'

#############################
emoji = pd.read_csv(
    'BERT-Sentiment-Analysis-Reddit-API/Emotion-recognition/Emotion-recognition/emoji_mapping_table.csv')
emoji_lst = list(emoji['Emoji'])
try:
    mturk_df = pd.read_csv(DATA, sep=",", encoding='cp1252', on_bad_lines='skip')
except:
    mturk_df = pd.read_csv(DATA, sep=",", encoding='utf-8', on_bad_lines='skip')

device = torch.device("cuda:0" if torch.cuda.is_available() else print('hello'))
wt = WordNetTagger()
bert_model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-original").to(device)

bert_model.eval()
tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
explanations = Generator(bert_model)

clip_model, preprocess = clip.load("ViT-B/32", device=device, jit=False)
model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-original").to("cuda")

##################################
save_to_csv = []
save_to_json = []
start = 300301
end = 300330
count = start - 1
for index, m_row in mturk_df.loc[(mturk_df['SubmissionID'] >= start) & (mturk_df['SubmissionID'] <= end)].iterrows():
    commentid = m_row['CommentID']
    sid = m_row['SubmissionID']
    try:
        if sid != count:
            urllib.request.urlretrieve(m_row['Images'], 'tmp.png')
            image = preprocess(Image.open("tmp.png")).unsqueeze(0).to(device)
            count = m_row['SubmissionID']
            print(f'{count}/{end}')
        else:
            image = image
    except:
        continue

    print(f'{count}/{end}:Comment{commentid}')

    if start <= sid <= end:
        cap_and_comments = [''.join(t for t in m_row['SubmissionTitle'] if str(t) not in emoji_lst)]
        comment = m_row['Comment']

        text = clip.tokenize(cap_and_comments).to(device)
        with torch.no_grad():
            image_features = clip_model.encode_image(image)
            text_features = clip_model.encode_text(text)
            logits_per_image, logits_per_text = clip_model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        sorted_idx = [int(i[0]) for i in sorted(enumerate(probs[0]), key=lambda x: x[1], reverse=True)]
        post_labels = []

        comment_clean = comment.replace("'", "")
        if len(comment_clean) >= 512:
            comment_clean = comment_clean[:511]

        inputs = tokenizer(comment_clean, return_tensors="pt")
        inputs = inputs.to(device)
        outputs = bert_model(**inputs)
        scores = 1 / (1 + torch.exp(-outputs[0]))  # Sigmoid
        threshold = .3
        comment_labels = []
        for idx, score in enumerate(scores[0]):
            if score > threshold:
                label = bert_model.config.id2label[idx]
                comment_labels.append((label, float(score)))
        if len(comment_labels) == 0:
            idx, score = max(enumerate(scores[0]))
            label = bert_model.config.id2label[idx]
            comment_labels.append((label, float(score)))
        post_labels.append(comment_labels)
    insert_row = [count, comment, post_labels[0]]
    save_to_csv.append(insert_row)

    # attention mapper
    text_batch = comment_clean
    encoding = tokenizer(text_batch, return_tensors='pt')
    input_ids = encoding['input_ids'].to("cuda")
    attention_mask = encoding['attention_mask'].to("cuda")

    # true class is positive - 1
    true_class = 1

    # generate an explanation for the input
    expl = explanations.generate_LRP(input_ids=input_ids, attention_mask=attention_mask, start_layer=0)[0]
    # normalize scores
    expl = (expl - expl.min()) / (expl.max() - expl.min())

    # get the model classification
    output = torch.nn.functional.softmax(model(input_ids=input_ids, attention_mask=attention_mask)[0], dim=-1)
    classification = output.argmax(dim=-1).item()
    # get class name
    class_name = classifications[classification]
    # if the classification is negative, higher explanation scores are more negative
    # flip for visualization
    if class_name == "NEGATIVE":
        expl *= (-1)

    tokens = tokenizer.convert_ids_to_tokens(input_ids.flatten())
    save_tokens = [(tokens[i], expl[i].item()) for i in range(len(tokens))]
    save_to_json.append(
        {'submission_id': count,
         'comment_id': commentid,
         'comment': comment,
         'emotion': post_labels[0],
         'attention': save_tokens})

with open(f'json_data2/emo_distribution_start{start}_end{count}.json', 'w') as f:
    json.dump(save_to_json, f)
    print('saved to json!')

df = pd.DataFrame(save_to_csv)
df.to_csv(
    f'BERT-Sentiment-Analysis-Reddit-API/DataCleaning/sqldf/tags2/start_{start}_end_{count}.csv',
    index=False, encoding='utf8')
save_to_csv = None
save_to_json = None
df = None

print('done')
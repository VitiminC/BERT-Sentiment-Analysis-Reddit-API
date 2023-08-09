from captum.attr import visualization
import torch
from transformers import BertTokenizer
from Transformer_Explainability.BERT_explainability.modules.BERT.ExplanationGenerator import Generator
from Transformer_Explainability.BERT_explainability.modules.BERT.BertForSequenceClassification import \
    BertForSequenceClassification
from transformers import AutoTokenizer
import gc
import urllib
import clip
from src.data_cleaning.script import *
from src.config.config import *
from src.emotion.go_emotion import *
from src.emotion.model import *
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
import weakref
import traceback

from memory_profiler import profile

#############################
class MyClass:

    def __init__(self):
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else print('hello'))
        self.bert_model = BertForMultiLabelClassification.from_pretrained("monologg/bert-base-cased-goemotions-original").to(self.device)
        self.bert_model.eval()
        self.tokenizer = BertTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
        self.explanations = Generator(self.bert_model)

    def get_insert_data(self, m_row):
        commentid = m_row['CommentID']
        sid = m_row['SubmissionID']

        count = sid
        print(f'{count}/{end}:Comment{commentid}')

        if start <= sid <= end:
            comment = m_row['Comment']
            post_labels = []

            comment_clean = comment.replace("'", "")
            if len(comment_clean) >= 512:
                comment_clean = comment_clean[:511]

            inputs = self.tokenizer(comment_clean, return_tensors="pt")
            inputs = inputs.to(self.device)
            outputs = self.bert_model(**inputs)
            scores = 1 / (1 + torch.exp(-outputs[0]))  # Sigmoid
            threshold = .3
            comment_labels = []
            for idx, score in enumerate(scores[0]):
                if score > threshold:
                    label = self.bert_model.config.id2label[idx]
                    comment_labels.append((label, float(score)))
            if len(comment_labels) == 0:
                idx, score = max(enumerate(scores[0]))
                label = self.bert_model.config.id2label[idx]
                comment_labels.append((label, float(score)))
            post_labels.append(comment_labels)
        insert_row = [count, commentid, comment, post_labels[0]]

        # attention mapper
        text_batch = comment_clean
        encoding = self.tokenizer(text_batch, return_tensors='pt')
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        expl = self.explanations.generate_LRP(input_ids=input_ids, attention_mask=attention_mask, start_layer=0)[0]
        expl = (expl - expl.min()) / (expl.max() - expl.min())
        output = torch.nn.functional.softmax(self.bert_model(input_ids=input_ids, attention_mask=attention_mask)[0], dim=-1)
        classification = output.argmax(dim=-1).item()
        class_name = classifications[classification]
        if class_name == "NEGATIVE":
            expl *= (-1)
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.flatten())
        save_tokens = [(tokens[i], expl[i].item()) for i in range(len(tokens))]
        insert_json = {'submission_id': count,
                       'comment_id': commentid,
                       'comment': comment,
                       'emotion': post_labels[0],
                       'attention': save_tokens}

        yield [insert_row, insert_json]


start = 325618
iterations = 1
increment = 60
obj = MyClass()
data = f'C:/Users/Charlie/Desktop/Database/BERT-Sentiment-Analysis-Reddit-API/DataCleaning/sqldf/for_labeling.csv'
mturk_df = pd.read_csv(data, sep=",", encoding='utf-8', on_bad_lines='skip')

while iterations != 0:
    save_to_csv = []
    save_to_json = []
    end = start + increment

    for index, m_row in mturk_df.loc[(mturk_df['SubmissionID'] >= start) & (mturk_df['SubmissionID'] <= end)].iterrows():
        data = list(obj.get_insert_data(m_row))
        save_to_csv.append(data[0][0])
        save_to_json.append(data[0][1])

    with open(f'json_data2/emo_distribution_start{start}_end{end}.json', 'w') as f:
        json.dump(save_to_json, f)
        print('saved to json!')

    df = pd.DataFrame(save_to_csv)
    df.to_csv(
        f'C:/Users/Charlie/Desktop/Database/BERT-Sentiment-Analysis-Reddit-API/DataCleaning/sqldf/tags2/start_{start}_end_{end}.csv', index=False, encoding='utf8')
    print('done')

    start = end
    iterations -= 1
    #torch.cuda.empty_cache()
    #gc.collect()
    print(start+1)

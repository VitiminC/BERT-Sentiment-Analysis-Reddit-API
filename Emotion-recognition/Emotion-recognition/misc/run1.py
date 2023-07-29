import re
from pprint import pprint

import pandas as pd

from src.data_cleaning.senticsentence import SenticPhrase


def clean_text(df, text_field, new_text_field_name):
    df[new_text_field_name] = df[text_field].str.lower()
    print(df[new_text_field_name])
    df[new_text_field_name] = df[new_text_field_name].apply(
        lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem))
    print(df[new_text_field_name])
    df[new_text_field_name] = df[new_text_field_name].apply(lambda elem: re.sub(r"\d+", "", elem))
    print(df[new_text_field_name])

    for idx, row in df.iterrows():
        text = row[new_text_field_name]
        print(text)
        sp = SenticPhrase(text)
        info = sp.info(text)

        print(info['polarity'])
        print(info['moodtags'])
        print(info['sentiment'])
        pprint(info['semantics'])

    return df


df = pd.read_csv('predicted_tag.csv')
clean_text(df.iloc[:50, :], 'comment', 'cleaned_comment')


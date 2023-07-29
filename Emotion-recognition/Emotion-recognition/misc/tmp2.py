import pandas as pd
from src.utils.sql_loader import DataSqlLoader, defaultdict


for i in range(16, 60):
    df = pd.read_csv('valid_image_submission_table.csv')

    animal = df[df['Category']=='A']
    people = df[df['Category'] == 'P']
    animal_and_people = df[df['Category']=='PA']
    food = df[df['Category']=='F']
    landscape = df[df['Category']=='L']
    others = df[df['Category']=='O']


    animal_2 = animal.sample(n = 2)
    people_2 = people.sample(n=2)
    animal_and_people_2 = animal_and_people.sample(n = 2)
    food_2 = food.sample(n = 2)
    landscape_2 = landscape.sample(n = 2)
    others_2 = others.sample(n = 2)

    new_df = pd.concat([animal_2, people_2, animal_and_people_2, food_2, landscape_2, others_2])
    new_df = new_df.drop('Category', axis=1).drop('Accept', axis=1)
    new_df.to_csv(f'mturk_data/21-07-26/mturk_{i+1}.csv', index=None)
    new_df2 = df[~df['SubmissionID'].isin(list(new_df['SubmissionID']))]
    new_df2.to_csv('valid_image_submission_table.csv', index=None)


con = DataSqlLoader()
emoji = pd.read_csv('emoji_mapping_table.csv')
emoji_lst = list(emoji['Emoji'])

for file_num in range(17, 60):
    mturk_df = pd.read_csv(f'mturk_data/21-07-26/mturk_{file_num}.csv')
    image_url_list = []
    title_list = []
    comments_dict = defaultdict(list)

    for index, m_row in mturk_df.iterrows():
        image_url_list.append(m_row['Images'])
        # title_list.append(m_row['SubmissionTitle'])
        title_list.append(''.join(t for t in m_row['SubmissionTitle'] if str(t) not in emoji_lst))
        sid = m_row['SubmissionID']
        comments = con.sql_query(query='''select * from valid_image_cleaned_comments_table where SubmissionID={}'''.format(sid))
        for idx, row in comments.iterrows():
            if idx + 1 <= 20:
                comments_dict[f'comment{idx+1}'].append(''.join(c for c in row['Comment'] if str(c) not in emoji_lst))

    d2 = pd.DataFrame(
        {
            # 'SubmissionID': sid,
            'image_url': image_url_list,
            'title': title_list,
            'comment1': comments_dict['comment1'],
            'comment2': comments_dict['comment2'],
            'comment3': comments_dict['comment3'],
            'comment4': comments_dict['comment4'],
            'comment5': comments_dict['comment5'],
            'comment6': comments_dict['comment6'],
            'comment7': comments_dict['comment7'],
            'comment8': comments_dict['comment8'],
            'comment9': comments_dict['comment9'],
            'comment10': comments_dict['comment10'],
            'comment11': comments_dict['comment11'],
            'comment12': comments_dict['comment12'],
            'comment13': comments_dict['comment13'],
            'comment14': comments_dict['comment14'],
            'comment15': comments_dict['comment15'],
            'comment16': comments_dict['comment16'],
            'comment17': comments_dict['comment17'],
            'comment18': comments_dict['comment18'],
            'comment19': comments_dict['comment19'],
            'comment20': comments_dict['comment20']
        }
    )
    print(file_num, d2)
    d2.to_csv(f'mturk_data/21-07-26/mturk_{file_num}c.csv', index=None)

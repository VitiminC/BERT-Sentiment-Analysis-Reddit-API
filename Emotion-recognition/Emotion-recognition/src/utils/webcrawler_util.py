from src.config import *


def request_reddit_data(url):
    response = requests.get(BASE_URL + url, headers={'User-agent': opt.user_agent})
    data = response.json()
    return data


def extract_emojis(text):
    emoji, emoticons = emot.emoji(text), emot.emoticons(text)
    emo_lst, emoti_lst = [], []

    if 'value' in emoji and len(emoji['value']) > 0:
        for idx in range(len(emoji['value'])):
            loc = emoji['location']
            emo_lst.append(text[loc[idx][0]])
            text = text.replace(text[loc[idx][0]], ' ')

    if 'value' in emoticons and len(emoticons['value']) > 0:
        for idx in range(len(emoticons['value'])):
            loc = emoticons['location']
            emoti_lst.append(text[loc[idx][0]: loc[idx][1]])
            text = text.replace(text[loc[idx][0]: loc[idx][1]], ' '*(loc[idx][1] - loc[idx][0]))

    text = '[{}] '.format(' '.join(emo_lst) + ' ' + ' '.join(emoti_lst)) + text
    return text


def clean_text(text):
    text = extract_emojis(text)

    text = text.strip() \
        .replace('\n', '') \
        .replace('\"', "'") \
        .replace('&amp', '') \
        .replace('&gt;', '') \
        .replace('&lt;', '') \
        .replace('*', '')

    _RE_COMBINE_WHITESPACE = re.compile(r"\s+")
    text = _RE_COMBINE_WHITESPACE.sub(" ", text)
    _RE_COMBINE_DOTS = re.compile(r"\.+")
    text = _RE_COMBINE_DOTS.sub(".", text)

    HTTP_URL = re.compile(r'\(?https?:\/\/.*[\r\n]*')
    WWW_URL = re.compile(r'\(?www?:\/\/.*[\r\n]*')
    text = HTTP_URL.sub("", text)
    text = WWW_URL.sub("", text)
    return text


def img_ocr(img_url):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))
    embedded_text = pytesseract.image_to_string(img)
    spell = SpellChecker()
    misspelled = spell.unknown(embedded_text.split(' '))

    for word in misspelled:
        corrected_word = spell.correction(word)
        embedded_text = embedded_text.replace(word, corrected_word)

    embedded_text = clean_text(embedded_text)
    return embedded_text


def get_top_subreddits():
    global TOP_SUBREDDIT_URL
    url = TOP_SUBREDDIT_URL
    subreddit_lst = []
    for offset in range(0, 100*opt.max_subreddit_pages, 100):
        req = requests.get(url, headers={'User-agent': opt.user_agent})
        soup = BeautifulSoup(req.content, 'html.parser')
        for tr in soup.find_all('tr')[2:]:
            tds = tr.find_all('td')
            subreddit = tds[1].text.split('/r/')[-1]
            subreddit_lst.append(subreddit)
        postfix = '/offset/{}'.format(offset)
        url = TOP_SUBREDDIT_URL + postfix
    return subreddit_lst


def collect_emoticonsfrom_wiki(wiki_url='https://en.wikipedia.org/wiki/List_of_emoticons'):
    uClient = uReq(wiki_url)
    page_html = uClient.read()
    uClient.close()
    emoticon_dict = {}
    page_soup = soup(page_html,"html.parser")
    table = page_soup.findAll("table", {"class": "wikitable"})
    for i in range(len(table)-5):
        emo_table = table[i]
        table_row = emo_table.findAll("tr")
        for row in table_row[1:len(table_row)-1]:
            row_info = row.findAll("td")
            if len(row_info) > 2:
                emoticons = [emo_item.text for emo_item in row_info[:-2]]
            elif len(row_info) == 2:
                emoticons = [emo_item.text for emo_item in row_info[:-1]]
            else:
                continue
            words_for_emo = re.compile(r'\[\d*\]').sub('', row_info[-1].text)
            words_for_emo = words_for_emo.replace('\n', '').replace("\'", "'")
            emoticons = [emoticon.replace('\u3000', ' ').replace('\n', '') for emoticon in emoticons]
            emoticon_dict[words_for_emo] = emoticons

    pprint.pprint(emoticon_dict)
    return emoticon_dict
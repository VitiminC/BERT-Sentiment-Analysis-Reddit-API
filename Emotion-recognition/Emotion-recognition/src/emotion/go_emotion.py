from nltk.corpus import wordnet
from nltk.probability import FreqDist
from nltk.tag import SequentialBackoffTagger

classifications = ['admiration',
                   'amusement',
                   'anger',
                   'annoyance',
                   'approval',
                   'caring',
                   'confusion',
                   'curiosity',
                   'desire',
                   'disappointment',
                   'disapproval',
                   'disgust',
                   'embarrassment',
                   'excitement',
                   'fear',
                   'gratitude',
                   'grief',
                   'joy',
                   'love',
                   'nervousness',
                   'optimism',
                   'pride',
                   'realization',
                   'relief',
                   'remorse',
                   'sadness',
                   'surprise',
                   'neutral'
                   ]


class WordNetTagger(SequentialBackoffTagger):
    def __init__(self, *args, **kwargs):
        SequentialBackoffTagger.__init__(self, *args, **kwargs)
        self.wordnet_tag_map = {
            'n': 'NN',
            's': 'JJ',
            'a': 'JJ',
            'r': 'RB',
            'v': 'VB'
        }

    def choose_tag(self, tokens, index, history):
        word = tokens[index]
        fd = FreqDist()

        for synset in wordnet.synsets(word):
            fd[synset.pos()] += 1

        return self.wordnet_tag_map.get(fd.max())



# Not using this code in project. 
import nltk
from nltk.tokenize import sent_tokenize
def textSummarize(txt):
    text = nltk.word_tokenize(txt)
    pos_tags = nltk.pos_tag(text)

    verbs = []
    for tags in pos_tags:
        if tags[1] == "VB":
            verbs.append(tags[0])

    sentences = sent_tokenize(txt)

    action_sentences = []
    for sent in sentences:
        for verb in verbs:
            if verb in sent:
                action_sentences.append(sent)
                break

    return " ".join(action_sentences)


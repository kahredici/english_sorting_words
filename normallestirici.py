
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from operator import itemgetter

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ""

def ayir(text, karistir=True):
	text = nltk.word_tokenize(text)
	tagged_text = nltk.pos_tag(text)

	ret = []
	for i in tagged_text:
		tur = get_wordnet_pos(i[1])
		if tur != "":
			ret.append(lemmatizer.lemmatize(i[0], tur).lower())
		else:
			ret.append(i[0].lower())
	if karistir:
		return list(set(ret))
	else:
		return ret


def buyuk_listeyi_sirala(text):
	t = text.split("\n")

	ret = []
	for i in t:
		i2 = i.split("\t")
		duzeltilmis_kelime = ayir(i2[0],karistir=False)[0]

		#arama
		daha_once_eklenmemis = True
		for ara in ret:
			if ara[0] == duzeltilmis_kelime:

				ara[1] += int(i2[1])
				daha_once_eklenmemis = False

		if daha_once_eklenmemis:
			ret.append([duzeltilmis_kelime,int(i2[1])])



	ret = sorted(ret, key=itemgetter(1))
	ret.reverse()

	return ret


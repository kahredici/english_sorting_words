from flask import Flask, request
from pymongo import MongoClient
import json
import normallestirici

app = Flask(__name__)
app.debug = True


client = MongoClient()
db = client.words
#client.drop_database('words')

isRunedBefore = db.words.find_one({"isRunedBefore":1})
if isRunedBefore == None:

	print("liste siralaniyor")
	fle = open("words.txt").read()
	word_list_family = normallestirici.buyuk_listeyi_sirala(fle)

	print("Words are inserting to mongodb...\n")
	read = open("words.txt").readlines()

	for counter, i in enumerate(word_list_family,1):
		place = counter
		word = i[0]

		db.words.insert_one(
		    {
		    "place": place,
		    "word": word
		    })

	db.words.insert_one({"isRunedBefore":1})

print("Api running...")



@app.route("/",methods=['GET'])
def index():
	k = request.args
	searching_word = normallestirici.ayir(k['word'])[0]

	word = db.words.find_one({"word":searching_word})
	del word['_id']
	word['percentage'] = str( int( (int(word['place'])/41284)*100))+"%"
	return json.dumps(word)

@app.route("/c",methods=['GET'])
def cumle():
	k = request.args
	searching_sentence = normallestirici.ayir(k['sentence'])

	ret = []
	for searching_word in searching_sentence:
		word = db.words.find_one({"word":searching_word})
		if word != None:
			del word['_id']
			word['percentage'] = str( int( (int(word['place'])/41284)*100))+"%"
			ret.append(word)

	newlist = sorted(ret, key=lambda k: k['place']) 

	# k = ""
	# for i in newlist:
	# 	if i['place'] > 1000:
	# 		k += "<ul>"
	# 		k += "<li>" + str(i['place']) + "</li>"
	# 		k += "<li>" + i['word'] + "</li>"
	# 		k += "</ul>"
	# k += str(len(newlist))
	# return k
	return json.dumps(newlist)



app.run()
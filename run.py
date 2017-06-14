from flask import Flask, request, url_for
from pymongo import MongoClient
import json
import normallestirici
import requests


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
def cumle_api():
	k = request.args['sentence']
	print(k)
	print()
	print()
	print()
	noktalama_isareleri = "abcdefgğhıijklmnoöpqrsştuüvwxyz"
	noktalama_isareleri += noktalama_isareleri.upper()
	k = [x if x in noktalama_isareleri else " " for x in k ]
	k = ''.join(k)
	print(k)

	searching_sentence = normallestirici.ayir(k)

	ret = []
	for searching_word in searching_sentence:
		word = db.words.find_one({"word":searching_word})
		if word != None:
			del word['_id']
			word['percentage'] = str( int( (int(word['place'])/41284)*100))+"%"
			ret.append(word)

	newlist = sorted(ret, key=lambda k: k['place']) 


	return json.dumps(newlist)

@app.route("/cumle",methods=["GET","POST"])
def cumle_html():
	if request.method == 'POST':
		k= request.form['cumle']

		noktalama_isareleri = "abcdefgğhıijklmnoöpqrsştuüvwxyz"
		noktalama_isareleri += noktalama_isareleri.upper()
		k = [x if x in noktalama_isareleri else " " for x in k ]
		k = ''.join(k)

		foo = "http://127.0.0.1:5000/c"+"?sentence="+k
		newlist = json.loads(requests.get(foo).text)

		k = ""
		for i in newlist:
			if i['place'] > 500:
				k += "<ul>"
				k += "<li>" + str(i['place']) + "</li>"
				k += "<li>" + i['word'] + "</li>"
				k += "</ul>"
		k += str(len(newlist))
		return k

	html = """
		<form action="/cumle" method="post">
		  Cumle: <input type="text" name="cumle"><br>
		  <input type="submit" value="Submit">
		</form>
	"""
	return html
app.run(threaded=True)
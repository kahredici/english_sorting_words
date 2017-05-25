from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)
# app.debug = True


client = MongoClient()
db = client.words
# client.drop_database('words')

isRunedBefore = db.words.find_one({"isRunedBefore":1})
if isRunedBefore == None:
    print("Words are inserting to mongodb...\n")
    read = open("words.txt").readlines()
    
    for i in read:
        i = i.strip("\n")
        i = i.split("\t")
        place = i[0]
        word = i[1]

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
    word = db.words.find_one({"word":k['word']})
    del word['_id']
    word['percentage'] = str( int( (int(word['place'])/41284)*100))+"%"
    return json.dumps(word)

app.run()
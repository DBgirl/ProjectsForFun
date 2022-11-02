#imports
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
from urllib import parse
import urllib.request
import keys #I have used key.py to store my secret keys

app = Flask(__name__,template_folder='templates')

url = "http://api.giphy.com/v1/gifs/search"


#create chatbot
#englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
englishBot = ChatBot("zebe")
trainer = ChatterBotCorpusTrainer(englishBot)
trainer.train("chatterbot.corpus.english.movies",
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.conversations") #train the chatter bot for english

#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
#function for the bot response
def get_bot_response():
    userText = request.args.get('msg') #get input message
    botreply =str(englishBot.get_response(userText))
    print (botreply)
    params = parse.urlencode({  "q": {botreply[0:45]}, "api_key": keys.giphykey,  "limit": "1"}) #call API

    with urllib.request.urlopen("".join((url, "?", params))) as response:
      data = json.loads(response.read())
    #print("Before that - the url ",str(data['data'][0]['images']['original']['url']))
    return str(data['data'][0]['images']['downsized_large']['url']) #returns the URL

if __name__ == "__main__":
    app.run()
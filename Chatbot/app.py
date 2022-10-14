#imports
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import json
from urllib import parse
import urllib.request

app = Flask(__name__,template_folder='templates')


url = "http://api.giphy.com/v1/gifs/search"

params = parse.urlencode({
  "q": "That isn't my name",
  "api_key": "GMEINSldKQkIZIiRTKCvk08crSNGZWTl",
  "limit": "1"
})

with urllib.request.urlopen("".join((url, "?", params))) as response:
  data = json.loads(response.read())

print(json.dumps(data, sort_keys=True, indent=4))
#create chatbot
#englishBot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
englishBot = ChatBot("Bitter")
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
    userText = request.args.get('msg')
    return str(englishBot.get_response(userText))

if __name__ == "__main__":
    app.run()
from flask import Flask, jsonify
from flask_restful import Api, Resource
from tweet_sentiment_analysis import get_sentiment

app = Flask(__name__)
api = Api(app)


class Sentiment (Resource):
    def get(self, search_term, lang):
        return jsonify(get_sentiment(search_term, lang))


api.add_resource(
    Sentiment, "/getSentiment/<string:search_term>-<string:lang>")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

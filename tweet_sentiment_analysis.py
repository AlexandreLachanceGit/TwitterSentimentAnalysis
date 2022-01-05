import os
import requests
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer


def main():
    search_term = "Trump"
    lang = "en"  # en ou fr

    nb_tweets = 100
    nb_requests = 10

    sentiment_total = 0
    nb_sentiments_total = 0
    for j in range(0, nb_requests):
        if (j == 0):
            response = make_first_request(search_term, nb_tweets, lang)
        else:
            response = make_request(search_term, nb_tweets, lang, int(
                response["meta"]["oldest_id"]) - 1)

        nb_tweets = int(response["meta"]["result_count"])
        if (nb_tweets == 0):
            break
        print("Request {} (Number of tweets: {})".format(j, nb_tweets))

        for i in range(0, nb_tweets):
            if (lang == "fr"):
                blob = TextBlob(response["data"][i]["text"],
                                pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
            elif (lang == "en"):
                blob = TextBlob(response["data"][i]["text"])

            sentiment_total += blob.sentiment[0]
            nb_sentiments_total += 1

    average = sentiment_total / nb_sentiments_total
    print(average)


def get_headers():
    return {"Authorization": "Bearer {}".format(os.environ.get("BEARER_TOKEN"))}


def make_first_request(search_term, nb_tweets, lang):
    url = "https://api.twitter.com/2/tweets/search/recent?query={} -is:retweet lang:{}&max_results={}".format(
        search_term, lang, nb_tweets)
    return requests.get(url, headers=get_headers()).json()


def make_request(search_term, nb_tweets, lang, max_id):
    url = "https://api.twitter.com/2/tweets/search/recent?until_id={}&query={} -is:retweet lang:{}&max_results={}".format(str(max_id),
                                                                                                                          search_term, lang, nb_tweets)
    return requests.get(url, headers=get_headers()).json()


main()

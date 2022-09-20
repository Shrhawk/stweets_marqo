import argparse
import json

import marqo
import stweet

mq = marqo.Client(url='http://localhost:8882')
INDEX_NAME = "tweets"


def populate_tweets_index(term='#bitcoin'):
    """
    Populate tweets index using twitter search
    :param term: term for searching tweets
    :return:
    """
    search_tweets_task = stweet.SearchTweetsTask(all_words=term)
    output_jl_tweets = stweet.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = stweet.JsonLineFileRawOutput('output_raw_search_users.jl')
    tweets_collector = stweet.CollectorRawOutput()
    users_collector = stweet.CollectorRawOutput()
    stweet.TweetSearchRunner(
        search_tweets_task=search_tweets_task,
        tweet_raw_data_outputs=[tweets_collector, output_jl_tweets],
        user_raw_data_outputs=[users_collector, output_jl_users]
    ).run()
    documents = []
    for tweet_info in tweets_collector.get_raw_list():
        tweet = json.loads(tweet_info.raw_value)
        display_text_range = tweet.get('display_text_range', [])[1]
        documents.append({
            "Title": tweet.get('full_text')[:display_text_range],
            "Description": tweet.get('full_text'),
            "_id": tweet.get('id_str')
        })
    if documents:
        mq.index(INDEX_NAME).add_documents(documents)


def search_tweet(query=''):
    """
    search tweets using marqo index
    :param query:
    :return:
    """
    results = mq.index(INDEX_NAME).search(query, searchable_attributes=["Description"])
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--populate-index', action='store_true')
    parser.add_argument('--query')
    args = parser.parse_args()

    if args.populate_index:
        populate_tweets_index()
    else:
        search_tweet(query=args.query)

from .tweet_mapper import map_twitter_api_tweets
from .post_service import insert_posts, get_latest_post
from ..ml.pipeline import process_tweet
from ..scrapper import TwitterAPI, tweepy_finance_context_query

from multiprocessing import Process
from tqdm import tqdm

import os


def data_aggregation_task(language, num_tweets):
    if "TWITTER_API_BEARER_TOKEN" not in os.environ:
        raise ValueError("TWITTER_API_BEARER_TOKEN environment variable not configured")
    
    try:
        latest_tweet = get_latest_post(language)
        since_datetime = None
        if latest_tweet is not None:
            since_datetime = latest_tweet.tweet_date

        print(f"searching tweets with {language} lang, since_datetime: {since_datetime}")

        api = TwitterAPI(os.environ["TWITTER_API_BEARER_TOKEN"])
        query = tweepy_finance_context_query()
        tweets = api.search_tweets(query, exclude_replies=True, exclude_retweets=True, num_results=num_tweets, language=language, since=since_datetime)
        posts = map_twitter_api_tweets(tweets)

        print(f"embedding {len(posts)} posts")
        post2save = []
        for post in tqdm(posts):
            result = process_tweet(post.tweet_text, post.tweet_retweet_count, post.tweet_like_count)
            if result is not None:
                post.tweet_embeddings, post.fraud_score, post.social_score = result
                post2save.append(post)

        print(f"saving {len(post2save)} posts")
        insert_posts(post2save)
    except Exception as e:
        print(f"while performing data aggregation task ({language}): {e}")
        return

    print(f"Data aggregation task ({language}) has been completed!")


def start_aggregation_task_async(num_tweets):
    pl_process = Process(target = data_aggregation_task, args=("pl", num_tweets,))
    en_process = Process(target = data_aggregation_task, args=("en", num_tweets,))

    pl_process.start()
    en_process.start()

from ..model.post import Post

from typing import List
from datetime import datetime

def map_twitter_api_tweets(dicts) -> List[Post]:
    posts = []
    for d in dicts:
        try:
            post = Post(
                d["author_id"],
                d["author"]["username"],
                d["author"]["name"],
                d["author"]["verified"],
                d["created_at"],
                d["text"],
                d["id"],
                d["public_metrics"]["like_count"],
                d["public_metrics"]["reply_count"],
                d["public_metrics"]["retweet_count"],
                d["public_metrics"]["quote_count"],
                d["lang"],
                d["media_urls"]
            )
            posts.append(post)
        except Exception as e:
            print(f"map_twitter_api_tweets failure: {e}")

    return posts

def map_nitter_api_tweets(dicts) -> List[Post]:
    posts = []
    for d in dicts:
        try:
            post = Post(
                # TODO
            )

            posts.append(post)
        except:
            pass
    
    return posts
import tweepy

class TwitterAPI:
    def __init__(self, bearer_token):
        self._api = tweepy.Client(bearer_token)

    def search_tweets(
        self,
        keywords,
        exclude_replies = False,
        exclude_retweets = False,
        min_likes=0, 
        min_replies=0, 
        min_retweets=0,
        since=None,
        until=None,
        num_results=100,
        language="en"
    ):
        space_separated_q_items = [keywords]
        # not supported on standard twitter API plan 😡
        # space_separated_q_items.append(f"min_faves:{min_likes}")
        # space_separated_q_items.append(f"min_replies:{min_replies}")
        # space_separated_q_items.append(f"min_retweets:{min_retweets}")
        space_separated_q_items.append(f"lang:{language}")
        if exclude_replies:
            space_separated_q_items.append("-is:reply")
        if exclude_retweets:
            space_separated_q_items.append("-is:retweet")
        q_string = " ".join(space_separated_q_items)
        print(f"[Twitter API] query string: {q_string}")

        response = self._api.search_recent_tweets(
            q_string, 
            start_time=since, 
            end_time=until,
            max_results=num_results,
            tweet_fields=["public_metrics", "id", "author_id", "created_at", "lang"]
        )
        tweets = response[0]

        return [dict(t) for t in tweets]


from .nitter_scraper import get_tweets_using_query
from .nitter_scraper.query import QueryBuilder


NITTER_INSTANCE = "https://nitter.net"


class NitterAPI:
    def __init__(self, instance=NITTER_INSTANCE):
        self._instance_url = instance

    def scrap_tweets(
        self,
        keywords,
        exclude_replies = False,
        exclude_retweets = False,
        min_likes=0, 
        min_replies=0, 
        min_retweets=0,
        since=None,
        until=None,
        num_pages=1,
        language="en"
    ):
        query = QueryBuilder() \
            .keywords([keywords]) \
            .min_likes(min_likes) \
            .min_replies(min_replies) \
            .min_retweets(min_retweets) \
            .language(language)
        if since is not None:
            query = query.since(since)
        if until is not None:
            query = query.until(until)
        if exclude_retweets:
            query = query.exclude_retweets()
        if exclude_replies:
            query = query.exclude_replies()
        query_string = query.build()

        print(f"[Nitter API] query string: {query_string}")
        print(f"[Nitter API] Firing requests at nitter.net, to bypass twitter API which costs money.")

        tweets_gen = get_tweets_using_query(query_string, pages=num_pages, address=self._instance_url)
        tweet_dicts = [tweet.dict() for tweet in tweets_gen]

        return tweet_dicts
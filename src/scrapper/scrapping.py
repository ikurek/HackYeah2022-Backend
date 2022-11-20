import tweepy

class TwitterAPI:
    """
    Twitter search module using Epic Elon Musk Spaceman Twitter official API
    """
    
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

        next_token = None
        aggregated_tweets = []
        while len(aggregated_tweets) < num_results:
            print(f"[Twitter API] sending twitter request, next_token: {next_token}")
            (tweets, includes, _, page_info) = self._api.search_recent_tweets(
                q_string, 
                start_time=since, 
                end_time=until,
                max_results=min(num_results, 100),
                tweet_fields=["public_metrics", "id", "author_id", "created_at", "lang", "attachments"],
                user_fields=["name", "username", "verified"],
                media_fields=["url", "alt_text"],
                expansions=["attachments.media_keys", "author_id"],
                next_token=next_token
            )
            if len(tweets) == 0:
                break

            users = includes["users"] if "users" in includes else []
            media = includes["media"] if "media" in includes else []
            next_token = page_info["next_token"] if "next_token" in page_info else None
            if next_token is None:
                break
            tweet_dictionaries = self._parse_tweets(tweets, users, media)
            aggregated_tweets.extend(tweet_dictionaries)
        
        return aggregated_tweets

    def _parse_tweets(self, tweets, users, media):
        # `tweet_hashmaps` for JVM users 
        tweet_dictionaries = [dict(t) for t in tweets]

        for tweet_d in tweet_dictionaries:
            author_id = tweet_d["author_id"]
            if "attachments" in tweet_d and "media_keys" in tweet_d["attachments"]:
                keys = [u for u in tweet_d["attachments"]["media_keys"]]
                media_urls = []
                # linear search FTW, n^2 complexity, super fast WOW
                for key in keys:
                    try:
                        m = next((m for m in media if m.media_key == key))
                        media_urls.append({
                            "type": m.type,
                            "url": m.url 
                        })
                    except Exception as e:
                        print(f"Media {key} not found: {e}")
                tweet_d["media_urls"] = media_urls
            else:
                tweet_d["media_urls"] = []
            
            try:
                author = next((u for u in users if u.id == author_id))
                tweet_d["author"] = {
                    "name": author.name,
                    "username": author.username,
                    "verified": author.verified 
                }
            except Exception as e:
                print(f"Users {author_id} not found: {e}")
                tweet_d["author"] = None

        # Me after writing this method:
        # https://bit.ly/2HUmo98

        return tweet_dictionaries

from .nitter_scraper import get_tweets_using_query
from .nitter_scraper.query import QueryBuilder


NITTER_INSTANCE = "https://nitter.net"


class NitterAPI:
    """
    Twitter search module using Nitter - alternative twitter frontend
    """
    
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
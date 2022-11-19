from nitter_scraper.nitter import NitterScraper
from nitter_scraper.profile import get_profile
from nitter_scraper.tweets import get_tweets, get_tweets_using_query, get_replies_for_tweet

__all__ = ["get_profile", "get_tweets", "get_tweets_using_query", "get_replies_for_tweet", "NitterScraper"]

__version__ = "0.5.2"

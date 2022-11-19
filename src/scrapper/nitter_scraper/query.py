from urllib.parse import urlencode
from datetime import date

class QueryBuilder:
    def __init__(self):
        self._query = ""
        self._query_items = dict()
        self._additional_url_query_items = dict()
        self._since = ""
        self._until = ""
    
    def min_likes(self, count):
        self._query_items["min_faves"] = count
        return self

    def min_replies(self, count):
        self._query_items["min_replies"] = count
        return self
    
    def min_retweets(self, count):
        self._query_items["min_retweets"] = count
        return self

    def since_time(self, timestamp):
        assert(type(timestamp) == int)
        self._query_items["since_time"] = timestamp
        return self

    def until_time(self, timestamp):
        assert(type(timestamp) == int)
        self._query_items["until_time"] = timestamp
        return self

    def keywords(self, keywords):
        self._query = " ".join(keywords)
        return self

    def since(self, since_date):
        assert(type(since_date) == date)
        self._since = since_date.strftime("%Y-%m-%d")
        return self

    def until(self, until_date):
        assert(type(until_date) == date)
        self._until = until_date.strftime("%Y-%m-%d")
        return self

    def exclude_replies(self):
        self._additional_url_query_items["e-replies"] = "on"
        return self
    
    def exclude_retweets(self):
        self._additional_url_query_items["e-nativeretweets"] = "on"
        return self

    def language(self, lang):
        self._query_items["lang"] = lang
        return self

    def build(self):
        space_separated_q_items = [self._query] + [f"{k}:{v}" for k, v in self._query_items.items()]
        q_string = " ".join(space_separated_q_items)
        items = {
            "f": "tweets",
            "q": q_string,
            "until": self._until,
            "since": self._since,
            **self._additional_url_query_items
        }

        return urlencode(items)
"""Module for scraping tweets"""
from datetime import datetime
import re
from typing import Dict, Optional, Callable

from requests_html import HTMLSession

from nitter_scraper.schema import Tweet  # noqa: I100, I202

import time


def link_parser(tweet_link):
    links = list(tweet_link.links)
    tweet_url = links[0]
    parts = links[0].split("/")

    tweet_id = parts[-1].replace("#m", "")
    username = parts[1]
    return tweet_id, username, tweet_url


def date_parser(tweet_date):
    try: 
        new_format = "%b %d, %Y · %I:%M %p %Z"
        d = datetime.strptime(tweet_date, new_format)
        day, month, year = d.day, d.month, d.year
        hour, minute, second = d.hour, d.minute, d.second
    except:
        split_datetime = tweet_date.split(",")
        day, month, year = split_datetime[0].strip().split("/")
        hour, minute, second = split_datetime[1].strip().split(":")

    data = {}

    data["day"] = int(day)
    data["month"] = int(month)
    data["year"] = int(year)

    data["hour"] = int(hour)
    data["minute"] = int(minute)
    data["second"] = int(second)

    return datetime(**data)


def clean_stat(stat):
    return int(stat.replace(",", ""))


def stats_parser(tweet_stats):
    stats = {}
    for ic in tweet_stats.find(".icon-container"):
        key = ic.find("span", first=True).attrs["class"][0].replace("icon", "").replace("-", "")
        value = ic.text
        stats[key] = value
    return stats


def attachment_parser(attachments):
    photos, videos = [], []
    if attachments:
        photos = [i.attrs["src"] for i in attachments.find("img")]
        videos = [i.attrs["src"] for i in attachments.find("source")]
    return photos, videos


def cashtag_parser(text):
    cashtag_regex = re.compile(r"\$[^\d\s]\w*")
    return cashtag_regex.findall(text)


def hashtag_parser(text):
    hashtag_regex = re.compile(r"\#[^\d\s]\w*")
    return hashtag_regex.findall(text)


def url_parser(links):
    return sorted(filter(lambda link: "http://" in link or "https://" in link, links))


def parse_tweet(html) -> Dict:
    data = {}
    
    id, username, url = link_parser(html.find(".tweet-link", first=True))
    data["tweet_id"] = id
    data["tweet_url"] = url
    data["username"] = username

    retweet = html.find(".retweet-header .icon-container .icon-retweet", first=True)
    data["is_retweet"] = True if retweet else False

    body = html.find(".tweet-body", first=True)

    pinned = body.find(".pinned", first=True)
    data["is_pinned"] = True if pinned is not None else False

    data["time"] = date_parser(body.find(".tweet-date a", first=True).attrs["title"])

    content = body.find(".tweet-content", first=True)
    data["text"] = content.text

    # tweet_header = html.find(".tweet-header") #NOTE: Maybe useful later on

    stats = stats_parser(html.find(".tweet-stats", first=True))

    if stats.get("comment"):
        data["replies"] = clean_stat(stats.get("comment"))
    else:
        data["replies"] = 0

    if stats.get("retweet"):
        data["retweets"] = clean_stat(stats.get("retweet"))
    else:
        data["retweets"] = 0

    if stats.get("heart"):
        data["likes"] = clean_stat(stats.get("heart"))
    else:
        data["likes"] = 0
    
    entries = {}
    entries["hashtags"] = hashtag_parser(content.text)
    entries["cashtags"] = cashtag_parser(content.text)
    entries["urls"] = url_parser(content.links)

    photos, videos = attachment_parser(body.find(".attachments", first=True))
    entries["photos"] = photos
    entries["videos"] = videos

    data["entries"] = entries
    # quote = html.find(".quote", first=True) #NOTE: Maybe useful later on
    return data

def replies_parser(html):
    return html.find(".replies", first=True)

def timeline_parser(html):
    return html.find(".timeline", first=True)

def pagination_parser(timeline, base_url):
    try:
        next_page = list(timeline.find(".show-more")[-1].links)[0]
        return f"{base_url}{next_page}"
    except:
        return None


def _get_tweets(
    base_url: str,
    root_element_getter: Callable,
    initial_url: Optional[str] = None,
    pages: int = 25,
    delay: int = 2,
    break_on_tweet_id: Optional[int] = None,
) -> Tweet:
    """Gets the target users tweets

    Args:
        username: Targeted users username.
        pages: Max number of pages to lookback starting from the latest tweet.
        break_on_tweet_id: Gives the ability to break out of a loop if a tweets id is found.
        address: The address to scrape from. The default is https://nitter.net which should
            be used as a fallback address.

    Yields:
        Tweet Objects

    """

    session = HTMLSession()
    url = initial_url or base_url

    def gen_tweets(pages):
        response = session.get(url)

        while pages > 0:
            if response.status_code == 200:
                root = root_element_getter(response.html)

                next_url = pagination_parser(root, base_url)
                if next_url is None:
                    print("Next page not available")
                    break
                
                timeline_items = root.find(".timeline-item")

                for item in timeline_items:
                    if "show-more" in item.attrs["class"] or "more-replies" in item.attrs["class"] or "unavailable" in item.attrs["class"]:
                        continue

                    tweet_data = parse_tweet(item)
                    tweet = Tweet.from_dict(tweet_data)

                    if tweet.tweet_id == break_on_tweet_id:
                        pages = 0
                        break

                    yield tweet
            else:
                print(f"Received non 200 response: {response}, html: {response.html._html}")
                break

            print(f"Sleeping for {delay} seconds, {pages-1} pages remaining...")
            time.sleep(delay)

            response = session.get(next_url)
            pages -= 1

    yield from gen_tweets(pages)


def get_replies_for_tweet(
    path: str,
    pages: int = 25,
    delay: int = 2,
    address="https://nitter.net"
) -> Tweet:
    url = f"{address}{path}"
    return _get_tweets(
        base_url=url,
        root_element_getter=replies_parser,
        pages=pages,
        delay=delay
    )


def get_tweets_using_query(
    query: str,
    pages: int = 25,
    delay: int = 2,
    address="https://nitter.net"
) -> Tweet:
    base_url = f"{address}/search"
    initial_url = f"{address}/search?{query}"
    return _get_tweets(
        base_url=base_url,
        root_element_getter=timeline_parser,
        initial_url=initial_url,
        pages=pages,
        delay=delay
    )


def get_tweets(
    username: str,
    pages: int = 25,
    break_on_tweet_id: Optional[int] = None,
    address="https://nitter.net",
) -> Tweet:
    url = f"{address}/{username}"
    return _get_tweets(
        base_url=url,
        root_element_getter=timeline_parser,
        pages=pages,
        delay=delay,
        break_on_tweet_id=break_on_tweet_id
    )

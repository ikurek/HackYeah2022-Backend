import datetime

import json
from flask import Flask, request
from src.database import init_db
from src.service import post_service
from src.service import search_service
from src.model.post import Post, PostSchema
from datetime import datetime

init_db()
app = Flask(__name__)
post_schema = PostSchema()


@app.route('/setup')
def setup():
    post = Post(
        tweet_id="123",
        tweet_author_id="Tweet ID",
        tweet_author_username="Author Username",
        tweet_author_display_name="Author Displayname",
        tweet_author_is_verified=True,
        tweet_date=datetime.now(),
        tweet_text="Tweet content"
    )
    post_service.insert_post(post)
    return ""


@app.route('/posts')
def get_posts():
    args = request.args
    posts = post_service.get_all_posts(
        from_date=datetime.fromisoformat(args.get('from_date', datetime.min.isoformat())),
        to_date=datetime.fromisoformat(args.get('to_date', datetime.max.isoformat()))
    )
    return post_schema.dump(posts, many=True)


@app.route('/posts/<post_id>')
def get_post(post_id: int):
    post = post_service.get_post(post_id=post_id)
    return post_schema.dump(post, many=False)


@app.route('/search')
def search():
    args = request.args
    posts = search_service.find_posts(
        smart_search_query=args.get('smart_search_query', ''),
        keyword=args.get('keyword', ''),
        author_username=args.get('author_username', ''),
        from_date=datetime.fromisoformat(args.get('from_date', datetime.min.isoformat())),
        to_date=datetime.fromisoformat(args.get('to_date', datetime.max.isoformat()))
    )
    return post_schema.dump(posts, many=True)

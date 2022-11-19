import datetime

import json
from flask import Flask
from src.database import init_db
from src.service import post_service
from src.model.post import Post, PostSchema

init_db()
app = Flask(__name__)
post_schema = PostSchema()


@app.route('/setup')
def setup():
    post = Post(
        tweet_id="123",
        tweet_author_id="Tweet ID",
        tweet_author_username="Author Username",
        tweet_author_displayname="Author Displayname",
        tweet_author_is_verified=True,
        tweet_date=datetime.datetime.now(),
        tweet_text="Tweet content"
    )
    post_service.insert_post(post)
    return


@app.route('/posts')
def get_posts():
    posts = post_service.get_all_posts()
    return post_schema.dump(posts, many=True)


@app.route('/posts/<post_id>')
def get_post(post_id: int):
    post = post_service.get_post(post_id=post_id)
    return post_schema.dump(post, many=False)

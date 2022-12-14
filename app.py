from src.database import init_db
from src.service import post_service, search_service, image_service, aggregation_service
from src.model.post import Post, PostSchema
from src.model.score import Score, ScoreSchema
from src.model.influencer import Influencer, InfluencerSchema
from datetime import datetime

import os
from flask import Flask, request
from typing import Optional

ALLOWED_IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

init_db()
app = Flask(__name__)
post_schema = PostSchema()
score_schema = ScoreSchema()
influencer_schema = InfluencerSchema()


@app.after_request
def apply_caching(response):
    response.headers['Content-Type'] = "application/json"
    response.headers['Accept'] = "*/*"
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, OPTIONS, PUT, PATCH, DELETE"
    response.headers['Access-Control-Allow-Headers'] = "X-Requested-With,content-type"
    response.headers['Access-Control-Allow-Credentials'] = "true"
    return response


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
        from_date=read_date(args, 'from_date'),
        to_date=read_date(args, 'to_date')
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
        from_date=read_date(args, 'from_date'),
        to_date=read_date(args, 'to_date')
    )
    return post_schema.dump(posts, many=True)


@app.route('/sync', defaults={'count': None})
@app.route('/sync/<count>')
def sync_tweets(count: Optional[int]):
    num_tweets = 100 if count is None else int(count)
    aggregation_service.start_aggregation_task_async(num_tweets)
    return ""


@app.route('/review/<post_id>')
def manual_review(post_id: int):
    args = request.args
    def update_block(post):
        post.manually_reviewed = bool(args.get("value"))
    post_service.update_post(post_id, update_block)
    return ""


@app.route('/imagescore', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "File not found", 400
    file = request.files['file']
    if file.filename == '':
        return "Filename not found", 400
    if file and allowed_image_file(file.filename):
        score = image_service.score_image_file(file)
        return score_schema.dump(score)

    
@app.route('/finfluencers')
def get_ranked_finfluencers():
    args = request.args
    author_ranking = search_service.get_author_ranking(
        from_date=read_date(args, 'from_date'),
        to_date=read_date(args, 'to_date')
    )
    return influencer_schema.dump(author_ranking, many=True)


def read_date(args, name) -> datetime:
    try:
        arg = args.get(name)
        if arg is None:
            raise ValueError
        return datetime.fromisoformat(arg)
    except ValueError:
        if name == 'from_date':
            return datetime.min
        elif name == 'to_date':
            return datetime.max
        else:
            raise ValueError


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_FILE_EXTENSIONS

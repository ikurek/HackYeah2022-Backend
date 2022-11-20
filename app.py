import datetime

import os
from flask import Flask, request
from src.database import init_db
from src.service import post_service, search_service, image_service, aggregation_service
from src.model.post import Post, PostSchema
from src.model.score import Score, ScoreSchema
from datetime import datetime
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg'}

init_db()
app = Flask(__name__)
post_schema = PostSchema()
score_schema = ScoreSchema()


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


@app.route('/sync')
def sync_tweets():
    aggregation_service.start_aggregation_task_async()
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


def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_FILE_EXTENSIONS

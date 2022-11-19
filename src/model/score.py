from datetime import datetime
from marshmallow import Schema, fields


class Score:
    def __init__(self, score: float):
        self.score = score

    def __repr__(self):
        return f'<Score {self.score!r}>'


class ScoreSchema(Schema):
    score = fields.Float()

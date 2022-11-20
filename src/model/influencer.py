from marshmallow import Schema, fields


class Influencer:
    def __init__(self, id, username: str, name: str, score: float):
        self.id = id
        self.username = username
        self.name = name
        self.score = score

    def __repr__(self):
        return f"<Influencer {self.username}>"


class InfluencerSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    name = fields.Str()
    score = fields.Float()

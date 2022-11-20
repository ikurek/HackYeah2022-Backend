from marshmallow import Schema, fields


class Influencer:
    def __init__(self, id, username: str, name: str, fraud_score: int, social_score: int):
        self.id = id
        self.username = username
        self.name = name
        self.fraud_score = fraud_score
        self.social_score = social_score

    def __repr__(self):
        return f"<Influencer {self.username}>"


class InfluencerSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    name = fields.Str()
    fraud_score = fields.Int()
    social_score = fields.Int()

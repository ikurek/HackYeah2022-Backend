import math

RETWEET_WEIGHT = 5
LIKE_WEIGHT = 2
LOGARITHM_MAX_POWER = 4
def calculate_social_scoring(fraud_score: float, retweet_count: int, like_count: int):
    influence = RETWEET_WEIGHT * retweet_count + LIKE_WEIGHT * like_count
    influence = math.log(influence)
    influence = min(influence, LOGARITHM_MAX_POWER)

    return math.ceil(fraud_score * influence / 4)


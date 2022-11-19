FINANCE_DOMAIN_ENTITY_PAIRS = [
    # business & finance
    (45,781974596148793345),
    (65,781974596148793345),
    (131,781974596148793345),
    (66,847888632711061504),
    (131,847888632711061504),
    (67,1037075567227494400),
    # investing
    (67,847894353708068864),
    (131,847894353708068864),
    (67,847890600674250753),
    # saving 
    (67,1321912164496470016),
    (131,1321912164496470016)
]

def tweepy_finance_context_query() -> str:
    query_components = []
    for (domain_id, entity_id) in FINANCE_DOMAIN_ENTITY_PAIRS:
        query_components.append(f"context:{domain_id}.{entity_id}")

    query = " OR ".join(query_components)
    return f"({query})"

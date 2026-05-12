import re


GENDER_KEYWORDS = {
    "male": ["male", "males",],
    "female": ["female", "females"]
}


filters = {}


def parse_nl_query(query: str) -> dict:
    query = query.strip().lower()

    has_male = any(re.search(r'\b' + kw + r'\b', query) for kw in GENDER_KEYWORDS["male"])
    has_female = any(re.search(r'\b' + kw + r'\b', query) for kw in GENDER_KEYWORDS["female"])
    
    if has_male and has_female:
        filters["gender"] = None
    elif has_female:
        filters["gender"] = "female"
    elif has_male:
        filters["gender"] = "male"

    return filters
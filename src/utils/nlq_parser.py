import re


COUNTRY_MAP: dict[str, str] = {
    "nigeria": "NG", "nigerian": "NG",
    "ghana": "GH", "ghanaian": "GH",
    "kenya": "KE", "kenyan": "KE",
    "south africa": "ZA", "south african": "ZA",
    "ethiopia": "ET", "ethiopian": "ET",
    "egypt": "EG", "egyptian": "EG",
    "tanzania": "TZ", "tanzanian": "TZ",
    "uganda": "UG", "ugandan": "UG",
    "angola": "AO", "angolan": "AO",
    "cameroon": "CM", "cameroonian": "CM",
    "senegal": "SN", "senegalese": "SN",
    "mali": "ML", "malian": "ML",
    "ivory coast": "CI", "cote d'ivoire": "CI",
    "mozambique": "MZ", "mozambican": "MZ",
    "zambia": "ZM", "zambian": "ZM",
    "zimbabwe": "ZW", "zimbabwean": "ZW",
    "rwanda": "RW", "rwandan": "RW",
    "benin": "BJ", "beninese": "BJ",
    "togo": "TG", "togolese": "TG",
    "niger": "NE", "nigerien": "NE",
    "burkina faso": "BF", "burkinabe": "BF",
    "guinea": "GN", "guinean": "GN",
    "gabon": "GA", "gabonese": "GA",
    "congo": "CG", "congolese": "CG",
    "democratic republic of congo": "CD", "drc": "CD",
    "somalia": "SO", "somali": "SO",
    "sudan": "SD", "sudanese": "SD",
    "libya": "LY", "libyan": "LY",
    "morocco": "MA", "moroccan": "MA",
    "algeria": "DZ", "algerian": "DZ",
    "tunisia": "TN", "tunisian": "TN",
    "united states": "US", "usa": "US", "american": "US",
    "united kingdom": "GB", "uk": "GB", "britain": "GB", "british": "GB",
    "france": "FR", "french": "FR",
    "germany": "DE", "german": "DE",
    "india": "IN", "indian": "IN",
    "china": "CN", "chinese": "CN",
    "brazil": "BR", "brazilian": "BR",
    "canada": "CA", "canadian": "CA",
    "australia": "AU", "australian": "AU",
    "japan": "JP", "japanese": "JP",
    "russia": "RU", "russian": "RU",
    "mexico": "MX", "mexican": "MX",
    "indonesia": "ID", "indonesian": "ID",
    "pakistan": "PK", "pakistani": "PK",
    "bangladesh": "BD", "bangladeshi": "BD",
    "philippines": "PH", "philippine": "PH", "filipino": "PH",
    "vietnam": "VN", "vietnamese": "VN",
    "turkey": "TR", "turkish": "TR",
    "iran": "IR", "iranian": "IR",
    "iraq": "IQ", "iraqi": "IQ",
    "saudi arabia": "SA", "saudi": "SA",
    "spain": "ES", "spanish": "ES",
    "italy": "IT", "italian": "IT",
    "colombia": "CO", "colombian": "CO",
    "argentina": "AR", "argentinian": "AR",
    "poland": "PL", "polish": "PL",
    "ukraine": "UA", "ukrainian": "UA",
    "netherlands": "NL", "dutch": "NL",
    "portugal": "PT", "portuguese": "PT",
    "sweden": "SE", "swedish": "SE",
    "norway": "NO", "norwegian": "NO",
    "denmark": "DK", "danish": "DK",
    "finland": "FI", "finnish": "FI",
    "switzerland": "CH", "swiss": "CH",
    "austria": "AT", "austrian": "AT",
    "belgium": "BE", "belgian": "BE",
    "new zealand": "NZ",
    "malawi": "MW", "malawian": "MW",
    "namibia": "NA", "namibian": "NA",
    "botswana": "BW", "batswana": "BW",
    "lesotho": "LS",
    "swaziland": "SZ", "eswatini": "SZ",
    "eritrea": "ER", "eritrean": "ER",
    "djibouti": "DJ", "djiboutian": "DJ",
    "comoros": "KM",
    "seychelles": "SC",
    "mauritius": "MU",
    "mauritanian": "MR", "mauritania": "MR",
    "cape verde": "CV",
    "sao tome": "ST",
    "equatorial guinea": "GQ",
    "central african republic": "CF",
    "chad": "TD", "chadian": "TD",
    "sierra leone": "SL",
    "liberia": "LR", "liberian": "LR",
    "gambia": "GM", "gambian": "GM",
}


GENDER_KEYWORDS = {
    "male": ["male", "males",],
    "female": ["female", "females"]
}


AGE_GROUP_KEYWORDS = {
    "child": ["child", "children", "kids", "kid"],
    "teenager": ["teenager", "teenagers", "teen", "teens", "adolescent", "adolescents", "youth"],
    "adult": ["adult", "adults"],
    "senior": ["senior", "seniors", "elderly", "elder", "old"],
    "young": ["young"],
}


filters = {}


def parse_nl_query(query: str) -> dict:
    query = query.strip().lower()

    # Gender matching
    has_male = any(re.search(r'\b' + kw + r'\b', query) for kw in GENDER_KEYWORDS["male"])
    has_female = any(re.search(r'\b' + kw + r'\b', query) for kw in GENDER_KEYWORDS["female"])
    
    if has_male and has_female:
        filters["gender"] = None
    elif has_female:
        filters["gender"] = "female"
    elif has_male:
        filters["gender"] = "male"

    # Country matching - using "from X" pattern
    pattern = r'\bfrom\s+([a-z]+(?:\s+[a-z]+)*)(?=\s+(?:aged?|above|over|below|under|between|who|that|with)\b|\s*$)'
    from_match = re.search(pattern, query)
    if from_match:
        possible_country = from_match.group(1).strip()
        if possible_country in COUNTRY_MAP:
            filters["country_id"] = COUNTRY_MAP[possible_country]

    # Match Age groups
    for group, keywords in AGE_GROUP_KEYWORDS.items():
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        if re.search(pattern, query):
            if group == "young":
                filters["min_age"] = 16
                filters["max_age"] = 24
            else:
                filters["age_group"] = group

    # Match "Above age x"
    above_match = re.search(
        r'\b(?:above|over|older than|greater than)(?:\s+the)?(?:\s+age)?(?:\s+of)?\s+(\d+)\b',
        query)
    if above_match:
        filters["min_age"] = int(above_match.group(1)) + 1

    # Match "Below age x"
    below_match = re.search(
        r'\b(?:below|under|younger than|less than)(?:\s+the)?(?:\s+age)?(?:\s+of)?\s+(\d+)\b',
        query)
    if below_match:
        filters["max_age"] = int(below_match.group(1)) - 1

    # Match "between X and Y age"
    between_match = re.search(r'\bbetween\s+(\d+)\s+and\s+(\d+)\b', query)
    if between_match:
        filters["min_age"] = int(between_match.group(1))
        filters["max_age"] = int(between_match.group(2))

    # Match "aged X" / "age X"
    aged_match = re.search(r'\b(?:aged?|age)\s+(\d+)\b', query)
    if aged_match:
        age = int(aged_match.group(1))
        filters["min_age"] = age
        filters["max_age"] = age

    return filters
from pieces_keywords import pieces_keywords

def get_domain_from_keyword(keyword):
    for domain, keywords in pieces_keywords.items():
        if keyword in keywords:
            return domain
    return "Unknown"

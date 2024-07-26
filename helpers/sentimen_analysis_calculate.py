def calculate_average_sentiment_score_and_label(sentiment_counts):
    n5 = sentiment_counts.get('Sangat Puas', 0)
    n4 = sentiment_counts.get('Puas', 0)
    n3 = sentiment_counts.get('Netral', 0)
    n2 = sentiment_counts.get('Tidak Puas', 0)
    n1 = sentiment_counts.get('Sangat Tidak Puas', 0)
    
    total_reviews = n5 + n4 + n3 + n2 + n1
    if total_reviews == 0:
        return 0, "No Reviews"
    
    R = (5 * n5 + 4 * n4 + 3 * n3 + 2 * n2 + 1 * n1) / total_reviews
    
    if R >= 4.5:
        sentiment_label = "Sangat Puas"
    elif R >= 3.5:
        sentiment_label = "Puas"
    elif R >= 2.5:
        sentiment_label = "Netral"
    elif R >= 1.5:
        sentiment_label = "Tidak Puas"
    else:
        sentiment_label = "Sangat Tidak Puas"
    
    return R, sentiment_label

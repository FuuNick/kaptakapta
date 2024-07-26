def calculate_overall_average_sentiment(results_df):
    return results_df['Satisfaction Score'].mean()

def generate_overall_conclusion(overall_average_score):
    if overall_average_score >= 4.5:
        return "Aplikasi ini Sangat Puas"
    elif overall_average_score >= 3.5:
        return "Aplikasi ini Puas"
    elif overall_average_score >= 2.5:
        return "Aplikasi ini Netral"
    elif overall_average_score >= 1.5:
        return "Aplikasi ini Tidak Puas"
    else:
        return "Aplikasi ini Sangat Tidak Puas"


def generate_overall_score_and_conclusion(results_df):
    overall_average_score = calculate_overall_average_sentiment(results_df)
    overall_conclusion = generate_overall_conclusion(overall_average_score)
    return overall_average_score, overall_conclusion


def calculate_sentiment_scores(results_df):
    sentiment_scores = []
    for review in results_df['Review']:
        domain = get_domain_from_keyword(review['Most Similar Keyword'])
        sentiment_score, sentiment_label = calculate_sentiment_score_and_label(review['Review'], domain)
        sentiment_scores.append({
            'Review': review['Review'],
            'Domain': domain,
            'Satisfaction Score': sentiment_score,
            'Satisfaction': sentiment_label
        })
    return pd.DataFrame(sentiment_scores)


def analyze_sentiment(results_df):
    sentiment_scores_df = calculate_sentiment_scores(results_df)
    overall_average_score, overall_conclusion = generate_overall_score_and_conclusion(sentiment_scores_df)
    return sentiment_scores_df, overall_average_score, overall_conclusion

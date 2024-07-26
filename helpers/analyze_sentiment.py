import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
from googletrans import Translator
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

@lru_cache(maxsize=None)
def translate_cache(text, target_language='id'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def analyze_sentiment_vader(review):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(review)['compound']
    if sentiment_score >= 0.5:
        sentiment_label = "Sangat Puas"
    elif sentiment_score >= 0.1:
        sentiment_label = "Puas"
    elif sentiment_score >= -0.1:
        sentiment_label = "Netral"
    elif sentiment_score >= -0.5:
        sentiment_label = "Tidak Puas"
    else:
        sentiment_label = "Sangat Tidak Puas"
    return sentiment_label

def analyze_sentiment_textblob(review):
    sentiment_score = TextBlob(review).sentiment.polarity
    if sentiment_score >= 0.5:
        sentiment_label = "Sangat Puas"
    elif sentiment_score >= 0.1:
        sentiment_label = "Puas"
    elif sentiment_score >= -0.1:
        sentiment_label = "Netral"
    elif sentiment_score >= -0.5:
        sentiment_label = "Tidak Puas"
    else:
        sentiment_label = "Sangat Tidak Puas"
    return sentiment_label

def analyze_sentiment_similarity(reviews_df, keywords, model='vader'):
    reviews = reviews_df["content_translated"].tolist()

    with ThreadPoolExecutor() as executor:
        reviews_en = list(executor.map(translate_cache, reviews))
        keywords_en = list(executor.map(translate_cache, keywords))
    
    vectorizer = TfidfVectorizer()
    reviews_vectors = vectorizer.fit_transform(reviews_en)
    keywords_vectors = vectorizer.transform(keywords_en)
    similarity_scores = cosine_similarity(reviews_vectors, keywords_vectors)
    
    results = []
    for i, review in enumerate(reviews):
        max_similarity_score = max(similarity_scores[i])
        max_similarity_index = similarity_scores[i].argmax()
        most_similar_keyword = keywords_en[max_similarity_index]
        
        if model == 'vader':
            sentiment_label = analyze_sentiment_vader(review)
        elif model == 'textblob':
            sentiment_label = analyze_sentiment_textblob(review)
        elif model == 'bert':
            sentiment_label = analyze_sentiment_bert(review)
        else:
            raise ValueError(f"Unknown model: {model}")

        review_id = translate_cache(review, 'id')
        most_similar_keyword_id = translate_cache(most_similar_keyword, 'id')

        results.append({
            "Review": review_id,
            "Most Similar Keyword": most_similar_keyword_id,
            "Satisfaction": sentiment_label
        })
    
    results_df = pd.DataFrame(results)
    return results_df

def fetch_and_translate_reviews(app_id, num_reviews, translate_to_english):
    result, continuation_token = reviews(
        app_id,
        lang='id',
        country='id',
        sort=Sort.MOST_RELEVANT,
        count=num_reviews,
        filter_score_with=None
    )
    df = pd.DataFrame(result)
    df['content_translated'] = df['content'].apply(translate_to_english)
    return df[['score', 'content_translated']]

def translate_text(text, target_language='id'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

if __name__ == "__main__":
    app_id = 'your.app.id.here'
    num_reviews = 100
    translate_to_english = lambda x: x  

    reviews_df = fetch_and_translate_reviews(app_id, num_reviews, translate_to_english)

    keywords = ['good', 'bad', 'excellent', 'poor', 'satisfactory']

    results_df = analyze_sentiment_similarity(reviews_df, keywords, model='vader')

    print(results_df.head())
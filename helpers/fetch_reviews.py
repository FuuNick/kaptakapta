import pandas as pd
from google_play_scraper import Sort, reviews
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import re
import string
from nltk.corpus import stopwords

# Fetch and translate reviews function
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

# Text cleaning function
def clean_text(text):
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Pre-process reviews function
def pre_process_reviews(df):
    # Handle missing values
    df['content_translated'].fillna('', inplace=True)
    
    # Clean text data
    df['content_cleaned'] = df['content_translated'].apply(clean_text)
    
    # Feature scaling for score
    scaler = StandardScaler()
    df['score_scaled'] = scaler.fit_transform(df[['score']])
    
    return df

# Vectorize text data
def vectorize_text(df):
    vectorizer = TfidfVectorizer()
    X_text = vectorizer.fit_transform(df['content_cleaned'])
    return X_text, vectorizer

# Main function to fetch, translate, and pre-process reviews
def main():
    # Parameters
    app_id = 'your.app.id.here'
    num_reviews = 100
    translate_to_english = lambda x: x  # Dummy translation function for now
    
    # Fetch and translate reviews
    df = fetch_and_translate_reviews(app_id, num_reviews, translate_to_english)
    
    # Pre-process reviews
    df = pre_process_reviews(df)
    
    # Vectorize text data
    X_text, vectorizer = vectorize_text(df)
    
    # Combine features
    X = pd.concat([pd.DataFrame(X_text.toarray()), df[['score_scaled']].reset_index(drop=True)], axis=1)
    y = df['score']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f'Training set shape: {X_train.shape}')
    print(f'Test set shape: {X_test.shape}')

if __name__ == "__main__":
    main()

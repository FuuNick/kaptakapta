import streamlit as st
import pandas as pd
from google_play_scraper import Sort
from helpers.fetch_reviews import fetch_and_translate_reviews
from helpers.analyze_sentiment import analyze_sentiment_similarity
from helpers.translate_reviews import translate_to_english
from helpers.utils import get_domain_from_keyword
from helpers.plotting import plot_sentiment_distribution
# from helpers.sentiment_analysis import generate_overall_score_and_conclusion
from pieces_keywords import pieces_keywords
from helpers.sentimen_analysis_calculate import calculate_average_sentiment_score_and_label

st.set_page_config(page_title="Google Play Store Review Analyzer", layout="wide")
st.title("Google Play Store Review Analyzer")
st.markdown("Analyze and visualize reviews from Google Play Store apps")

with st.sidebar:    
    app_id = st.text_input("Enter the App ID (e.g., id.or.muhammadiyah.quran):", "id.or.muhammadiyah.quran")
    sort_by = st.selectbox("Sort Reviews By", options=["Most Relevant", "Newest"], index=0)
    sort_mapping = {"Most Relevant": Sort.MOST_RELEVANT, "Newest": Sort.NEWEST}
    model = st.selectbox("Select Sentiment Model", options=["VADER", "TextBlob", "BERT"], index=0)
    model_mapping = {"VADER": "vader", "TextBlob": "textblob", "BERT": "bert"}
    
    analyze_option = st.radio("Choose Analysis Option", ["Combine all PIECES domains", "Choose one domain"])

    if analyze_option == "Choose one domain":
        selected_domain = st.selectbox("Select Domain", options=list(pieces_keywords.keys()))
        st.write(f"Domain selected: {selected_domain}")
        all_keywords = pieces_keywords[selected_domain]
    else:
        all_keywords = [keyword for keywords in pieces_keywords.values() for keyword in keywords]

num_reviews = 50

if st.sidebar.button("Fetch and Analyze Reviews"):
    with st.spinner("Fetching reviews..."):
        reviews_df = fetch_and_translate_reviews(app_id, num_reviews, translate_to_english)
    st.success("Reviews fetched and translated successfully!")

    with st.spinner("Analyzing sentiment and similarity..."):
        results_df = analyze_sentiment_similarity(reviews_df, all_keywords, model=model_mapping[model])
    st.success("Analysis completed successfully!")

    st.markdown("### Tabel Hasil Analisis")
    st.dataframe(results_df)

    total_keywords = results_df["Most Similar Keyword"].value_counts().to_dict()
    sentiment_counts = results_df['Satisfaction'].value_counts().reindex(['Sangat Tidak Puas', 'Tidak Puas', 'Netral', 'Puas', 'Sangat Puas'], fill_value=0)

    plot_sentiment_distribution(sentiment_counts)

    R, sentiment_label = calculate_average_sentiment_score_and_label(sentiment_counts)

    satisfaction_mapping = {
        'Sangat Tidak Puas': 1,
        'Tidak Puas': 2,
        'Netral': 3,
        'Puas': 4,
        'Sangat Puas': 5
    }

    results_df['Satisfaction Score'] = results_df['Satisfaction'].map(satisfaction_mapping)

    # overall_average_score, overall_conclusion = generate_overall_score_and_conclusion(results_df)

    keyword_counts = pd.DataFrame(total_keywords.items(), columns=["Keyword", "Total"])
    keyword_counts.sort_values(by="Total", ascending=False, inplace=True)

    st.markdown("### Tabel Total Keyword Yang Terkait dengan Review")
    st.dataframe(keyword_counts)

    # st.markdown(f"### Skor Rata - Rata : {overall_average_score}")
    # st.markdown(f"### Kesimpulan Keseluruhan: {overall_conclusion}")

    st.markdown(f"### Sentiment Label: {sentiment_label}")
    st.markdown(f"### Dengan skor: {R}")

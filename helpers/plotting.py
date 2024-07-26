import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_sentiment_distribution(sentiment_counts):
    plt.figure(figsize=(10, 6))
    bars = sentiment_counts.plot(kind="bar", color=["red", "orange", "yellow", "lightgreen", "green"], alpha=0.8)
    for bar in bars.patches:
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.2, str(int(bar.get_height())), ha='center', va='bottom', fontsize=10, color='black')
    plt.title("Distribusi Skala Kepuasan", fontsize=16, fontweight='bold')
    plt.xlabel("Skala Kepuasan", fontsize=14)
    plt.ylabel("Jumlah Review", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    st.pyplot(plt)
